#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def die(msg: str, code: int = 2):
  print(f"ERR: {msg}", file=sys.stderr)
  sys.exit(code)

def ok(msg: str):
  print(f"OK: {msg}")

def try_parse_yaml(p: Path):
  # YAML is optional; we parse with PyYAML if present, else do a minimal key presence check.
  text = p.read_text(encoding="utf-8")
  try:
    import yaml  # type: ignore
    return yaml.safe_load(text), "pyyaml"
  except Exception:
    # minimal: ensure a few required keys exist
    required = ["capability_id:", "capability_version:", "interfaces:", "tritrpc:"]
    missing = [k for k in required if k not in text]
    if missing:
      die(f"{p}: YAML parser unavailable and minimal check failed; missing {missing}")
    return {"_minimal_ok": True}, "minimal"

def parse_json(p: Path):
  try:
    return json.loads(p.read_text(encoding="utf-8"))
  except Exception as e:
    die(f"{p}: invalid JSON ({e})")

def main():
  # structure
  must_exist = [
    ROOT/"capd"/"capability.yaml",
    ROOT/"rpc"/"tritrpc"/"semantic_search.proto",
    ROOT/"schemas",
    ROOT/"topics"/"semantic-search.md",
    ROOT/"tools"/"validate_package.py",
    ROOT/"examples"/"upsert_documents_request.json",
    ROOT/"examples"/"query_request.json",
    ROOT/"examples"/"explain_request.json",
  ]
  for p in must_exist:
    if not p.exists():
      die(f"missing required path: {p}")

  ok("package structure looks sane")

  capd, mode = try_parse_yaml(ROOT/"capd"/"capability.yaml")
  ok(f"capd parses ({mode})")

  # proto sanity
  proto = (ROOT/"rpc"/"tritrpc"/"semantic_search.proto").read_text(encoding="utf-8")
  if "service SemanticSearchService" not in proto:
    die("proto missing service SemanticSearchService")
  for m in ["UpsertDocuments","Query","Explain","Health"]:
    if f"rpc {m}" not in proto:
      die(f"proto missing rpc {m}")
  ok("tritrpc proto looks sane")

  # schemas parse
  schemas_dir = ROOT/"schemas"
  schema_files = sorted([p for p in schemas_dir.glob("*.json") if p.is_file()])
  if not schema_files:
    die("no schemas found")
  for p in schema_files:
    parse_json(p)
  ok("json schemas parse")

  # examples parse
  for p in (ROOT/"examples").glob("*.json"):
    parse_json(p)
  ok("examples parse")

  ok("NOTE: YAML + Avro semantic validation is intentionally minimal here; wire into global validators next.")
  ok("capability package validates")

if __name__ == "__main__":
  main()
