# Python

- Read `pyproject.toml`, version constraints and environment manager first.
- Use type hints at public boundaries; use mypy or Pyright only if configured.
- Prefer `pathlib`, context managers, dataclasses and explicit exceptions.
- Use dictionary dispatch for registries; use `match` or `if` for small closed cases.
- Avoid mutable defaults, broad exceptions and hidden global state.
- Profile with `cProfile`, py-spy or scalene before optimizing.
- Prefer vectorized/native operations for numeric workloads, but measure conversion overhead.
- Use pytest and property tests where valuable.
- Respect async boundaries; do not call blocking I/O in the event loop.
