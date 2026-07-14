<script lang="ts">
  import { Monitor, Moon, Sun } from "lucide-svelte";
  import luxHappy from "@phoxia/lux/assets/lux/lux-happy.svg?url";
  import { localeNames, translations } from "$lib/i18n/content.ts";
  import { localeState, setLocale } from "$lib/i18n/store.svelte.ts";
  import { getTheme, setTheme } from "$lib/theme.svelte.ts";
  import { landingTranslations } from "$lib/i18n/landing.ts";
  let copy = $derived(translations[localeState.current]);
  let landing = $derived(landingTranslations[localeState.current]);
  const themes = [
    ["light", Sun],
    ["dark", Moon],
    ["system", Monitor],
  ] as const;
</script>
<a class="skip" href="#content">{landing.skip}</a>
<header class="site-header">
  <a class="brand" href="/" aria-label={landing.brandHome}><img src={luxHappy} alt="" /><span>Phoxia <b>DevKit</b></span></a>
  <nav aria-label={landing.primary}><a href="#product">{landing.product}</a><a href="#how">{landing.how}</a><a href="/docs">{copy.docs}</a></nav>
  <div class="header-actions">
    <div class="segmented locale-control" role="group" aria-label={copy.language}>
      <button type="button" aria-label={localeNames["pt-BR"]} aria-pressed={localeState.current === "pt-BR"} onclick={() => setLocale("pt-BR")}>PT</button>
      <button type="button" aria-label={localeNames["en-US"]} aria-pressed={localeState.current === "en-US"} onclick={() => setLocale("en-US")}>EN</button>
    </div>
    <div class="segmented theme-control" role="group" aria-label={copy.theme}>
      {#each themes as [theme, Icon]}
        {@const label = theme === "light" ? copy.light : theme === "dark" ? copy.dark : copy.system}
        <button type="button" title={label} aria-label={`${label} theme`} aria-pressed={getTheme() === theme} onclick={() => setTheme(theme)}><Icon size={16} /></button>
      {/each}
    </div>
  </div>
</header>
