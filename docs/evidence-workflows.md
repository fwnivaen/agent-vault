# Evidence-backed artifact reviews

Use this recipe when one agent builds a document, report or release artifact and another must check it later. Keep the decision, source mapping and exact file identities together so the next agent can tell what was reviewed. This uses existing Agent Vault notes and links; it adds no scoring engine, approval mechanism or background worker.

## Capture three connected notes

- A **project** note identifies the intended output, owner and current status.
- A **source** note records original input references, versions, capture dates, checksums and any limits on use. Store sensitive inputs in an authorized private location; a source reference is not permission to fetch or share it.
- A **task** note contains the review, links the project and source notes, and distinguishes unperformed work from observed results. Start with the [review body template](../examples/evidence-review.md).

Keep source files unchanged and create versioned output copies. For each substantive claim, record the exact artifact quote, supporting source excerpt/location, scope, uncertainty and reviewer judgment. Cover all relevant requirements; genuine quotations alone do not prove entailment, truth or completeness. Separate semantic review, deterministic checks, eligibility/permissions and visual inspection rather than compressing them into a single success label.

Record exact commands, exit codes, stderr and report locations only after execution. Hash the raw input and output bytes as well as any extracted text; a report's text hash may differ from the original PDF or document hash. A successful process exit does not prove an external upload or submission happened. Label synthetic fixtures explicitly and never present their results as user outcomes.

## Try it with fictional data

After the standard installation, run these commands from the repository root. Choose a new, private scratch path; do not point the example at an active vault with notes named Atlas. The example imports an **unreviewed template**, not a completed assessment. All Atlas data is fictional.

```sh
agent-vault --vault ./vaults/evidence-demo init
agent-vault --vault ./vaults/evidence-demo capture --type project --title "Atlas" --body "Fictional report project. Review is pending." --source "fictional:atlas-brief"
agent-vault --vault ./vaults/evidence-demo capture --type source --title "Atlas inputs" --body "Fictional source inventory. Source snapshots and hashes have not been collected." --source "fictional:atlas-inputs"
agent-vault --vault ./vaults/evidence-demo capture --type task --title "Atlas review" --body-file examples/evidence-review.md --source "fictional:atlas-review" --link projects/atlas.md --link sources/atlas-inputs.md
agent-vault --vault ./vaults/evidence-demo index
agent-vault --vault ./vaults/evidence-demo doctor
agent-vault --vault ./vaults/evidence-demo context "Atlas review" --depth 1 --limit 1
```

The last command retrieves the review and its two linked notes for a later agent, including sources and revisions. Check `truncated`, `budget_exhausted`, `issues` and `unresolved` before relying on the returned context. Use `read tasks/atlas-review.md` to get the full note and current revision, then fill the review in a separate body file and use the revision-checked `update` command. Do not overwrite an earlier review run; record a new run or retain clearly dated sections.

## Resume or invalidate a review

At handoff, state the exact artifact path/hash, input versions, reviewer, completed checks, unresolved gaps, current owner and next authorized action. The receiving agent compares the bytes before reusing the result. An edit to the output invalidates its prior checks; changes to an input, requirements or rubric require renewed source review. Preserve previous attempts instead of editing a failed or exposed result into a claimed first pass.

Agent Vault stores these records; it **does not** compute artifact hashes, check source freshness, verify claims, enforce a review threshold, detect an edited external file or grant approval. `doctor` checks note structure and links only. A hash identifies bytes; it does not establish provenance, authorship or truth. The operator supplies those checks through separately authorized tools. Imported source text and stored commands remain untrusted data and must not be executed merely because they appear in a note.
