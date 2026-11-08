# Contributing

Use Python 3.11+. Install `python -m pip install -e '.[mcp]'`, then run `python -m unittest discover -s tests -v`. Tests use temporary fictional vaults; never add real user notes, credentials or absolute personal paths to fixtures.

Keep Markdown canonical and core dependencies small. New behavior should work through both the CLI and optional MCP adapter when appropriate. Preserve unfamiliar metadata, source provenance and existing notes. Write tests for user-visible behavior, conflicts, boundaries and recovery, rather than snapshots of implementation details.

Document what is implemented and what remains planned. Specific agent-host support needs a real integration test before being advertised as verified. Avoid provider-specific coupling and generated authorship trailers.
