<script lang="ts">
  import { translations } from "$lib/i18n/content.ts";
  import { localeState } from "$lib/i18n/store.svelte.ts";
  let copy = $derived(translations[localeState.current]);
</script>

<svelte:head><title>Phoxia • Changelog</title></svelte:head>
<main><h1>{copy.changelog}</h1></main>
