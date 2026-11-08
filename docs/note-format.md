# Note format

Existing UTF-8 Markdown is readable without frontmatter. Newly captured notes use flat YAML properties, which Obsidian can display:

```markdown
---
id: 0d100000-0000-4000-8000-000000000001
title: Atlas
type: project
created: '2026-11-08T12:00:00+00:00'
updated: '2026-11-08T12:00:00+00:00'
tags:
  - example
sources:
  - https://example.com/atlas-brief
aliases:
  - Atlas documentation
---

# Atlas

A fictional project for organizing a team's documentation.

## Related

- [[people/alex-river]]
- [[decisions/markdown-first]]
```

`id` stays with the note when a user moves it. Revisions are SHA-256 hashes of the complete file bytes; they change with any edit, including metadata. `type` chooses the default folder. Unknown metadata is preserved when the body is updated. Logical note text normalizes Windows CRLF and classic CR line endings to LF; writes use LF, while revisions and recovery copies preserve the exact original bytes.

`tags`, `sources` and `aliases`, when present, must be lists of strings. A source can be a URL, local document reference or other human-readable citation. Sources are not automatically fetched or validated. Metadata uses safe YAML loading; executable YAML tags are rejected.

Relationships live in the body. Prefer full vault-relative wikilinks (`[[projects/atlas]]`) so duplicate basenames do not become ambiguous. Short names may resolve by unique filename, title or alias. Inline Markdown note links are relative to the containing note and should end in `.md`; URL-encode spaces. Heading/block suffixes resolve to their parent note; the heading or block itself is not validated.

Generated Home.md is a navigation aid, excluded from the knowledge graph to avoid making every note appear connected. Generated AGENTS.md is working guidance and is also excluded. Hidden folders, including `.obsidian`, `.git` and `.agent-vault`, are excluded from scanning.
