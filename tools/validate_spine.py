#!/usr/bin/env python3
"""Offline maturity-spine validator: repo.maturity.yaml (repo-maturity.v1),
lab.manifest.json (lab.manifest.v1), service-manifest/functional-service.v1.json
(functional-service.v1). Zero required deps; PyYAML enables strict maturity checks."""
import json, re, sys, os

FUNCTION_ENUM={"speech","ocr","image","video","translation","embedding","reranking",
 "timeseries","graph","nlp","language-intelligence","routing","guardrail","agent-tool"}
STATUS_ENUM={"draft","experimental","candidate","approved","deprecated"}
MSP_ENUM={"forbidden-in-sourceos","lab-only","governed-runtime-only"}
PLANE_ENUM={"standards","runtime","governance","sourceos-carry","socios-lab","workspace-governance","cli","research","archive"}
MSTATUS_ENUM={"active","experimental","incubating","archival","deprecated"}
LEVELS={"M0","M1","M2","M3","M4","M5"}
CANON_ENUM={"canonical","reference","experimental","archive","stub"}

def fail(m): print(f"FAIL: {m}",file=sys.stderr); sys.exit(1)

def req_files():
    for f in ["repo.maturity.yaml","lab.manifest.json","service-manifest/functional-service.v1.json",
              "schemas/repo-maturity.schema.json","schemas/functional-service.schema.json",
              "datasets/README.md","evals/README.md","adapters/README.md","training-runs/README.md"]:
        if not os.path.exists(f): fail(f"missing required file: {f}")

def check_schemas():
    for s in ("schemas/repo-maturity.schema.json","schemas/functional-service.schema.json"):
        try: json.load(open(s))
        except Exception as e: fail(f"{s} invalid JSON: {e}")

def check_service():
    d=json.load(open("service-manifest/functional-service.v1.json"))
    if d.get("schemaVersion")!="functional-service.v1": fail("service schemaVersion")
    s=d.get("service",{})
    for k in ("id","name","ownerRepository","status"):
        if k not in s: fail(f"service.{k} required")
    if not re.match(r"^[a-z0-9][a-z0-9_.-]+$",s["id"]): fail(f"service.id pattern: {s['id']}")
    if s["status"] not in STATUS_ENUM: fail(f"service.status enum: {s['status']}")
    if not re.match(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$",s["ownerRepository"]): fail("ownerRepository")
    if d.get("function") not in FUNCTION_ENUM: fail(f"function not in canonical enum: {d.get('function')}")
    m=d.get("model",{})
    if "modelRef" not in m: fail("model.modelRef required")
    if m.get("mutableStatePolicy") not in MSP_ENUM: fail(f"mutableStatePolicy enum: {m.get('mutableStatePolicy')}")
    if not isinstance(d.get("inputs"),list) or not isinstance(d.get("outputs"),list): fail("inputs/outputs arrays")
    ev=d.get("evals",{})
    if not isinstance(ev.get("required"),bool) or not isinstance(ev.get("references"),list): fail("evals")
    g=d.get("governance",{})
    for k in ("ledgerRequired","guardrailRequired","routingRequired"):
        if not isinstance(g.get(k),bool): fail(f"governance.{k}")
    sc=d.get("sourceosCarry",{})
    if sc.get("carriesMutableModelState") is not False: fail("carriesMutableModelState must be false")
    for k in ("allowed","clientRefRequired"):
        if not isinstance(sc.get(k),bool): fail(f"sourceosCarry.{k}")

def check_lab():
    d=json.load(open("lab.manifest.json"))
    if d.get("schemaVersion")!="lab.manifest.v1": fail("lab.manifest schemaVersion")
    for k in ("lab","repository","modality","boundary","surfaces","serviceManifests"):
        if k not in d: fail(f"lab.manifest.{k} required")
    if not isinstance(d["surfaces"],list) or not d["surfaces"]: fail("surfaces non-empty array")
    if d["modality"] not in FUNCTION_ENUM: fail(f"modality enum: {d['modality']}")

def check_maturity():
    txt=open("repo.maturity.yaml").read()
    try:
        import yaml; d=yaml.safe_load(txt)
    except Exception:
        for key in ("schemaVersion: repo-maturity.v1","repository:","plane:","status:","maturity:",
                    "owners:","canonicality:","validation:","integrations:"):
            if key not in txt: fail(f"repo.maturity.yaml missing {key!r} (install pyyaml for strict)")
        return
    if d.get("schemaVersion")!="repo-maturity.v1": fail("maturity schemaVersion")
    for k in ("repository","plane","status","maturity","owners","canonicality","validation","integrations"):
        if k not in d: fail(f"repo.maturity.{k} required")
    if d["plane"] not in PLANE_ENUM: fail(f"plane enum: {d['plane']}")
    if d["status"] not in MSTATUS_ENUM: fail(f"status enum: {d['status']}")
    if d["canonicality"] not in CANON_ENUM: fail(f"canonicality enum: {d['canonicality']}")
    mat=d["maturity"]
    if mat.get("level") not in LEVELS: fail("maturity.level")
    if mat.get("targetLevel") not in (LEVELS-{"M0"}): fail("maturity.targetLevel")
    if not isinstance(mat.get("evidence"),list): fail("maturity.evidence array")
    if not (isinstance(d["owners"],list) and d["owners"]): fail("owners non-empty")
    v=d["validation"]
    if not isinstance(v.get("commands"),list) or not isinstance(v.get("ciRequired"),bool): fail("validation")
    if not isinstance(d["integrations"],list) or not d["integrations"]: fail("integrations non-empty")
    for it in d["integrations"]:
        if "repository" not in it or "relationship" not in it: fail("integration repository+relationship")

def main():
    req_files(); check_schemas(); check_service(); check_lab(); check_maturity()
    print("OK: speechlab maturity spine (repo-maturity.v1 + lab.manifest.v1 + functional-service.v1) validated")

if __name__=="__main__": main()
