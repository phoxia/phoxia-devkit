---
name: release
description: Analyzes, prepares or verifies an independent semantic release with channels, compatibility, migration and rollback.
argument-hint: "<analyze|prepare|verify> [scope]"
disable-model-invocation: true
---

# Release workflow

Recommend no release, patch, minor, major or pre-release from public-contract impact.

For pre-1.0: fix -> patch; feature or break -> minor with explicit notes.

For 1.0+: compatible fix -> patch; compatible feature -> minor; incompatible public contract -> major.

Create release notes, migration order, rollout, rollback, support status and approval evidence.

Do not tag, publish or deploy.
