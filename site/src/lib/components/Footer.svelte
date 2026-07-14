<script lang="ts">
  import { Github } from "lucide-svelte";
  import phoxiaGlyph from "@phoxia/lux/assets/brand/phoxia-glyph.svg?url";
  import { translations } from "$lib/i18n/content.ts";
  import { landingTranslations } from "$lib/i18n/landing.ts";
  import { localeState } from "$lib/i18n/store.svelte.ts";
  let copy = $derived(translations[localeState.current]);
  let landing = $derived(landingTranslations[localeState.current]);
</script>

<footer>
  <div class="footer-inner">
    <div class="footer-main">
      <div class="footer-brand">
        <a href="/" class="footer-logo" aria-label={landing.brandHome}><img src={phoxiaGlyph} alt="" /><b>Phoxia DevKit</b></a>
        <p>{landing.footer}</p>
        <small>AGPL-3.0-only · Phoxia</small>
      </div>
      <nav class="footer-nav" aria-label={landing.footerNavigation}>
        <div class="footer-group"><b>{landing.product}</b><a href="/docs">{copy.docs}</a><a href="/quick-start">{landing.quickStart}</a><a href="/changelog">{copy.changelog}</a></div>
        <div class="footer-group"><b>{landing.project}</b><a href="https://github.com/phoxia/phoxia-devkit">GitHub</a><a href="https://github.com/phoxia/phoxia-devkit/blob/main/CONTRIBUTING.md">{landing.contributing}</a><a href="https://github.com/phoxia/phoxia-devkit/blob/main/GOVERNANCE.md">{landing.governance}</a></div>
        <div class="footer-group"><b>{landing.trustSupport}</b><a href="https://github.com/phoxia/phoxia-devkit/blob/main/SECURITY.md">{landing.security}</a><a href="https://github.com/phoxia/phoxia-devkit/issues">{landing.support}</a><a href="https://github.com/phoxia/phoxia-devkit/blob/main/CODE_OF_CONDUCT.md">{landing.codeOfConduct}</a><a href="https://github.com/phoxia/phoxia-devkit/blob/main/LICENSE">AGPLv3</a></div>
      </nav>
    </div>
    <div class="footer-bottom"><span>© {new Date().getFullYear()} Phoxia · AGPL-3.0-only</span><a href="https://github.com/phoxia/phoxia-devkit"><Github size={14} aria-hidden="true" /> GitHub</a></div>
  </div>
</footer>
