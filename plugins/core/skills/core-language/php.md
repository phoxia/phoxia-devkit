# PHP

- Use `strict_types` where compatible.
- Respect Composer, framework and PHP version constraints.
- Prefer typed properties, enums and explicit DTO boundaries.
- Use `match` for closed exhaustive cases; arrays or maps for registries.
- Avoid dynamic properties, global service location and string-built queries.
- Run PHPStan or Psalm only at the configured level.
- Measure OPcache, database and serialization behavior in production-like mode.
- Use PHPUnit or Pest and test authorization and validation.
