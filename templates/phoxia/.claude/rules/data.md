---
paths:
  - "**/*.sql"
  - "**/migrations/**/*"
  - "**/prisma/**/*"
  - "**/entities/**/*"
  - "**/models/**/*"
---

# Data and tenancy

- Every tenant-owned query has enforced tenant scope.
- Unique constraints include tenant scope unless globally authoritative.
- Prefer expand-and-contract migrations.
- Backfills are bounded, resumable, idempotent and observable.
- Classify new fields and define retention and deletion.
