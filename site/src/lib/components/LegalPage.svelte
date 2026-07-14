<script lang="ts">
  import { Scale, ShieldCheck } from "lucide-svelte";
  import Header from "$lib/components/Header.svelte";
  import Footer from "$lib/components/Footer.svelte";
  import type { LegalPageCopy } from "$lib/i18n/legal.ts";

  let { copy, kind }: { copy: LegalPageCopy; kind: "privacy" | "terms" } = $props();
  let Icon = $derived(kind === "privacy" ? ShieldCheck : Scale);
</script>

<Header />
<main id="content" class="legal-page">
  <header class="legal-header">
    <Icon size={22} aria-hidden="true" />
    <div><h1>{copy.title}</h1><p>{copy.updated}</p><strong>{copy.status}</strong></div>
  </header>
  <div class="legal-layout">
    <nav class="legal-toc" aria-label={copy.contents}>
      <b>{copy.contents}</b>
      {#each copy.sections as section}
        <a href={`#${section.id}`}>{section.title}</a>
      {/each}
    </nav>
    <div class="legal-content">
      {#each copy.sections as section}
        <section id={section.id} class="legal-section">
          <h2>{section.title}</h2>
          <p>{section.content}</p>
        </section>
      {/each}
    </div>
  </div>
</main>
<Footer />

<style>
  .legal-page { max-width: 1120px; min-height: 70vh; margin: auto; padding: 64px 24px 96px; }
  .legal-header { max-width: 760px; margin: 0 auto 40px; display: flex; align-items: flex-start; gap: 14px; }
  .legal-header :global(svg) { flex: none; margin-top: 5px; color: var(--amber); }
  .legal-header h1 { margin: 0; font-size: clamp(30px, 4vw, 44px); line-height: 1.1; }
  .legal-header p { margin: 10px 0 4px; color: var(--muted); font: 11px "JetBrains Mono", monospace; }
  .legal-header strong { color: var(--amber); font: 600 10px "JetBrains Mono", monospace; text-transform: uppercase; letter-spacing: .08em; }
  .legal-layout { display: grid; grid-template-columns: 240px minmax(0, 760px); justify-content: center; gap: 48px; }
  .legal-toc { position: sticky; top: 24px; align-self: start; display: flex; flex-direction: column; gap: 8px; }
  .legal-toc b { margin-bottom: 4px; font: 600 10px "JetBrains Mono", monospace; text-transform: uppercase; letter-spacing: .08em; }
  .legal-toc a { min-height: 0; padding: 0; border-radius: 0; color: var(--muted); background: transparent; font-size: 12px; line-height: 1.45; }
  .legal-toc a:hover { color: var(--text); background: transparent; }
  .legal-section { padding: 0 0 32px; margin: 0 0 32px; border-bottom: 1px solid var(--border); scroll-margin-top: 24px; }
  .legal-section:last-child { margin-bottom: 0; }
  .legal-section h2 { margin: 0 0 14px; font-size: 19px; }
  .legal-section p { margin: 0; color: var(--muted); white-space: pre-line; }
  @media (max-width: 800px) { .legal-layout { grid-template-columns: 1fr; gap: 32px; } .legal-toc { position: static; } }
</style>
