cwlVersion: v1.2
class: CommandLineTool
baseCommand: ["ourtool", "list-items"]
inputs:
  limit: { type: int, inputBinding: { prefix: "--limit" } }
  offset: { type: int, inputBinding: { prefix: "--offset" } }
  filters: { type: ["null", string], inputBinding: { prefix: "--filters-json" } }
outputs:
  result: { type: File, outputBinding: { glob: "result.json" } }
