"""Small JSONC parser and source-preserving nested-object patcher."""

from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import re
import stat
import tempfile

from .common import fail


_NUMBER_RE = re.compile(r"-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?")


@dataclass
class Token:
    kind: str
    value: object
    start: int
    end: int


@dataclass
class Property:
    key: str
    key_start: int
    key_end: int
    value: "Node"
    comma_start: int = None
    comma_end: int = None


@dataclass
class Node:
    kind: str
    value: object
    start: int
    end: int
    open_end: int = None
    close_start: int = None
    properties: list = field(default_factory=list)


def _tokenize(source):
    tokens = []
    index = 0
    length = len(source)
    while index < length:
        char = source[index]
        if char.isspace():
            index += 1
            continue
        if source.startswith("//", index):
            newline = source.find("\n", index + 2)
            index = length if newline == -1 else newline + 1
            continue
        if source.startswith("/*", index):
            close = source.find("*/", index + 2)
            if close == -1:
                fail("unterminated JSONC block comment")
            index = close + 2
            continue
        if char in "{}[]:,":
            tokens.append(Token(char, char, index, index + 1))
            index += 1
            continue
        if char == '"':
            start = index
            index += 1
            escaped = False
            while index < length:
                current = source[index]
                if escaped:
                    escaped = False
                elif current == "\\":
                    escaped = True
                elif current == '"':
                    index += 1
                    break
                elif current in "\r\n":
                    fail("newline in JSONC string at byte {}".format(start))
                index += 1
            else:
                fail("unterminated JSONC string at byte {}".format(start))
            raw = source[start:index]
            try:
                value = json.loads(raw)
            except ValueError as exc:
                fail("invalid JSONC string at byte {}: {}".format(start, exc))
            tokens.append(Token("string", value, start, index))
            continue
        matched = _NUMBER_RE.match(source, index)
        if matched:
            raw = matched.group(0)
            tokens.append(Token("number", json.loads(raw), index, matched.end()))
            index = matched.end()
            continue
        literals = {"true": True, "false": False, "null": None}
        literal = next((item for item in literals if source.startswith(item, index)), None)
        if literal is not None:
            tokens.append(Token(literal, literals[literal], index, index + len(literal)))
            index += len(literal)
            continue
        fail("unexpected JSONC token at byte {}".format(index))
    return tokens


class Parser:
    def __init__(self, source):
        self.source = source
        self.tokens = _tokenize(source)
        self.index = 0

    def parse(self):
        if not self.tokens:
            fail("JSONC document is empty")
        node = self.parse_value()
        if self.index != len(self.tokens):
            fail("unexpected trailing JSONC token at byte {}".format(self.tokens[self.index].start))
        return node

    def peek(self, kind=None):
        if self.index >= len(self.tokens):
            return None
        token = self.tokens[self.index]
        return token if kind is None or token.kind == kind else None

    def take(self, kind):
        token = self.peek(kind)
        if token is None:
            found = self.peek()
            location = found.start if found else len(self.source)
            fail("expected JSONC {!r} at byte {}".format(kind, location))
        self.index += 1
        return token

    def parse_value(self):
        token = self.peek()
        if token is None:
            fail("expected JSONC value at end of document")
        if token.kind == "{":
            return self.parse_object()
        if token.kind == "[":
            return self.parse_array()
        if token.kind in ("string", "number", "true", "false", "null"):
            self.index += 1
            return Node(token.kind, token.value, token.start, token.end)
        fail("expected JSONC value at byte {}".format(token.start))

    def parse_object(self):
        opening = self.take("{")
        properties = []
        values = {}
        if self.peek("}"):
            closing = self.take("}")
            return Node("object", values, opening.start, closing.end, opening.end, closing.start, properties)
        while True:
            key = self.take("string")
            if key.value in values:
                fail("duplicate JSONC object key {!r}".format(key.value))
            self.take(":")
            value = self.parse_value()
            prop = Property(key.value, key.start, key.end, value)
            properties.append(prop)
            values[key.value] = value.value
            if self.peek(","):
                comma = self.take(",")
                prop.comma_start = comma.start
                prop.comma_end = comma.end
                if self.peek("}"):
                    break
                continue
            break
        closing = self.take("}")
        return Node("object", values, opening.start, closing.end, opening.end, closing.start, properties)

    def parse_array(self):
        opening = self.take("[")
        values = []
        if self.peek("]"):
            closing = self.take("]")
            return Node("array", values, opening.start, closing.end, opening.end, closing.start)
        while True:
            values.append(self.parse_value().value)
            if self.peek(","):
                self.take(",")
                if self.peek("]"):
                    break
                continue
            break
        closing = self.take("]")
        return Node("array", values, opening.start, closing.end, opening.end, closing.start)


def parse(source):
    return Parser(source).parse()


def _property(node, key):
    return next((item for item in node.properties if item.key == key), None)


def get_path(source, path):
    node = parse(source)
    for key in path:
        if node.kind != "object":
            fail("JSONC path {} traverses a non-object".format(".".join(path)))
        prop = _property(node, key)
        if prop is None:
            return False, None
        node = prop.value
    return True, node.value


def _newline(source):
    return "\r\n" if "\r\n" in source else "\n"


def _line_indent(source, offset):
    line_start = max(source.rfind("\n", 0, offset), source.rfind("\r", 0, offset)) + 1
    prefix = source[line_start:offset]
    return prefix if prefix.strip() == "" else ""


