# Command reference

All commands use `agent-vault --vault PATH COMMAND`. Alternatively set `AGENT_VAULT`. The vault is never guessed from the current directory. JSON goes to stdout; errors go to stderr.

| Command | Arguments / behavior |
|---|---|
| `init` | Add the standard folders, private state and AGENTS guidance. Existing files are preserved. |
| `capture` | `--title TEXT --type TYPE --body TEXT` or `--body-file FILE`; repeat `--source`, `--tag`, `--link` as needed. Links are existing vault-relative `.md` paths. |
| `read PATH` | Return body, metadata and the current revision. |
| `classify PATH` | `--type TYPE --revision SHA`; set the type of an existing note, preserving its body, path and other metadata. Then preview an `organize` move if useful. |
| `update PATH` | `--revision SHA --body TEXT` or `--body-file FILE`; preserve metadata and back up the old bytes. The body is the full Markdown body including headings. |
| `search QUERY` | `--limit N` (1–100); lexical ranking over titles, tags and body. |
| `context QUERY` | `--depth N` (0–3), `--limit N` (1–20 seeds), `--max-chars N` (500–100000 body characters). Defaults: 1, 5 and 16000. |
| `graph` | Return note summaries, directed links, unresolved targets and unreadable-file issues. Incoming edges are backlinks. |
| `suggest` | `--limit N` (1–100); preview unlinked title/alias mentions. Does not edit files. |
| `link SOURCE TARGET` | `--revision SHA`; add a wikilink after verifying the two notes exist. |
| `organize PATH` | `--revision SHA`; preview moving to the folder for its frontmatter type. `--apply` makes a safe move. Linked notes may need a link-aware editor instead. |
| `index` | Generate the owned Home.md map. Refuse to replace an unrelated, user-owned Home.md. |
| `doctor` | Check broken/ambiguous links, duplicate IDs, unreadable notes and orphans. Orphans are informational. |
| `serve` | Optional MCP stdio server. `--allow-write` exposes mutation tools. |

Exit codes: **0** successful operation, **1** doctor found a structural issue, **2** invalid arguments or operation failure. A conflict does not overwrite the note. Orphan notes alone do not make doctor fail.

Capture from a file:

```sh
agent-vault --vault /path/to/memory capture --type source --title "Workshop notes" --body-file workshop.md --source "workshop-2026-11-08"
```

Context includes sources, revisions, link distance, per-note truncation and diagnostics. The body budget excludes metadata/JSON overhead, and lexical search is not a guarantee that every relevant note was found. Agents should inspect the returned documents and diagnostics before making claims.
