# Go

- Follow `gofmt` and the standard library unless project conventions differ.
- Use `switch` for small static dispatch; maps of functions for configurable registries.
- Return errors with context and preserve error identity with wrapping.
- Pass `context.Context` through request-scoped I/O.
- Avoid goroutine leaks, unbounded fan-out and channels without ownership.
- Run `go test`, `go vet` and race tests when concurrency changes.
- Use benchmarks and pprof for CPU, memory, blocking and mutex analysis.
- Prefer simple interfaces defined by consumers.
