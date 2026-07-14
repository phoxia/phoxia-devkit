<script lang="ts">
  import { Github } from "lucide-svelte";
  import luxHappy from "@phoxia/lux/assets/lux/lux-happy.svg?url";
  import { localeNames, translations } from "$lib/i18n/content.ts";
  import { localeState, setLocale } from "$lib/i18n/store.svelte.ts";
  import { SUPPORTED_LOCALES } from "$lib/i18n/locales.ts";
  import { getTheme, setTheme } from "$lib/theme.svelte.ts";
  import { landingTranslations } from "$lib/i18n/landing.ts";
  let copy = $derived(translations[localeState.current]);
  let landing = $derived(landingTranslations[localeState.current]);
</script>
<a class="skip" href="#content">{landing.skip}</a>
<header class="site-header">
  <a class="brand" href="/" aria-label={landing.brandHome}><img src={luxHappy} alt="" /><span>Phoxia <b>DevKit</b></span></a>
  <nav aria-label={landing.primary}><a href="#product">{landing.product}</a><a href="#how">{landing.how}</a><a href="/docs">{copy.docs}</a><a href="/quick-start">{copy.quickStart}</a><a class="optional" href="/changelog">{copy.changelog}</a></nav>
  <div class="header-actions">
    <label class="control"><span class="sr-only">{copy.language}</span><select aria-label={copy.language} value={localeState.current} onchange={(e) => setLocale(e.currentTarget.value)}>{#each SUPPORTED_LOCALES as locale}<option value={locale}>{localeNames[locale]}</option>{/each}</select></label>
    <label class="control"><span class="sr-only">{copy.theme}</span><select aria-label={copy.theme} value={getTheme()} onchange={(e) => setTheme(e.currentTarget.value)}><option value="system">{copy.system}</option><option value="light">{copy.light}</option><option value="dark">{copy.dark}</option></select></label>
    <a class="github optional" href="https://github.com/phoxia/phoxia-devkit"><Github size={17} /><span class="sr-only">GitHub</span></a>
    <a class="button small" href="#install">{copy.getStarted}</a>
  </div>
</header>
