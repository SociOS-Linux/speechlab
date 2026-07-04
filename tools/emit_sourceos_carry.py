#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "functional-service.json"


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    service = manifest["service"]
    carry = {
        "schemaVersion": "functional-service-carry.v0",
        "kind": "FunctionalServiceCarry",
        "carryId": "urn:srcos:model-carry:functional-service:speechlab-holmes-pilot",
        "displayName": "SpeechLab Holmes Pilot Carry Profile",
        "service": {
            "id": service["id"],
            "ownerRepository": service["ownerRepository"],
            "function": manifest["function"],
            "manifestRef": "SociOS-Linux/speechlab:manifests/functional-service.json"
        },
        "sourceos": {
            "includeInImageBuilds": True,
            "enabledByDefault": False,
            "activationRequiresOptIn": True,
            "carriesMutableModelState": False,
            "carriesModelWeights": False,
            "clientRefRequired": True
        },
        "runtime": {
            "mode": "local-client-reference",
            "networkDefault": "denied",
            "launchProfileRef": "urn:srcos:launch-profile:speechlab-holmes-pilot:disabled-v0",
            "healthCheck": "make smoke"
        },
        "policy": {
            "localOnlyDefault": True,
            "sendPromptOffDeviceDefault": False,
            "allowToolUse": False,
            "allowNetwork": False,
            "allowModelDownload": False,
            "requiresSignedServiceReference": True,
            "requiresLedgerForPromotion": True,
            "requiresSignedIntentForPersonalTuning": True
        },
        "evidence": {
            "emitRuntimeHealth": True,
            "emitRoutingDecision": True,
            "emitSmokeReceipt": True,
            "emitPromptHashOnly": True,
            "smokeReceiptRef": "SociOS-Linux/speechlab:evidence/smoke-receipt.example.json"
        },
        "integrations": {
            "productSurface": "SocioProphet/holmes",
            "workspaceController": "SocioProphet/sociosphere",
            "contractSpine": "SocioProphet/functional-model-surfaces",
            "carryAuthority": "SourceOS-Linux/sourceos-model-carry",
            "optInAutomation": "SociOS-Linux/socios",
            "governanceLedger": "SocioProphet/model-governance-ledger",
            "router": "SocioProphet/model-router"
        }
    }
    print(json.dumps(carry, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
