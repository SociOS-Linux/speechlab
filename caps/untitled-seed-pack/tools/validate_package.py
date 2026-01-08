#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQ = [
  "capd/capability.jsonld",
  "mcp/tools.json",
  "rpc/trirpc.v1.proto",
  "schemas/jsonschema/untitled3_status_conduit_token.v1.json",
  "schemas/jsonschema/untitled4_items_list_envelope.v1.json",
  "schemas/jsonschema/untitled9_hydration_diagnostics_event.v1.json",
  "schemas/avro/agentbus.v1.ToolCalled.avsc",
  "schemas/avro/agentbus.v1.ToolReturned.avsc",
  "schemas/avro/agentbus.v1.TaskCompleted.avsc",
  "topics/glossary.jsonld",
  "topics/topics.json",
  "docs/trees/untitled_3_tree_enriched.json",
  "docs/trees/untitled_4_tree_enriched.json",
  "docs/trees/untitled_9_tree_enriched.json"
]

def must(p):
  fp = ROOT / p
  if not fp.exists():
    raise SystemExit(f"ERR missing: {p}")
  return fp

def json_ok(p):
  fp = must(p)
  try:
    json.loads(fp.read_text(encoding="utf-8"))
  except Exception as e:
    raise SystemExit(f"ERR invalid json: {p}: {e}")

def main():
  for p in REQ:
    if p.endswith((".json", ".jsonld", ".avsc")):
      json_ok(p)
    else:
      must(p)
  mcp = json.loads((ROOT/"mcp/tools.json").read_text(encoding="utf-8"))
  tok_tool = next(t for t in mcp["tools"] if t["name"]=="get_conduit_token")
  if "conduit_token" not in tok_tool.get("redactionKeys", []):
    raise SystemExit("ERR get_conduit_token missing redactionKeys.conduit_token")
  print("OK: capability package validates")

if __name__ == "__main__":
  main()
