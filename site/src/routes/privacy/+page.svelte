<script lang="ts">
  import LegalPage from "$lib/components/LegalPage.svelte";
  import { legalTranslations } from "$lib/i18n/legal.ts";
  import { localeState } from "$lib/i18n/store.svelte.ts";
  let copy = $derived(legalTranslations[localeState.current].privacy);
</script>
<svelte:head><title>Phoxia • Privacy</title><meta name="description" content="Privacy policy for kit.phoxia.org and Phoxia DevKit." /><link rel="canonical" href="https://kit.phoxia.org/privacy" /></svelte:head>
<LegalPage {copy} kind="privacy" />
