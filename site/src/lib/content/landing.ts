const commands = Object.freeze([
  "npx @phoxia/devkit init",
  "phxdk doctor",
  "phxdk status",
] as const);
const paths = Object.freeze([
  ".phoxia/project.yaml",
  "AGENTS.md",
  "CLAUDE.md",
  "~/.phoxia-devkit",
] as const);
const workflow = Object.freeze([
  "Initialize",
  "Describe project",
  "Work with AI",
  "Verify",
  "Keep synchronized",
] as const);

export const landingContent = Object.freeze({
  version: "1.0.0",
  installCommand: commands[0],
  targets: Object.freeze(["Claude Code", "Codex"] as const),
  commands,
  paths,
  workflow,
  profiles: Object.freeze([
    "Personal",
    "Work",
    "Phoxia",
    "Specialist",
  ] as const),
  sections: Object.freeze([
    "hero",
    "problem",
    "pipeline",
    "workflow",
    "files-impact",
    "configuration-trust",
    "profiles",
    "install",
  ] as const),
  urls: Object.freeze({
    docs: "/docs",
    quickStart: "/quick-start",
    changelog: "/changelog",
    repository: "https://github.com/phoxia/phoxia-devkit",
  }),
});
