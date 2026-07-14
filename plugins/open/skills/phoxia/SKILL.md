---
name: phoxia
description: Maintains Phoxia project standards, RFCs, Pulse events, contracts and open-source readiness.
argument-hint: "<project-update|rfc-analyze|rfc-create|rfc-amend|rfc-sync|event|contract|open-source-readiness> [scope]"
---

# Phoxia workflow

Read `AGENTS.md`, `phoxia.project.yaml`, accepted RFC copies, schemas and tests.

- `project-update`: audit repository identity, README, license, CLA, contribution guide, security, docs, data model, CI and release policy.
- `rfc-analyze`: classify as no RFC, ADR, Feature Record, amendment, new RFC or superseding RFC.
- `rfc-create`: create English and Portuguese drafts. Drafts have no number.
- `rfc-amend`: preserve historical text and append a compatible amendment.
- `rfc-sync`: copy accepted files and update SHA-256 locks. Do not regenerate.
- `event`: design a completed-fact Pulse event with idempotency, ordering, classification, retention and replay.
- `contract`: design API or command auth, tenant, idempotency, errors, compatibility and tests.
- `open-source-readiness`: verify license, CLA, governance, community, security, templates and release workflow.
