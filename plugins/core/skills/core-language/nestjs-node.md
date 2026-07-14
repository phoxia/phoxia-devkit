# NestJS and Node.js services

- Keep controllers thin and application behavior explicit.
- Validate DTOs at external boundaries.
- Do not leak ORM entities into contracts.
- Make request scope and provider lifetimes deliberate.
- Keep event-loop work bounded; move CPU work appropriately.
- Test guards, authorization, interceptors and serialization.
- Use outbox and idempotency for reliable asynchronous flows.
- Profile Node and database behavior before architectural rewrites.
