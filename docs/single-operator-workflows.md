# Continue work without competing operators

Use this pattern for agents that share one browser, deployment console or other mutable resource. Store one current task/checkpoint, linked to its project and evidence notes. Another agent retrieves those records instead of replaying the conversation. The vault records ownership; it does not enforce a lock or resume an agent.

## Record scope before stopping

Distinguish a blocked item from a blocked service and a blocked operator. An unanswered consent can hold one item while unrelated work remains possible. A host's human-interaction request can still park the whole operator or shared surface. Never infer that unrelated work may continue during that wait. Record the actual host behavior and where the human step lives.

Keep the owner identity, exact resource, last completed action, held pages/state, uncertain external outcomes and next authorized action in the checkpoint. Idle status is not owner release. A successor needs explicit release/handoff and must check whether an interrupted external action already happened before retrying. Preserve original evidence and question mappings.

Return missing information to the designated coordinator through the existing result channel. Never create a reciprocal assignment to an ancestor already waiting on the worker. Forward an actual scoped answer with its original provenance; an agent's message, dispatch receipt or wake cannot substitute for consent, a human interaction or authority. Use only host-supported resumption, and stop a refused route instead of trying another identity or surface.

## Avoid repeating unchanged work

Keep a canonical-ID disposition index with evidenced aliases, source references, the decision and its relevant dependency identities. Distinguish a discovery preview from a complete review. Skip unchanged rejected/held items; reopen only for a named change in requirements, source evidence, policy or a scoped answer. A change requests review rather than clearing a hold. Previously completed or uncertain external actions always require duplicate/outcome checks.

Perform inexpensive prerequisites before building an artifact. Reconcile original external receipts once at a real start/resume boundary, then update progress from new positive receipts. Attempts and uploads do not count as external success. Keep actual event time, observed interval and verification time separate; ambiguous calendar boundaries remain unresolved.

Reuse completed artifact reviews only for the same item and unchanged raw hashes of every relevant input, policy, output and report, with a prior passing semantic/visual review. Hashes identify bytes; they do not prove complete dependency inventories, truth, current external state or authorization. See [artifact reviews](evidence-workflows.md).

## Bound recovery and measure the right result

Document the supported recovery condition, maximum attempts and state-loss consequences. Save state before recovery. Do not reset a reserved human page or uncertain external action. After the bounded recovery fails, report the affected service and preservation limit; pursue another service only when ownership and host access permit it.

Check live timeout configuration and installed host semantics separately. An estimated-duration field, wall-clock interval or completed turn may have no relationship to the enforced work limit. Record which was actually verified.

Use the [checkpoint body](../examples/single-operator-checkpoint.md). Keep three distinct milestones: verified local fix with executed checks; actual worker resumption with dated action evidence; external result with a positive receipt or preserved hold. A delivered handoff proves only delivery. Agent Vault supplies retrieval, revision checks and note links, not scheduling, locking, receipt verification, human-wait cancellation or application execution.

This agent-neutral recipe comes from a November 2026 local workflow repair. Examples are fictional; no host integration, performance improvement or external outcome is claimed by storing it.
