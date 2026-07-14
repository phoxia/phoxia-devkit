#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

export function run(args = process.argv.slice(2), options = {}) {
  const nodeVersion = options.nodeVersion ?? process.versions.node;
  if (Number.parseInt(nodeVersion, 10) < 20) {
    console.error(`Phoxia DevKit requires Node.js 20 or newer. Current version: ${nodeVersion}.`);
    return 1;
  }
  const spawn = options.spawnSync ?? spawnSync;
  const engine = resolve(dirname(fileURLToPath(import.meta.url)), "../tools/phoxia_devkit.py");
  const candidates = process.platform === "win32" ? ["py", "python"] : ["python3", "python"];
  for (const python of candidates) {
    const result = spawn(python, [engine, ...args], { stdio: "inherit" });
    if (!result.error) return result.status ?? 1;
  }
  console.error("Phoxia DevKit requires Python 3. Install Python 3 and run this command again.");
  return 127;
}
if (process.argv[1] === fileURLToPath(import.meta.url)) process.exitCode = run();
