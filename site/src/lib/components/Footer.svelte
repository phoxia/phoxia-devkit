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
      </div>
      <nav class="footer-nav" aria-label={landing.footerNavigation}>
        <div class="footer-group"><b>{landing.product}</b><a href="/docs">{copy.docs}</a><a href="/quick-start">{landing.quickStart}</a><a href="/changelog">{copy.changelog}</a></div>
        <div class="footer-group"><b>{landing.project}</b><a href="https://github.com/phoxia/phoxia-devkit">GitHub</a><a href="https://github.com/phoxia/phoxia-devkit/blob/main/CONTRIBUTING.md">{landing.contributing}</a><a href="https://github.com/phoxia/phoxia-devkit/blob/main/GOVERNANCE.md">{landing.governance}</a></div>
        <div class="footer-group"><b>{landing.trustSupport}</b><a href="https://github.com/phoxia/phoxia-devkit/blob/main/SECURITY.md">{landing.security}</a><a href="https://github.com/phoxia/phoxia-devkit/issues">{landing.support}</a><a href="https://github.com/phoxia/phoxia-devkit/blob/main/CODE_OF_CONDUCT.md">{landing.codeOfConduct}</a><a href="https://github.com/phoxia/phoxia-devkit/blob/main/LICENSE">AGPLv3</a></div>
      </nav>
    </div>
    <div class="footer-bottom">
      <span>© {new Date().getFullYear()} Phoxia · AGPLv3 · <a href="https://www.phoxia.org/">phoxia.org</a></span>
      <div class="footer-external">
        <a href="https://discord.gg/HD2p367Zb5" aria-label="Phoxia on Discord">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057c.002.022.015.043.03.056a19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128c.126-.094.252-.192.372-.292a.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.1.246.198.373.292a.077.077 0 0 1-.006.127 12.3 12.3 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z" />
          </svg>
          Discord
        </a>
        <a href="https://github.com/phoxia/phoxia-devkit" aria-label="Phoxia DevKit on GitHub"><Github size={14} aria-hidden="true" /> GitHub</a>
      </div>
    </div>
  </div>
</footer>
