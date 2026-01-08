# Architecture

This repository is a Linux-native capability for SourceOS.

## Scope
- Provide a reproducible, verifiable implementation surface.
- Expose stable contracts (RPC/API + schemas).
- Emit evidence/audit artifacts for key actions where applicable.

## Layout (canonical)
- `capd/`      Capability metadata (human + machine readable).
- `rpc/`       Wire contracts (e.g., triRPC service definitions).
- `schemas/`   JSON Schema or equivalent for messages/events/artifacts.
- `tools/`     Validators, linters, repo guards.
- `scripts/`   Dev/CI helpers.
- `docs/`      Human documentation.

## Invariants
- Linux-first, open-source, reproducible.
- `make validate` must succeed in CI.
