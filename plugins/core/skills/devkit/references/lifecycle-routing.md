# Lifecycle routing

- `feature start`: clarify outcome and scope, recover context, classify the record, plan, test, implement, verify and document with `phoxia-dev` and `phoxia-project`.
- `feature continue`: recover state and execute the exact unfinished action.
- `feature review`: check correctness and project-relevant completion gates.
- `fix start`: reproduce, find the shared root cause, add regression coverage, fix once and verify.
- `fix continue|review`: recover or review the same evidence chain.
- `docs ...`: delegate ADR/Feature Record/system/data/operations/changelog work to `phoxia-docs` and RFC/open-source work to `phoxia-open`.
- `release ...`: delegate to `phoxia-release` only when requested or `releaseSuggestions` is enabled and the project uses releases.
- `operate ...`: assess readiness, incident response, backups, tested restore and cost against actual project risk.
- `handoff`: delegate concise durable state to `phoxia-handoff`.

Do not suggest releases when the project or user has disabled them. After completion, offer no more than one enabled next action.
