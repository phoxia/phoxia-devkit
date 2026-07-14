# Documentation standard

Minimal project files:

```text
CLAUDE.md
PROJECT.yaml
CHANGELOG.md
docs/
  SYSTEM.md
  DATA.md
  OPERATIONS.md
  UX.md
  LEGAL.md
  records/
```

Phoxia projects also have `AGENTS.md` and `phoxia.project.yaml`.

`DATA.md` maintains Mermaid ER, DBML, dictionary, ownership, fields, relations, indexes, constraints, classification, retention and schema drift.

Migrations are normative history. ORM metadata is declared implementation. The deployed database is observed reality.

`OPERATIONS.md` maintains SLOs, telemetry, health, alerts, backup, degraded modes and rollback.

`LEGAL.md` tracks markets, personal data, minors, ads, consent, Terms and Privacy readiness.
