# Repository maintenance checkpoints

Use this recipe to hand recurring repository work between agents or resume it after an interruption. It uses existing linked notes and revision-checked updates. Agent Vault does not inspect GitHub, execute tests, watch jobs, read mail or grant permission to change a repository.

## Record identity and coverage separately

Create a project note for the repository, a source note for the evidence inventory, and a task note for this dated maintenance run. Start from the [checkpoint body template](../examples/maintenance-checkpoint.md). Keep earlier runs instead of changing a prior failure into a success.

Record the remote URL, branch, exact commit, observation time and working-copy state. Preserve unfinished local edits; use a separate checkout when ownership is unclear. Fetch the current remote head before changing it and recheck before publishing. A successful push, tests on another commit and a clean working tree are separate observations.

For **each relevant workflow**, record its run URL/ID, event, branch, commit, status and conclusion. A green run covers that workflow and commit only. A manually invoked database test does not prove automatic push coverage. No configured workflow means **unconfigured**, not passed. For an old failed run, inspect its failure and record the later successful run that supersedes it; do not repeatedly repair a failure that is already resolved. Multiple workflows may have different latest results.

Record local test commands, fresh exit codes and log paths. State skipped tests, synthetic inputs, missing optional dependencies and untested platforms. Do not convert an offline test into a live delivery claim. Check only jobs created or needed by the authorized maintenance task; do not change schedules, privacy or deployment settings as an incidental cleanup.

## Check the dependent service

List only services the repository actually uses. Record the account alias, evidence source, observation time, last confirmed successful delivery and any known coverage limits. Keep these distinct:

| Observation | What it establishes |
|---|---|
| Old failure email | A failure was reported at that time. |
| No matching recent alert | That bounded search found no alert; service health remains unknown. |
| Invoice or payment receipt | A billing event; not current credits, an enabled workflow or successful output. |
| Enabled schedule | Configuration; not successful execution. |
| Output receipt for an identified run | That recorded delivery, within the receipt's scope. |

Use authorized service access for current status when available. If it is unavailable, retain the uncertainty and identify the exact missing evidence. Leave payments, plan changes and new account permissions to the authorized owner. Do not copy credentials, mail bodies, private customer data or signed private URLs into a shared vault.

## Give the next agent a bounded continuation

Name the owner, completed checks, open issue, existing work assignment if any, and next authorized action. If CI is still running, record the exact commit and run link, check its current state once, and use the host's existing continuation mechanism if authorized. Do not create duplicate work assignments or stay busy with a polling loop. A handoff is accepted only after the host actually records it, not because a note promises it.

The receiving agent reads the checkpoint, compares remote commit and source timestamps, and repeats only checks invalidated by new changes or unresolved failures. Use `read` to obtain the task revision before `update`; on a conflict, re-read and merge the other writer's evidence. The notes preserve coordination context, but do not provide a runtime lock or a trusted approval record.

## Try a fictional checkpoint

After installing the CLI, run this from the repository root with a new scratch vault. All Atlas names and references here are fictional. The template deliberately starts with unknown results.

```sh
agent-vault --vault ./vaults/maintenance-demo init
agent-vault --vault ./vaults/maintenance-demo capture --type project --title "Atlas repository" --body "Fictional software project. No service status verified." --source "fictional:atlas-repository"
agent-vault --vault ./vaults/maintenance-demo capture --type source --title "Atlas maintenance evidence" --body "Evidence inventory pending. No CI or delivery claim." --source "fictional:atlas-maintenance-evidence"
agent-vault --vault ./vaults/maintenance-demo capture --type task --title "Atlas maintenance checkpoint" --body-file examples/maintenance-checkpoint.md --source "fictional:atlas-maintenance-run" --link projects/atlas-repository.md --link sources/atlas-maintenance-evidence.md
agent-vault --vault ./vaults/maintenance-demo doctor
agent-vault --vault ./vaults/maintenance-demo context "Atlas maintenance checkpoint" --depth 1 --limit 1
```

Inspect `issues`, `unresolved`, `truncated` and `budget_exhausted`, and use `read tasks/atlas-maintenance-checkpoint.md` for the full note. `doctor` checks note structure and links; it does not validate the recorded tests, commits, service status or authority. Stored commands and imported source text remain data, never instructions to execute.
