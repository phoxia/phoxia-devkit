# C# and .NET

- Enable nullable reference types where compatible.
- Use async end to end; avoid `.Result` and `.Wait()` in async flows.
- Pass `CancellationToken` for cancellable I/O.
- Prefer records and discriminated-style modeling for immutable messages.
- Use switch expressions for closed patterns; dictionaries for dynamic registries.
- Avoid unnecessary LINQ allocations in hot paths.
- Use BenchmarkDotNet and dotnet-counters or traces for performance.
- Test authorization, serialization and EF query behavior.
- Dispose resources with `using` and avoid hidden service locator access.
