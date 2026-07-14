# Ruby

- Follow the project's Ruby, Bundler, Rails and style versions.
- Use hashes for dynamic registries; use `case` for small closed dispatch.
- Avoid monkey patches and callbacks that hide important behavior.
- Watch N+1 queries, object allocation and unnecessary metaprogramming.
- Profile with stackprof, memory_profiler or project tools.
- Use RSpec or Minitest according to the repository.
- Keep service objects and domain models proportional to complexity.
- Validate background job idempotency and retry behavior.
