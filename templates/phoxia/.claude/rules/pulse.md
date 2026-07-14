---
paths:
  - "**/events/**/*"
  - "**/*event*.{ts,js,rs,json,yaml,yml}"
  - "**/consumers/**/*"
  - "**/producers/**/*"
---

# Pulse

- Event names describe completed facts.
- Use the versioned Phoxia envelope.
- Define tenant, subject, partition key, ordering, classification and retention.
- Producers coordinate durable state with outbox when needed.
- Consumers persist idempotency state.
- Define replay and dead-letter behavior.
