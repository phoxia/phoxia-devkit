# C++

- Use RAII, value semantics and standard containers.
- Prefer `std::unique_ptr`; use shared ownership only when real.
- Use `std::variant` and exhaustive visitation for closed alternatives.
- `switch` may compile to a jump table; function-pointer tables are not universally faster.
- Avoid raw owning pointers and unchecked casts.
- Enable warnings, sanitizers and static analysis.
- Benchmark optimized builds with realistic data.
- Watch allocations, virtual dispatch, cache locality, false sharing and exception boundaries.
- Respect the project's C++ standard and build system.
