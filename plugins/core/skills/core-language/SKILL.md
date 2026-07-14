---
name: core-language
description: Loads concise language and framework guidance only when implementing, reviewing, debugging or optimizing code in a specific technology.
argument-hint: "[task or files]"
---

# Language and framework engineering

Analyze the requested task and repository evidence.

1. Detect languages from file extensions, manifests and toolchain files.
2. Read `common.md`.
3. Read only the matching language and framework files in this skill directory.
4. Prefer the versions, tools and conventions actually present in the repository.
5. Do not load unrelated language files.
6. Do not convert code to another language unless requested.
7. Do not claim an optimization without measurement.

For unfamiliar languages, use `new-language-template.md` to form a temporary evidence-based guide.

When dispatch design is relevant, apply the language-specific guidance. Never impose object maps, switches, inheritance, functional style, DDD or any single paradigm universally.
