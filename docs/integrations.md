# Agent integrations

There are three ways to use the same vault:

1. **Files:** any agent that can read authorized Markdown directories can consume and organize the notes. Use the agent protocol; coordinate writes and backups yourself.
2. **CLI:** a terminal-capable agent gets JSON results, diagnostics, revisions, local history and a shared writer lock.
3. **MCP:** the optional official Python SDK exposes the same operations over stdio. A compatible host launches `agent-vault --vault ABSOLUTE_PATH serve` as a child process.

No model-specific SDK, API key, embedding service, cloud database, Jarvis component or Obsidian plugin is required. The MCP package is optional; core installation only needs PyYAML and filelock.

## MCP tools

Read-only mode exposes `search_notes`, `read_note`, `get_context`, `get_graph`, `suggest_links` and `vault_health`.

Adding `--allow-write` exposes `capture_note`, `update_note`, `classify_note`, `link_notes`, `organize_note` and `rebuild_index`. There is no delete tool, remote fetch tool or arbitrary shell tool. The host still decides whether each invocation is allowed. Running a write-capable server does not authorize an agent to ignore the user's instructions.

The README includes a generic `mcpServers` configuration example. Use an absolute executable path and vault path; avoid relying on an interactive shell's activated environment. MCP transport is local stdio only in this version. Remote agents need an authorized local connection or access to a copy/sync of the same vault; the repository itself does not host anyone's memory.

## What is verified

Automated tests connect the official MCP client to the real stdio command, discover tools, retrieve linked context and check read-only exposure. A second client reads the first client's captured note, updates it, and receives a conflict for a stale revision.

These are protocol tests, not claims that every Claude/GPT/MausBot product has been manually connected. Hosts differ in filesystem permissions, MCP support and configuration. Agents without MCP can still use the CLI or ordinary files.
