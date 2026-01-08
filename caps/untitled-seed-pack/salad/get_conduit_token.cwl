cwlVersion: v1.2
class: CommandLineTool
baseCommand: ["ourtool", "get-conduit-token"]
inputs:
  scopes: { type: ["null", string], inputBinding: { prefix: "--scopes-csv" } }
outputs:
  result: { type: File, outputBinding: { glob: "result.json" } }
