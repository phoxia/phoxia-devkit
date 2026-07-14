<script lang="ts">
  import { translations } from "$lib/i18n/content.ts";
  import { localeState } from "$lib/i18n/store.svelte.ts";
  let copy = $derived(translations[localeState.current]);
</script>

<svelte:head><title>Phoxia • Quick Start</title></svelte:head>
<main><h1>{copy.quickStart}</h1></main>
