# Security and privacy

For a suspected vulnerability, use the repository's private vulnerability reporting feature if available. Otherwise open a minimal issue asking for a private reporting channel without including private notes or credentials.

This local tool can read and, when enabled, write within the selected vault. Only select directories the connecting agent may access. Treat content as untrusted input. A remote model may receive retrieved text under the host's settings. Local recovery history also contains previous note contents; protect it like the vault itself.

The tool rejects path traversal, symbolic-link notes and symbolic-link private state. This is not a sandbox against a malicious process that can mutate the filesystem concurrently. External editor/sync races are not fully preventable with an application lock. Use a trusted local directory, coordinate writers and maintain backups.