def _format_property(key, value, indent, newline):
    serialized = json.dumps(value, indent=2, ensure_ascii=False)
    lines = serialized.splitlines()
    first = json.dumps(key, ensure_ascii=False) + ": " + lines[0]
    return first + "".join(newline + indent + line for line in lines[1:])


def _nested_value(path, value):
    result = value
    for key in reversed(path):
        result = {key: result}
    return result


def _insert_property(source, node, key, value):
    newline = _newline(source)
    close_line_start = max(
        source.rfind("\n", 0, node.close_start), source.rfind("\r", 0, node.close_start),
    ) + 1
    close_prefix = source[close_line_start:node.close_start]
    insert_at = close_line_start if close_prefix.strip() == "" else node.close_start
    base_indent = close_prefix if close_prefix.strip() == "" else _line_indent(source, node.close_start)
    child_indent = base_indent + "  "
    if node.properties:
        inferred = _line_indent(source, node.properties[0].key_start)
        if inferred:
            child_indent = inferred
        last = node.properties[-1]
        if last.comma_start is None:
            comma_at = last.value.end
            source = source[:comma_at] + "," + source[comma_at:]
            if insert_at >= comma_at:
                insert_at += 1
        property_text = child_indent + _format_property(key, value, child_indent, newline) + newline
        return source[:insert_at] + property_text + source[insert_at:]
    property_text = newline + child_indent + _format_property(key, value, child_indent, newline)
    if insert_at == close_line_start and close_line_start > node.open_end:
        property_text = child_indent + _format_property(key, value, child_indent, newline) + newline
    else:
        property_text += newline + base_indent
    return source[:insert_at] + property_text + source[insert_at:]


def set_path(source, path, value):
    if not path:
        fail("cannot replace the JSONC document root")
    root = parse(source)
    node = root
    for index, key in enumerate(path):
        if node.kind != "object":
            fail("JSONC path {} traverses a non-object".format(".".join(path)))
        prop = _property(node, key)
        if index == len(path) - 1:
            if prop is None:
                return _insert_property(source, node, key, value)
            if prop.value.value == value:
                return source
            indent = _line_indent(source, prop.key_start)
            rendered = json.dumps(value, indent=2, ensure_ascii=False)
            lines = rendered.splitlines()
            replacement = lines[0] + "".join(_newline(source) + indent + line for line in lines[1:])
            return source[:prop.value.start] + replacement + source[prop.value.end:]
        if prop is None:
            return _insert_property(source, node, key, _nested_value(path[index + 1:], value))
        node = prop.value
    return source


def delete_path(source, path):
    if not path:
        fail("cannot delete the JSONC document root")
    node = parse(source)
    for key in path[:-1]:
        if node.kind != "object":
            fail("JSONC path {} traverses a non-object".format(".".join(path)))
        prop = _property(node, key)
        if prop is None:
            return source, False
        node = prop.value
    if node.kind != "object":
        fail("JSONC path {} has a non-object parent".format(".".join(path)))
    prop = _property(node, path[-1])
    if prop is None:
        return source, False
    if prop.comma_start is not None:
        return source[:prop.key_start] + source[prop.comma_end:], True
    index = node.properties.index(prop)
    if index > 0:
        previous = node.properties[index - 1]
        return (
            source[:previous.comma_start]
            + source[previous.comma_end:prop.key_start]
            + source[prop.value.end:],
            True,
        )
    return source[:prop.key_start] + source[prop.value.end:], True


def read_plain_json(path):
    if not path.exists():
        return {}, False
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        fail("cannot read {}: {}".format(path, exc))
    if not raw.strip():
        return {}, True
    try:
        value = json.loads(raw)
    except ValueError as exc:
        fail("cannot parse {} as JSON: {}".format(path, exc))
    if not isinstance(value, dict):
        fail("{} must contain a JSON object".format(path))
    return value, True


def nested_get(value, path):
    current = value
    for key in path:
        if not isinstance(current, dict):
            fail("config path {} traverses a non-object".format(".".join(path)))
        if key not in current:
            return False, None
        current = current[key]
    return True, current


def nested_set(value, path, replacement):
    current = value
    for key in path[:-1]:
        child = current.get(key)
        if child is None:
            child = {}
            current[key] = child
        if not isinstance(child, dict):
            fail("config path {} traverses a non-object".format(".".join(path)))
        current = child
    current[path[-1]] = replacement


def nested_delete(value, path):
    current = value
    for key in path[:-1]:
        if not isinstance(current, dict):
            fail("config path {} traverses a non-object".format(".".join(path)))
        if key not in current:
            return False
        current = current[key]
    if not isinstance(current, dict) or path[-1] not in current:
        return False
    del current[path[-1]]
    return True


def atomic_write(path, content):
    target = path
    if path.is_symlink():
        try:
            target = path.resolve(strict=True)
        except OSError as exc:
            fail("cannot resolve config symlink {}: {}".format(path, exc))
    parent = target.parent
    try:
        parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        mode = stat.S_IMODE(target.stat().st_mode) if target.exists() else 0o600
        descriptor, temporary = tempfile.mkstemp(prefix=".{}-".format(target.name), dir=str(parent))
        try:
            os.fchmod(descriptor, mode)
            with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as stream:
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, str(target))
        except Exception:
            try:
                os.unlink(temporary)
            except OSError:
                pass
            raise
    except OSError as exc:
        fail("cannot atomically write {}: {}".format(target, exc))
