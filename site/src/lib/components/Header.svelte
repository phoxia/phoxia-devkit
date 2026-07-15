<script lang="ts">
  import { Globe, Monitor, Moon, Sun } from "lucide-svelte";
  import luxHappy from "@phoxia/lux/assets/lux/lux-happy.svg?url";
  import { localeNames, translations } from "$lib/i18n/content.ts";
  import type { Locale } from "$lib/i18n/locales.ts";
  import { localeState, setLocale } from "$lib/i18n/store.svelte.ts";
  import { getTheme, setTheme } from "$lib/theme.svelte.ts";
  import { landingTranslations } from "$lib/i18n/landing.ts";
  import { onMount } from "svelte";
  let copy = $derived(translations[localeState.current]);
  let landing = $derived(landingTranslations[localeState.current]);
  let theme = $derived(getTheme());
  let currentLocale = $derived<Locale>(localeState.current);

  let themeOpen = $state(false);
  let langOpen = $state(false);

  onMount(() => {
    function closeMenus(e: MouseEvent) {
      if (!(e.target as HTMLElement)?.closest(".menu")) { themeOpen = false; langOpen = false; }
    }
    function onKeydown(e: KeyboardEvent) {
      if (e.key === "Escape") { themeOpen = false; langOpen = false; }
    }
    document.addEventListener("click", closeMenus);
    document.addEventListener("keydown", onKeydown);
    return () => {
      document.removeEventListener("click", closeMenus);
      document.removeEventListener("keydown", onKeydown);
    };
  });
</script>
<a class="skip" href="#content">{landing.skip}</a>
<header class="site-header">
  <a class="brand" href="/" aria-label={landing.brandHome}><img src={luxHappy} alt="" /><span>Phoxia <b>DevKit</b></span></a>
  <nav aria-label={landing.primary}><a href="/#product">{landing.product}</a><a href="/#how">{landing.how}</a><a href="/docs">{copy.docs}</a></nav>
  <div class="header-actions">
    <div class="menu">
      <button class="control-button" type="button" aria-label={`${copy.language}: ${localeNames[currentLocale]}`} aria-expanded={langOpen} onclick={() => { langOpen = !langOpen; themeOpen = false; }}>
        <Globe size={15} aria-hidden="true" />
        <span>{currentLocale === "pt-BR" ? "PT" : "EN"}</span>
      </button>
      {#if langOpen}
        <div class="dropdown">
          <button aria-pressed={currentLocale === "en-US"} onclick={() => { setLocale("en-US"); langOpen = false; }}>English</button>
          <button aria-pressed={currentLocale === "pt-BR"} onclick={() => { setLocale("pt-BR"); langOpen = false; }}>Português</button>
        </div>
      {/if}
    </div>
    <div class="menu">
      <button class="control-button icon-only" type="button" aria-label={`${copy.theme}: ${theme === "light" ? copy.light : theme === "dark" ? copy.dark : copy.system}`} aria-expanded={themeOpen} onclick={() => { themeOpen = !themeOpen; langOpen = false; }}>
        {#if theme === "light"}<Sun size={15} aria-hidden="true" />{:else if theme === "dark"}<Moon size={15} aria-hidden="true" />{:else}<Monitor size={15} aria-hidden="true" />{/if}
      </button>
      {#if themeOpen}
        <div class="dropdown">
          <button aria-pressed={theme === "system"} onclick={() => { setTheme("system"); themeOpen = false; }}><Monitor size={15} aria-hidden="true" />{copy.system}</button>
          <button aria-pressed={theme === "light"} onclick={() => { setTheme("light"); themeOpen = false; }}><Sun size={15} aria-hidden="true" />{copy.light}</button>
          <button aria-pressed={theme === "dark"} onclick={() => { setTheme("dark"); themeOpen = false; }}><Moon size={15} aria-hidden="true" />{copy.dark}</button>
        </div>
      {/if}
    </div>
  </div>
</header>

<style>
  .menu { position: relative; }
  .dropdown {
    position: absolute;
    top: calc(100% + 8px);
    right: 0;
    display: grid;
    min-width: 130px;
    padding: 6px;
    border: 1px solid var(--border);
    border-radius: 10px;
    background: var(--surface);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
    z-index: 50;
  }
  .dropdown button {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 8px;
    min-height: 36px;
    padding: 6px 10px;
    border: 0;
    border-radius: 7px;
    background: transparent;
    color: var(--text);
    font-size: 13px;
    cursor: pointer;
  }
  .dropdown button:hover { background: var(--surface2); }
  .dropdown button[aria-pressed="true"] { background: var(--surface2); }
</style>
