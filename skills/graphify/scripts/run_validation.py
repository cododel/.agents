"""Validate transport structure without altering Graphify extraction semantics."""
from __future__ import annotations

import math


def rows(value: dict, key: str, required: bool = True) -> list[dict]:
    items = value.get(key, None if required else [])
    if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
        raise ValueError(f"{key} must be an array of objects")
    return items


def text_field(row: dict, key: str) -> str:
    value = row.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"missing string field: {key}")
    return value


def validate_extraction(value: object, sources: list[str] | None = None) -> dict:
    if not isinstance(value, dict):
        raise ValueError("extraction must be an object")
    nodes = rows(value, "nodes")
    edges = rows(value, "edges")
    hyperedges = rows(value, "hyperedges", required=False)
    for node in nodes:
        text_field(node, "id")
    for edge in edges:
        text_field(edge, "source")
        text_field(edge, "target")
    for edge in hyperedges:
        text_field(edge, "id")
        members = edge.get("nodes")
        if not isinstance(members, list) or len(members) < 3 or not all(isinstance(n, str) and n for n in members):
            raise ValueError("hyperedge requires at least three node IDs")
    if sources is not None:
        for row in nodes + edges + hyperedges:
            if text_field(row, "source_file") not in sources:
                raise ValueError("chunk contains a foreign source_file")
        for node in nodes:
            text_field(node, "label")
            if node.get("file_type") not in {"code", "document", "paper", "image", "rationale", "concept"}:
                raise ValueError("invalid node file_type")
        for edge in edges + hyperedges:
            text_field(edge, "relation")
            if edge.get("confidence") not in {"EXTRACTED", "INFERRED", "AMBIGUOUS"}:
                raise ValueError("invalid edge confidence class")
            score = edge.get("confidence_score")
            if type(score) not in (int, float) or not math.isfinite(score) or not 0 <= score <= 1:
                raise ValueError("invalid edge confidence_score")
    for key in ("input_tokens", "output_tokens"):
        count = value.get(key, 0)
        if type(count) is not int or count < 0:
            raise ValueError(f"{key} must be a nonnegative integer")
    return value


def validate_graph(value: dict) -> None:
    nodes = rows(value, "nodes")
    if not nodes:
        raise ValueError("refusing to publish an empty graph")
    identifiers = [text_field(n, "id") for n in nodes]
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("duplicate graph node ID")
    for edge in rows(value, "links"):
        if text_field(edge, "source") not in identifiers or text_field(edge, "target") not in identifiers:
            raise ValueError("graph has a dangling endpoint")
