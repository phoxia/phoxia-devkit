<script lang="ts">
  import "../app.css";
  import favicon from "@phoxia/lux/assets/favicon/favicon.svg?url";
  import appleTouchIcon from "@phoxia/lux/assets/favicon/apple-touch-icon.png?url";
  import icon192 from "@phoxia/lux/assets/favicon/icon-192.png?url";
  import icon512 from "@phoxia/lux/assets/favicon/icon-512.png?url";
  import maskable192 from "@phoxia/lux/assets/favicon/maskable-192.png?url";
  import maskable512 from "@phoxia/lux/assets/favicon/maskable-512.png?url";
  import { initLocale } from "$lib/i18n/store.svelte.ts";
  import { initTheme } from "$lib/theme.svelte.ts";

  let { children } = $props();

  const manifest = JSON.stringify({
    name: "Phoxia",
    short_name: "Phoxia",
    description: "Open source, fair revenue, real transparency.",
    start_url: "/",
    display: "standalone",
    background_color: "#080914",
    theme_color: "#080914",
    icons: [
      { src: icon192, sizes: "192x192", type: "image/png", purpose: "any" },
      { src: icon512, sizes: "512x512", type: "image/png", purpose: "any" },
      { src: maskable192, sizes: "192x192", type: "image/png", purpose: "maskable" },
      { src: maskable512, sizes: "512x512", type: "image/png", purpose: "maskable" }
    ]
  });

  const manifestHref = "data:application/manifest+json," + encodeURIComponent(manifest);

  $effect(() => {
    initLocale();
    document.documentElement.dataset.hydrated = "true";
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
  <link rel="manifest" href={manifestHref} />
  <link rel="apple-touch-icon" href={appleTouchIcon} />
</svelte:head>

{@render children()}
