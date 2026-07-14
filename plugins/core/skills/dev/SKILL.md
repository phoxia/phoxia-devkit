---
name: dev
description: Plans, implements, debugs, reviews, tests or optimizes software using repository evidence and language-aware guidance.
argument-hint: "<plan|implement|debug|review|test|optimize> [task]"
---

# Development workflow

Read repository instructions and manifests.

- `plan`: current state, scope, ordered steps, tests, compatibility and risk. Do not implement.
- `implement`: smallest coherent change, tests, contracts, verification and final diff.
- `debug`: reproduce, collect evidence, test hypotheses, fix root cause and add regression coverage.
- `review`: risk-based correctness, security, data, API, performance and accessibility review.
- `test`: smallest valuable behavioral test matrix.
- `optimize`: metric, baseline, profile, change, verify and compare.

Read only relevant files under `core-language` when language specifics matter.
