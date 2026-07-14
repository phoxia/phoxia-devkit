# Review routing

Select relevant checks from evidence; `review full` is not a command to run every checklist blindly.

- security: authentication, authorization, secrets, injection, abuse and supply chain;
- reliability/availability: shared corporate NAT means one IP is not one user; IP-only throttling can produce widespread `429`. Consider account, credential, device, organization and endpoint signals, capacity and dependency failure;
- privacy/data: classification, collection, access, retention, deletion, residency and incident impact;
- legal/licensing: verify provenance, license text, use and distribution. Strong copyleft or network-copyleft is not automatic “contamination”; evaluate actual obligations and compatibility;
- accessibility: keyboard, screen reader, focus, contrast, non-color state and appropriate target size;
- performance/cost: measure hot paths, scale assumptions and external spend before claims;
- architecture/contracts: ownership, versioned APIs/events, migrations, idempotency and rollback;
- operations/restore: a backup is not recovery evidence; require a tested restore path, observable failure and stated limitations.

Each finding contains evidence, impact, confidence, limitation and the smallest viable mitigation. Warn immediately on critical security, privacy, legal, availability or data-loss risk; collect lower-severity findings for the requested result.
