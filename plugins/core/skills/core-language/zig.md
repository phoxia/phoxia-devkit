# Zig

- Pass allocators explicitly and document ownership.
- Use error unions and `defer` for cleanup.
- Keep comptime logic understandable and bounded.
- Avoid hidden allocations and undefined behavior.
- Use tagged unions and switches for closed state.
- Test with `zig test` and build modes relevant to release safety.
- Benchmark optimized builds and inspect allocation and binary size.
