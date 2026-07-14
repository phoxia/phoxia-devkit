# Installation

The 1.0 installer is non-destructive.

It does not delete or replace:

```text
~/.claude
~/.claude.json
~/.codex
```

Managed state is stored under:

```text
~/.phoxia-devkit
```

Codex-compatible user skills are installed under:

```text
~/.agents/skills
```

POSIX launchers are written to `~/.local/bin`. PowerShell launchers are written to `~/.phoxia-devkit/bin`.

## Examples

```bash
./install-linux.sh --targets claude,codex --profiles all
phoxia-devkit doctor
phoxia-devkit status
```

Launchers show a static local hint by default. It performs no diagnostic and uses no model tokens. Disable it with `--no-startup-hints`; set deterministic banner language with `--locale pt-BR` or another locale, with English fallback.

The external executable is limited to install, update, uninstall, restore, status and installed-package doctor. Project work runs through `$phoxia-devkit` in Codex or `/phoxia-core:devkit` in Claude.


## Uninstall managed files

```bash
phoxia-devkit uninstall
```

Uninstall removes only Phoxia-managed profile directories, launchers and prefixed skills. It does not touch the user's normal Claude or Codex homes.
