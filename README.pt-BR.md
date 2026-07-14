# Phoxia DevKit 1.0.0

Kit multiperfil de desenvolvimento e governança de software para **Claude Code e Codex**.

## Conteúdo público

Esta distribuição contém:

- perfis Personal, Work, Phoxia e Specialist;
- Agent Skills portáveis;
- plugins e adaptadores de projeto para Claude Code;
- `AGENTS.md`, skills e agentes personalizados para Codex;
- instalação determinística e fluxos contextuais de projeto dentro dos agentes.

## Instalar Claude e Codex juntos

Linux ou macOS:

```bash
./install-linux.sh --targets claude,codex --profiles all
```

Windows PowerShell:

```powershell
.\install-windows.ps1 --targets claude,codex --profiles all
```

O instalador não apaga nem substitui `~/.claude` ou `~/.codex`. Os arquivos gerenciados ficam em `~/.phoxia-devkit`, as skills do Codex em `~/.agents/skills` e os launchers POSIX em `~/.local/bin`.

Launchers gerados:

```text
claude-personal     codex-personal
claude-work         codex-work
claude-phoxia       codex-phoxia
claude-specialist   codex-specialist
```

## Trabalhar em um projeto

```text
$phoxia-devkit project guide
$phoxia-devkit feature start
$phoxia-devkit fix start
$phoxia-devkit review full
$phoxia-devkit mode direct
```

No Claude, use `/phoxia-core:devkit` no lugar de `$phoxia-devkit`. Os comandos ficam em inglês; a resposta acompanha o idioma do usuário. Pedidos em linguagem natural também funcionam.

Inicialização, sincronização, features, fixes, revisões, documentação, operações e releases opcionais acontecem pelas skills, não por subcomandos no shell. Veja `plugins/core/skills/devkit/references/commands.md`.

## Verificar

```bash
phxdk doctor
phxdk status
```

Leia `docs/INSTALLATION.md`, `docs/PROFILES.md` e `docs/PROJECT-CONFIGURATION.md`.
