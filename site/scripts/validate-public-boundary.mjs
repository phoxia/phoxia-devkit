import { readFile, readdir } from "node:fs/promises";
import { extname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../build/", import.meta.url));
const forbidden = [
  /private devkit/i,
  /private lux/i,
  /phoxia control/i,
  /private rfc/i,
  /organizational monitoring/i,
];

async function files(directory) {
  const result = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) result.push(...(await files(path)));
    else if ([".html", ".js", ".json", ".css"].includes(extname(path)))
      result.push(path);
  }
  return result;
}

for (const path of await files(root)) {
  const text = await readFile(path, "utf8");
  for (const pattern of forbidden) {
    if (pattern.test(text))
      throw new Error(`${path}: public boundary violation ${pattern}`);
  }
}
console.log("Public boundary passed.");
