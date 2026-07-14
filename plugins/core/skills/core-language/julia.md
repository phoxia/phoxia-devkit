# Julia

- Aim for type-stable functions.
- Avoid abstractly typed fields in hot data structures.
- Measure allocations and compilation latency.
- Use BenchmarkTools correctly and interpolate benchmark inputs.
- Prefer multiple dispatch when it models behavior, not as a substitute for clear modules.
- Test numerical tolerances, dimensions and edge cases.
- Separate first-run compilation cost from steady-state performance.
