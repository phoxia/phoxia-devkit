# Common language guidance

- Inspect manifests, compiler versions, lockfiles and CI before recommending tools.
- Use idiomatic ownership, error and concurrency models.
- Prefer explicit invariants and typed boundaries.
- Avoid premature abstraction and premature optimization.
- Measure hot paths with the ecosystem profiler.
- Preserve backward compatibility where contracts are consumed externally.
- Use formatter, linter, type checker, tests and sanitizer supported by the project.
- Avoid unbounded concurrency, retries, queues and memory growth.
- Never treat average-case complexity as a complete performance claim.
- Choose dispatch by semantics, exhaustiveness, extensibility and measured cost.
