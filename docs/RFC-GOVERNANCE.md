# RFC, ADR and Feature Record governance

Create an RFC for cross-domain, platform, ownership, security, privacy, governance or difficult migration decisions.

Draft RFCs have a slug and no number.

An accepted RFC receives the next number and immutable identity.

Use an ADR for an important local technical decision.

Use a Feature Record for a significant capability. Include flows, data, contracts, permissions, UI, failure matrix, tests, observability, rollout and version impact.

Infrastructure is classified by scope, not as a fourth record type. Cross-domain or platform infrastructure may require an RFC; an important local infrastructure choice usually uses an ADR.

English is canonical. Portuguese is an approved translation.

Generate both once, review them and copy exact files to product repositories. Store SHA-256 lock files. Do not regenerate translations during sync.

Use amendments for compatible clarification. Use a superseding RFC for a material normative change.
