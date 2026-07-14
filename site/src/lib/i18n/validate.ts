const TECHNICAL_TOKENS = [
  "Phoxia DevKit",
  "Claude Code",
  "Codex",
  ".phoxia/project.yaml",
  "AGENTS.md",
  "CLAUDE.md",
];

function leaves(value: unknown, prefix = ""): Map<string, string> {
  const result = new Map<string, string>();
  if (!value || typeof value !== "object" || Array.isArray(value))
    return result;
  for (const [key, child] of Object.entries(value)) {
    const path = prefix ? `${prefix}.${key}` : key;
    if (typeof child === "string") result.set(path, child);
    else
      for (const [nested, text] of leaves(child, path))
        result.set(nested, text);
  }
  return result;
}

export function validateLocaleSet(locales: Record<string, unknown>): void {
  const canonical = leaves(locales["en-US"]);
  if (!canonical.size)
    throw new Error("en-US: canonical locale is missing or empty");
  for (const [locale, value] of Object.entries(locales)) {
    const translated = leaves(value);
    for (const [path, source] of canonical) {
      const target = translated.get(path);
      if (target === undefined) throw new Error(`${locale}: missing ${path}`);
      for (const token of TECHNICAL_TOKENS) {
        if (source.includes(token) && !target.includes(token)) {
          throw new Error(`${locale}: ${path} must preserve ${token}`);
        }
      }
    }
    for (const path of translated.keys()) {
      if (!canonical.has(path))
        throw new Error(`${locale}: unexpected ${path}`);
    }
  }
}
