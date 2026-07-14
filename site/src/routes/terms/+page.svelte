<script lang="ts">
  import LegalPage from "$lib/components/LegalPage.svelte";
  import { legalTranslations } from "$lib/i18n/legal.ts";
  import { localeState } from "$lib/i18n/store.svelte.ts";
  let copy = $derived(legalTranslations[localeState.current].terms);
</script>
<svelte:head><title>Phoxia • Terms</title><meta name="description" content="Terms of use for kit.phoxia.org and Phoxia DevKit." /><link rel="canonical" href="https://kit.phoxia.org/terms" /></svelte:head>
<LegalPage {copy} kind="terms" />
