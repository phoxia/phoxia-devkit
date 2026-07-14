# Rust

- Prefer enums and exhaustive `match` for closed state and dispatch.
- Do not replace `match` with `HashMap<&str, fn>` for a small static set without evidence.
- Use maps or trait registries when dispatch is genuinely dynamic.
- Make ownership and lifetime choices obvious before cloning.
- Avoid `unsafe` unless necessary, documented and tested with Miri or sanitizers where possible.
- Use `Result` with contextual errors; avoid panics in recoverable paths.
- Run `cargo fmt`, `cargo clippy`, `cargo test`.
- Profile release builds; use criterion for microbenchmarks.
- Watch allocations, lock contention, async task growth and blocking work inside Tokio.
