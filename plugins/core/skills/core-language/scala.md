# Scala

- Respect the Scala version and ecosystem already chosen.
- Prefer algebraic data types and exhaustive matching.
- Keep effects explicit when the project uses an effect system.
- Avoid advanced type machinery that does not improve the domain contract.
- Watch collection conversions, lazy retention and accidental parallelism.
- Benchmark JVM behavior with JMH and inspect allocation.
- Use property testing for laws and invariants.
