"""Evaluator-only probes. Run against one baseline, candidate or repaired dispatch directory."""

import argparse
import sys
from pathlib import Path


def observe(tick):
    result = {"job": "job-1", "kind": "original", "playable": True,
              "private_url": "synthetic-private-asset-handle"}

    def purchase():
        return {"id": "purchase-1", "job": "job-1", "state": "pending", "destination": "channel-1"}

    def deliver(order, asset, enabled=True, fail=False):
        calls, audit = [], []

        def send(destination, locator):
            if fail:
                raise OSError("unreachable: " + locator)
            calls.append((destination, locator))

        tick(order, enabled, asset, send, audit)
        return calls, audit

    expected = [("channel-1", result["private_url"])]
    order = purchase()
    calls, _ = deliver(order, result)
    yield "original delivered", calls == expected and order["state"] == "delivered"
    order = purchase()
    before, _ = deliver(order, result, enabled=False)
    after, _ = deliver(order, result)
    yield "pause and resume", before == [] and after == expected and order["state"] == "delivered"

    for key, value in (("job", "other-job"), ("kind", "preview"), ("playable", False)):
        order = purchase()
        calls, _ = deliver(order, dict(result, **{key: value}))
        yield "reject invalid " + key, calls == [] and order["state"] == "pending"

    order = purchase()
    _, audit = deliver(order, result, fail=True)
    yield "redacted failure with purchase ID", ("purchase-1" in str(audit)
                                               and result["private_url"] not in str(audit))
    calls, _ = deliver(order, result)
    yield "retry after transport failure", calls == expected and order["state"] == "delivered"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(args.source.resolve(strict=True)))
    from dispatch import tick

    results = list(observe(tick))
    for label, passed in results:
        print(("PASS" if passed else "FAIL") + " " + label)
    sys.exit(0 if all(passed for _, passed in results) else 1)
