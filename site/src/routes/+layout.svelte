<script lang="ts">
  import "../app.css";
  import favicon from "@phoxia/lux/assets/favicon/favicon.svg?url";
  import manifest from "@phoxia/lux/assets/favicon/site.webmanifest?url";
  import appleTouchIcon from "@phoxia/lux/assets/favicon/apple-touch-icon.png?url";
  import { initLocale } from "$lib/i18n/store.svelte.ts";
  import { initTheme } from "$lib/theme.svelte.ts";

  let { children } = $props();

  $effect(() => {
    initLocale();
    return initTheme();
  });
</script>

<svelte:head>
  <title>Phoxia • Kit</title>
  <meta
    name="description"
    content="Keep AI-assisted development grounded in your project with Phoxia DevKit."
  />
  <link rel="canonical" href="https://kit.phoxia.org/" />
  <link rel="icon" href={favicon} />
  <link rel="manifest" href={manifest} />
  <link rel="apple-touch-icon" href={appleTouchIcon} />
</svelte:head>

{@render children()}
