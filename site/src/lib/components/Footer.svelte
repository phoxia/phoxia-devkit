<script lang="ts">
  import { Github } from "lucide-svelte";
  import luxHappy from "@phoxia/lux/assets/lux/lux-happy.svg?url";
  import { translations } from "$lib/i18n/content.ts";
  import { landingTranslations } from "$lib/i18n/landing.ts";
  import { localeState } from "$lib/i18n/store.svelte.ts";
  let copy = $derived(translations[localeState.current]); let landing = $derived(landingTranslations[localeState.current]);
</script>
<footer><div class="footer-inner"><div class="footer-brand"><div><img src={luxHappy} alt="" /><b>Phoxia DevKit</b></div><p>{landing.footer}</p><small>AGPL-3.0-only · Phoxia</small></div><div><b>{landing.resources}</b><a href="/docs">{copy.docs}</a><a href="/changelog">{copy.changelog}</a><a href="https://github.com/phoxia/phoxia-devkit/blob/main/SECURITY.md">{landing.security}</a><a href="https://github.com/phoxia/phoxia-devkit/issues">{landing.support}</a></div><div><b>{landing.project}</b><a href="https://github.com/phoxia/phoxia-devkit"><Github size={15} /> GitHub</a><a href="https://github.com/phoxia/phoxia-devkit/blob/main/CONTRIBUTING.md">{landing.contributing}</a><a href="https://github.com/phoxia/phoxia-devkit/blob/main/LICENSE">AGPLv3</a></div></div></footer>
