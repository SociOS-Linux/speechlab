#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "Makefile",
    "manifests/functional-service.json",
    "examples/smoke-input.json",
    "examples/smoke-output.json",
    "evidence/smoke-receipt.example.json",
    "tools/smoke.py",
    "tools/emit_sourceos_carry.py",
]

EXPECTED_SERVICE_ID = "speechlab.holmes.speech-pilot"
EXPECTED_FUNCTION = "speech"


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> int:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            return fail(f"missing required file: {rel}")

    manifest = load_json("manifests/functional-service.json")
    if manifest.get("schemaVersion") != "functional-service.v1":
        return fail("manifest must use functional-service.v1")
    if manifest.get("function") != EXPECTED_FUNCTION:
        return fail("manifest function must be speech")
    service = manifest.get("service", {})
    if service.get("id") != EXPECTED_SERVICE_ID:
        return fail("manifest service.id mismatch")
    if service.get("ownerRepository") != "SociOS-Linux/speechlab":
        return fail("manifest ownerRepository mismatch")

    sourceos = manifest.get("sourceosCarry", {})
    if sourceos.get("allowed") is not True:
        return fail("sourceosCarry.allowed must be true")
    if sourceos.get("carriesMutableModelState") is not False:
        return fail("SourceOS carry must not carry mutable model state")
    if sourceos.get("clientRefRequired") is not True:
        return fail("SourceOS carry must require a client ref")

    output = load_json("examples/smoke-output.json")
    if output.get("serviceId") != EXPECTED_SERVICE_ID:
        return fail("smoke output serviceId mismatch")
    ranking = output.get("ranking", [])
    if not ranking or ranking[0].get("id") != "holmes":
        return fail("smoke output must rank holmes first")
    if output.get("pass") is not True:
        return fail("smoke output pass must be true")

    receipt = load_json("evidence/smoke-receipt.example.json")
    if receipt.get("networkRequired") is not False:
        return fail("smoke receipt must be offline")
    if receipt.get("modelWeightsIncluded") is not False:
        return fail("smoke receipt must not include model weights")
    if receipt.get("mutableAdapterIncluded") is not False:
        return fail("smoke receipt must not include mutable adapters")

    print("OK: speechlab manifest and fixtures validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
