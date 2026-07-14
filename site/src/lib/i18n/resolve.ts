import { canonicalLocale, DEFAULT_LOCALE, type Locale } from "./locales.ts";

function compatibleLocale(value: string): Locale | null {
  const exact = canonicalLocale(value);
  if (exact) return exact;
  const base = value.toLowerCase().split("-", 1)[0];
  if (base === "en") return "en-US";
  if (base === "pt") return "pt-BR";
  return null;
}

export function resolveLocale(
  stored: string | null,
  preferred: readonly string[],
): Locale {
  const saved = stored && compatibleLocale(stored);
  if (saved) return saved;
  for (const candidate of preferred) {
    const locale = compatibleLocale(candidate);
    if (locale) return locale;
  }
  return DEFAULT_LOCALE;
}
