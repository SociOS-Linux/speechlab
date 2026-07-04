#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "examples" / "smoke-input.json"
EXPECTED = ROOT / "examples" / "smoke-output.json"


def terms(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def rank(payload: dict) -> dict:
    query = payload["query"]
    query_terms = terms(query)
    rows = []
    for candidate in payload.get("candidates", []):
        matched = sorted(query_terms & terms(candidate.get("text", "")))
        rows.append({
            "id": candidate["id"],
            "score": len(matched),
            "matchedTerms": matched,
        })
    rows.sort(key=lambda row: (-row["score"], row["id"]))
    return {
        "serviceId": "speechlab.holmes.speech-pilot",
        "query": query,
        "ranking": rows,
        "pass": bool(rows and rows[0]["id"] == "holmes"),
    }


def main() -> int:
    payload = json.loads(INPUT.read_text(encoding="utf-8"))
    actual = rank(payload)
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    if actual != expected:
        print(json.dumps({"ok": False, "actual": actual, "expected": expected}, indent=2), file=sys.stderr)
        return 1
    print(json.dumps({"ok": True, "serviceId": actual["serviceId"], "top": actual["ranking"][0]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
