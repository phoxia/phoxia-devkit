export const SUPPORTED_LOCALES = ["en-US", "pt-BR"] as const;

export type Locale = (typeof SUPPORTED_LOCALES)[number];
export const DEFAULT_LOCALE: Locale = "en-US";

export function canonicalLocale(value: string): Locale | null {
  return (
    SUPPORTED_LOCALES.find(
      (locale) => locale.toLowerCase() === value.toLowerCase(),
    ) ?? null
  );
}

export function isLocale(value: string): value is Locale {
  return canonicalLocale(value) !== null;
}
