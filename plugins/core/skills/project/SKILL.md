---
name: project
description: Brainstorms, guides, bootstraps, synchronizes, audits and documents a project, including data models, legal readiness and Feature Records.
argument-hint: "<brainstorm|guide|bootstrap|sync|audit|data|feature|legal|ui> [scope]"
---

# Project workflow

- `brainstorm`: ask about problem, users, goals, platforms, data, minors, ads, identity, payments, performance, budget, license and design. Produce a brief and alternatives. Do not scaffold.
- `guide`: recover context and the smallest unfinished next step using `../devkit/references/context-discovery.md` and `../devkit/references/project-guide.md`.
- `bootstrap`: create the approved minimal setup.
- `sync`: check `.claude/project-state.local.json`; skip when no relevant files changed.
- `audit`: review architecture, contracts, data, security, legal readiness, UI and operations.
- `data`: create or refresh Mermaid ER, DBML, dictionary and schema lock.
- `feature`: create a Feature Record and failure matrix.
- `legal`: assess Terms, Privacy, age, advertising and consent readiness without claiming compliance.
- `ui`: create a visual contract and screenshot regression plan.
