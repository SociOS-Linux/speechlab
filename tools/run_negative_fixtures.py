#!/usr/bin/env python3
"""M3 negative-fixture runner: every fixture under fixtures/invalid/ MUST be rejected
by its schema. Exits non-zero if any invalid document unexpectedly validates — that would
mean the schema/validator has regressed and could admit a malformed manifest."""
import json, os, sys, glob
import jsonschema
try:
    import yaml
except Exception:
    yaml=None

FS="schemas/functional-service.schema.json"
RM="schemas/repo-maturity.schema.json"

def load(p):
    if p.endswith((".yaml",".yml")):
        return None if yaml is None else yaml.safe_load(open(p))
    return json.load(open(p))

def schema_for(p):
    b=os.path.basename(p)
    if b.startswith("functional-service"): return json.load(open(FS))
    if b.startswith("maturity"): return json.load(open(RM))
    return None

def main():
    fixtures=sorted(glob.glob("fixtures/invalid/*"))
    if not fixtures:
        print("FAIL: no negative fixtures found under fixtures/invalid/", file=sys.stderr); return 1
    leaked=0
    for p in fixtures:
        s=schema_for(p)
        if s is None:
            print(f"  SKIP (no schema mapping): {p}"); continue
        d=load(p)
        if d is None:
            print(f"  SKIP (pyyaml unavailable): {p}"); continue
        try:
            jsonschema.validate(d, s)
            print(f"  FAIL: {p} unexpectedly VALIDATED — schema too loose"); leaked+=1
        except jsonschema.ValidationError as e:
            print(f"  OK rejected: {os.path.basename(p)} :: {e.message[:70]}")
    if leaked:
        print(f"{leaked} invalid fixture(s) passed validation", file=sys.stderr); return 1
    print("OK: all negative fixtures correctly rejected"); return 0

if __name__=="__main__":
    raise SystemExit(main())
