# Roadmap

The first release concentrates on connected Markdown, cross-agent retrieval and guarded edits. These additions are future work, not implemented features:

- Link-aware, multi-file move transactions with preview and recovery.
- Incremental search for larger vaults, while keeping Markdown canonical.
- Optional local semantic retrieval with visible provenance and no mandatory provider.
- Reviewable import adapters for documents and selected inbox exports.
- Scoped collections so a client can be limited to a subset of a vault.
- Conflict/contradiction review, stale-fact reminders and richer task handoffs.
- A tested compatibility matrix for specific agent hosts.

Any ingestion or reasoning feature should keep the original source, show uncertainty and let people inspect what will be saved. Core retrieval and file access should continue working without a model subscription.
