# FEAT-0001: Safe project initialization

Status: implemented

`phxdk init` configures Claude Code and Codex project context using add, update or replace modes. It previews file impact, requires confirmation unless explicitly automated, preserves user text outside managed blocks and backs up modified files under `.phoxia/backups/`.
