# Enrichment update (v2.14) — Untitled 3, 4, 9

This update adds **semantic labels + symbol labels + per-node documentation snippets** for three trees:

- **Untitled 3**: success response + conduit token semantics
- **Untitled 4**: paginated items list schema (context scopes, mapping, flags)
- **Untitled 9**: React hydration bootstrap + recoverable error logging

## Remediation notes
- **Untitled 4** could not be parsed as strict JSON due to malformed/migration fields in the extracted text (e.g., `context_scopes_v2` sometimes appearing without a value). The resulting tree is therefore a **schema-level reconstruction** based on observed keys and repeated field patterns.
- **Untitled 9** is minified; the tree is an **intent-level decomposition** (globals → logging → hydrate root) grounded in stable React patterns visible in the snippet.

## Files added
- `untitled_3_tree_enriched.json` / `.html`
- `untitled_4_tree_enriched.json` / `.html`
- `untitled_9_tree_enriched.json` / `.html`
