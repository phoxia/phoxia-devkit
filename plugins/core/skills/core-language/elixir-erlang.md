# Elixir and Erlang

- Design supervision and failure domains before adding defensive catches.
- Keep processes small and state ownership explicit.
- Use pattern matching and tagged tuples for control flow.
- Avoid unbounded mailboxes and synchronous call chains.
- Make retries and backoff bounded.
- Test with ExUnit or Common Test and use property tests for protocols.
- Profile scheduler, reductions, memory and message queues.
- Preserve OTP conventions rather than recreating them with custom abstractions.
