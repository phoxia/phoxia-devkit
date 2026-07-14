# Phoxia DevKit 1.0.2

A multi-profile development and software-governance kit for **Claude Code and Codex**.

Configure the current repository with a preview, confirmation and automatic backup:

```bash
npx @phoxia/devkit init
phxdk init --mode update
phxdk init --mode replace --dry-run
```

Use `--yes` only after reviewing the same preview. The separate `phxdk install` command installs profiles and launchers in your home directory.

## Public package boundaries

This public distribution contains:

- Personal, Work, Phoxia and Specialist profiles;
- portable Agent Skills;
- Claude Code plugins and project adapters;
- Codex `AGENTS.md`, skills and custom-agent adapters;
- deterministic installation and contextual project workflows inside the agents.

## Install Claude and Codex together

Linux or macOS:

```bash
./install-linux.sh --targets claude,codex --profiles all
```

Windows PowerShell:

```powershell
.\install-windows.ps1 --targets claude,codex --profiles all
```

The installer is non-destructive. It stores managed profiles under `~/.phoxia-devkit`, installs Codex skills under `~/.agents/skills`, and creates launchers without deleting `~/.claude` or `~/.codex`.

Launchers include:

```text
claude-personal     codex-personal
claude-work         codex-work
claude-phoxia       codex-phoxia
claude-specialist   codex-specialist
```

## Work with a project

```text
$phoxia-devkit project guide
$phoxia-devkit feature start
$phoxia-devkit fix start
$phoxia-devkit review full
$phoxia-devkit mode direct
```

Claude uses `/phoxia-core:devkit` instead of `$phoxia-devkit`. Commands stay English; replies follow the user's language. Natural-language requests work too.

Project setup, synchronization, features, fixes, reviews, documentation, operations and optional releases run through skills, not shell subcommands. See `plugins/core/skills/devkit/references/commands.md`.

## Verify

```bash
phxdk doctor
phxdk status
```

See `docs/INSTALLATION.md`, `docs/PROFILES.md` and `docs/PROJECT-CONFIGURATION.md`.
