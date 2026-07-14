<script lang="ts">
  import { Languages, Monitor, Moon, Sun } from "lucide-svelte";
  import luxHappy from "@phoxia/lux/assets/lux/lux-happy.svg?url";
  import { localeNames, translations } from "$lib/i18n/content.ts";
  import type { Locale } from "$lib/i18n/locales.ts";
  import { localeState, setLocale } from "$lib/i18n/store.svelte.ts";
  import { getTheme, setTheme } from "$lib/theme.svelte.ts";
  import { landingTranslations } from "$lib/i18n/landing.ts";
  let copy = $derived(translations[localeState.current]);
  let landing = $derived(landingTranslations[localeState.current]);
  let theme = $derived(getTheme());
  let nextLocale = $derived<Locale>(localeState.current === "en-US" ? "pt-BR" : "en-US");
  let ThemeIcon = $derived(theme === "dark" ? Sun : theme === "light" ? Moon : Monitor);
  let themeLabel = $derived(theme === "light" ? copy.light : theme === "dark" ? copy.dark : copy.system);

  function cycleTheme() {
    setTheme(theme === "system" ? "dark" : theme === "dark" ? "light" : "system");
  }
</script>
<a class="skip" href="#content">{landing.skip}</a>
<header class="site-header">
  <a class="brand" href="/" aria-label={landing.brandHome}><img src={luxHappy} alt="" /><span>Phoxia <b>DevKit</b></span></a>
  <nav aria-label={landing.primary}><a href="/#product">{landing.product}</a><a href="/#how">{landing.how}</a><a href="/docs">{copy.docs}</a></nav>
  <div class="header-actions">
    <button class="control-button" type="button" title={`${copy.language}: ${localeNames[nextLocale]}`} aria-label={`${copy.language}: ${localeNames[nextLocale]}`} onclick={() => setLocale(nextLocale)}><Languages size={15} aria-hidden="true" /><span>{nextLocale === "pt-BR" ? "PT" : "EN"}</span></button>
    <button class="control-button icon-only" type="button" title={`${copy.theme}: ${themeLabel}`} aria-label={`${copy.theme}: ${themeLabel}`} onclick={cycleTheme}><ThemeIcon size={15} aria-hidden="true" /></button>
  </div>
</header>
