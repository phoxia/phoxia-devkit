# Release and versioning policy

Each product and repository has an independent version.

## Semantic versioning

- Patch: backward-compatible correction.
- Minor: backward-compatible capability.
- Major: incompatible public-contract change.
- `0.y.z`: initial development.
- `1.0.0`: first stable public contract.

## Channels

```text
experimental -> alpha -> beta -> rc -> stable
```

## Examples

- `0.0.1`: disposable prototype.
- `0.1.0`: first usable preview.
- `0.4.2`: preview correction.
- `1.0.0-alpha.1`: early stable candidate.
- `1.0.0-beta.1`: broader testing.
- `1.0.0-rc.1`: intended stable release unless blocked.
- `1.0.0`: compatibility commitment.

For pre-1.0 products, fixes use patch and features or breaking changes use minor with explicit notes.

For 1.0 and later, `fix` suggests patch, `feat` suggests minor, and breaking public contracts suggest major.

Commit messages are evidence, not final authority. A maintainer approves the release plan.
