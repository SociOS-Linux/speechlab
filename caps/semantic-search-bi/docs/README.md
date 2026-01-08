# semantic-search-bi (Capability Contract)
This cap defines the contract for semantic indexing + retrieval + explainability.

## What this is
- A *contract package*: schemas + triRPC surface + topics + validation tools.
- NOT a full implementation of search backends.

## Composition
- Ingestion caps (OCR/Image/Speech) produce normalized documents -> UpsertDocuments.
- Analytics/BI caps consume Query + Explain outputs for dashboards, triage, and casework.
- Evidence envelopes bind every RPC call to audit-ready traces.

## Wire format
- triRPC uses `TriuneEnvelope` with:
  - payload: JSON validated by schemas/*
  - evidence: JSON validated by schemas/evidence_envelope.json
