# Context discovery

Stop when evidence is sufficient for the requested scope. Use this precedence:

1. `AGENTS.md`, `CLAUDE.md`, `.phoxia/project.yaml` and repository policy.
2. registered RFC copies, indexes, dependencies and locks.
3. ADR and Feature Record decisions.
4. versioned APIs, events, data contracts and migrations.
5. tests.
6. implementation.
7. Git history.

Locate record paths from project configuration before guessing. Search accepted or active records by domain, service, contract and feature; follow dependencies and supersession. When documentation conflicts with tests or contracts, report the conflict rather than silently choosing.

Use an RFC for cross-domain/platform, ownership, security/privacy, governance or difficult migration decisions. Use an ADR for an important local technical decision. Use a Feature Record for a significant capability. Infrastructure is not a fourth type: platform scope may require an RFC; local scope usually needs an ADR. Recommend the missing record before high-impact work when intent cannot be recovered safely.

For material conclusions, state evidence, inference, confidence and limitations.
