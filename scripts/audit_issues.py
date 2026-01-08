#!/usr/bin/env python3
import json, os, re, subprocess, sys

REPO = os.environ.get("REPO", "").strip()  # optional: owner/name
REQUIRED_DOD = re.compile(r"\b(Definition of Done|DoD)\b", re.I)
REQUIRED_ACC = re.compile(r"\b(Acceptance Criteria|Acceptance)\b", re.I)

def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    out = (p.stdout or "").strip()
    err = (p.stderr or "").strip()
    return p.returncode, out, err

def main():
    repo = REPO
    if not repo:
        rc, out, err = run(["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"])
        if rc != 0 or not out:
            print("ERR: could not determine repo (set REPO=owner/name).", file=sys.stderr)
            print(err if err else "(empty stderr)", file=sys.stderr)
            return 2
        repo = out

    rc, out, err = run(["gh", "issue", "list", "-R", repo, "--state", "all", "--limit", "500", "--json", "number,title,body"])
    if rc != 0 or not out:
        print("ERR: gh issue list did not return JSON (API/rate-limit/auth?).", file=sys.stderr)
        print(err if err else "(empty)", file=sys.stderr)
        return 2

    try:
        issues = json.loads(out)
    except Exception as e:
        print("ERR: could not parse JSON from gh output:", repr(e), file=sys.stderr)
        print(out[:300], file=sys.stderr)
        return 2

    missing = []
    for it in issues:
        body = it.get("body") or ""
        has_dod = bool(REQUIRED_DOD.search(body))
        has_acc = bool(REQUIRED_ACC.search(body))
        if not (has_dod and has_acc):
            missing.append((it.get("number"), has_dod, has_acc, it.get("title", "")))

    print(f"OK: scanned {len(issues)} issues in {repo}")
    if missing:
        print("ERR: issues missing required sections (number | DoD | Acceptance | title):")
        for n, d, a, t in missing:
            print(f"- #{n} | DoD={d} | Acceptance={a} | {t}")
        return 2

    print("OK: every issue contains DoD + Acceptance sections")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
