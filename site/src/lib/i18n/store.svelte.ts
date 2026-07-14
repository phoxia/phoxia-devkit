import { translations, type LocaleCopy } from "./content.ts";
import { DEFAULT_LOCALE, isLocale, type Locale } from "./locales.ts";
import { resolveLocale } from "./resolve.ts";

const STORAGE_KEY = "phoxia-kit-locale-v1";
export const localeState = $state<{ current: Locale }>({
  current: DEFAULT_LOCALE,
});

export function initLocale(): void {
  if (typeof window === "undefined") return;
  let stored: string | null = null;
  try { stored = localStorage.getItem(STORAGE_KEY); } catch { /* storage can be blocked */ }
  localeState.current = resolveLocale(stored, navigator.languages);
  document.documentElement.lang = localeState.current;
}

export function getLocale(): Locale {
  return localeState.current;
}

export function setLocale(locale: string): void {
  if (!isLocale(locale)) return;
  localeState.current = locale;
  try { localStorage.setItem(STORAGE_KEY, locale); } catch { /* preference remains in memory */ }
  if (typeof document !== "undefined") document.documentElement.lang = locale;
}

export function t(): LocaleCopy {
  return translations[localeState.current] ?? translations[DEFAULT_LOCALE];
}
