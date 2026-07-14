# Java

- Respect the configured JDK and build system.
- Prefer records, sealed types and exhaustive switches when supported.
- Use interfaces at stable boundaries, not for every class.
- Handle nullability explicitly; avoid unchecked Optional use in fields and hot loops.
- Manage thread pools and structured or virtual concurrency according to the installed JDK.
- Use JMH for microbenchmarks and Flight Recorder for real profiling.
- Watch allocation, GC pressure, N+1 persistence and blocking calls.
- Run unit, integration and compatibility tests through Maven or Gradle.
