const STORAGE_KEY = "phoxia-kit-theme-v1";
export type Theme = "system" | "light" | "dark";
let current = $state<Theme>("system");
let media: MediaQueryList | undefined;
let listening = false;

function valid(value: unknown): value is Theme {
  return value === "system" || value === "light" || value === "dark";
}
function effective(): "light" | "dark" {
  return current === "system" && media
    ? media.matches
      ? "dark"
      : "light"
    : current === "light"
      ? "light"
      : "dark";
}
function apply(): void {
  if (typeof document !== "undefined")
    document.documentElement.dataset.theme = effective();
}

export function initTheme(): (() => void) | undefined {
  if (typeof window === "undefined") return;
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (valid(stored)) current = stored;
  } catch {
    /* storage can be blocked */
  }
  media ??= window.matchMedia("(prefers-color-scheme: dark)");
  if (!listening) { media.addEventListener("change", apply); listening = true; }
  apply();
  return () => { if (media && listening) media.removeEventListener("change", apply); listening = false; };
}
export function getTheme(): Theme {
  return current;
}
export function setTheme(value: string): void {
  if (!valid(value)) return;
  current = value;
  try {
    localStorage.setItem(STORAGE_KEY, value);
  } catch {
    /* preference remains in memory */
  }
  apply();
}
