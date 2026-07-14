# Multi-agent architecture

## Source of truth

The package keeps one set of engineering workflows and generates target-specific adapters at installation or project initialization time.

```text
profile manifests
skills and references
Claude agent definitions
        ↓
Claude Code plugins and project skills
Codex AGENTS.md, Agent Skills and TOML agents
```

## Profiles

A profile defines standing instructions, enabled plugins, skills, agents and default project-classification values.

The public profiles are Personal, Work, Phoxia and Specialist.

## User installation

The installer creates isolated homes under `~/.phoxia-devkit/profiles` and launchers that set `CLAUDE_CONFIG_DIR` or `CODEX_HOME`. Existing default homes are not replaced.

## Project installation

`project init` writes only a marked managed block into `CLAUDE.md` and `AGENTS.md`. Text outside the block remains owned by the repository.

Selected skills are vendored into `.claude/skills` and `.agents/skills`. Claude agents are written to `.claude/agents`; Codex agents are converted to `.codex/agents/*.toml`.

## Workspace installation

`workspace init --recursive` detects nested Git roots and configures each repository independently. This is required when the parent folder is not itself the Git root used by an agent.

## Extensibility

Optional private or organization-specific behavior is packaged as a layer manifest. A layer may add instructions, a Claude plugin, skills and agents without changing the public core.
