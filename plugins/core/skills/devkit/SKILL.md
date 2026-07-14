---
name: devkit
description: Use when a user greets the agent, asks what to do next, needs project setup or synchronization, starts or continues a feature or fix, requests a review, documentation, operations, release, handoff, mode, or DevKit preference.
---

# Phoxia DevKit navigator

Reply in the user's language; command names remain English. On a greeting or vague help request, do not scan the repository: mention `project guide` and `help`, then wait for intent.

For material work, read repository instructions and `.phoxia/project.yaml`, then load only the relevant reference:

- command lookup: `references/commands.md`
- project orientation and missing records: `references/context-discovery.md` and `references/project-guide.md`
- feature, fix, docs, release, operations or handoff: `references/lifecycle-routing.md`
- risk review: `references/review-routing.md`
- modes or preferences: `references/preferences-and-style.md`

Delegate implementation to `phoxia-dev`, project work to `phoxia-project`, documentation to `phoxia-docs`/`phoxia-open`, releases to `phoxia-release`, proprietary licensing to `phoxia-specialist`, UI to `phoxia-ui`, and handoffs to `phoxia-handoff`.

Lead with evidence. Surface critical security, privacy, legal, availability or data-loss risk immediately. After completing work, offer at most one contextual next action when enabled.
