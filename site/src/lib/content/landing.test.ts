import assert from "node:assert/strict";
import test from "node:test";

import { landingContent } from "./landing.ts";

test("uses real public entry points", () => {
  assert.equal(landingContent.installCommand, "npx @phoxia/devkit init");
  assert.deepEqual(landingContent.targets, ["Claude Code", "Codex"]);
  assert.equal(JSON.stringify(landingContent).includes("RFC Vault"), false);
});

test("keeps verified commands, paths, workflows, and URLs immutable", () => {
  assert.deepEqual(landingContent.commands, [
    "npx @phoxia/devkit init",
    "phxdk doctor",
    "phxdk status",
  ]);
  assert.deepEqual(landingContent.paths, [
    ".phoxia/project.yaml",
    "AGENTS.md",
    "CLAUDE.md",
    "~/.phoxia-devkit",
  ]);
  assert.deepEqual(landingContent.workflow, [
    "Initialize",
    "Describe project",
    "Work with AI",
    "Verify",
    "Keep synchronized",
  ]);
  assert.equal(landingContent.urls.docs, "/docs");
  assert.equal(
    landingContent.urls.repository,
    "https://github.com/phoxia/phoxia-devkit",
  );
  assert.equal(Object.isFrozen(landingContent), true);
});

test("keeps the approved twelve-section landing inventory", () => {
  assert.deepEqual(landingContent.sections, [
    "hero",
    "evidence",
    "problem",
    "help",
    "workflow",
    "profiles",
    "generated-files",
    "transparency",
    "setup-modes",
    "trust",
    "newcomer",
    "install",
  ]);
});

test("does not advertise shell commands that the DevKit implements as skills", async () => {
  const source = await import("node:fs/promises").then((fs) => fs.readFile(new URL("../i18n/landing.ts", import.meta.url), "utf8"));
  assert.doesNotMatch(source, /phoxia (use|run)/);
});
