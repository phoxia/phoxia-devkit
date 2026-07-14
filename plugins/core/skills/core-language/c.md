# C

- Make ownership, lifetime and buffer length explicit.
- Prefer fixed-width integer types at binary and network boundaries.
- Treat all external sizes and indexes as hostile.
- Use `switch` for enums and dense integer cases; measure before replacing it with function tables.
- Compile with strong warnings and sanitizers in test builds.
- Check allocation, overflow, truncation, signedness and error returns.
- Use valgrind or platform tooling where sanitizers are unavailable.
- Avoid undefined behavior and non-portable assumptions unless isolated.
