# /topics/semantic-search/*
These topics are stable routing keys used for:
- event emission
- audit trace stitching
- capability discovery + composition graphs

## /topics/semantic-search/upsert
Document ingestion/upsert lifecycle events.

## /topics/semantic-search/query
Query execution lifecycle events.

## /topics/semantic-search/explain
Explanation and feature-attribution lifecycle events.

## /topics/semantic-search/health
Health/diagnostic lifecycle events.

### Topic invariants
- Topics MUST be globally unique within the workspace.
- Topics MUST be deterministic strings, not runtime-generated GUIDs.
- Topics SHOULD be used as join keys for evidence traces.
