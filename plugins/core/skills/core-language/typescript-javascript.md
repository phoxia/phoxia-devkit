# TypeScript and JavaScript

- Prefer TypeScript strict mode for maintained application code.
- Model discriminated unions explicitly and use exhaustive checks.
- Use `switch` for closed exhaustive unions; use typed handler maps for extensible data-driven dispatch.
- Define handler maps once, not inside hot calls, and use `satisfies Record<...>` where helpful.
- Avoid `any`; narrow `unknown` at boundaries.
- Respect the repository package manager and lockfile.
- Profile Node with built-in profiling, Clinic or the project's tooling.
- Watch event-loop blocking, N+1 I/O, uncontrolled Promise concurrency and retained closures.
- Run actual package scripts for lint, typecheck and tests.
