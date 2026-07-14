<script lang="ts">
  import { Check, ChevronRight, FileCode2, Terminal } from "lucide-svelte";
  import luxConfident from "@phoxia/lux/assets/lux/lux-confident.svg?url";
  let { eyebrow, title, nodes, ariaLabel }: { eyebrow: string; title: string; nodes: readonly (readonly [string, string])[]; ariaLabel: string } = $props();
</script>
<div class="evidence section" aria-labelledby="evidence-title">
  <div class="section-heading"><p class="eyebrow">{eyebrow}</p><h2 id="evidence-title">{title}</h2></div>
  <div class="thread" aria-label={ariaLabel}>
    <article><FileCode2 /><b>{nodes[0][0]}</b><span>{nodes[0][1]}</span></article><ChevronRight class="thread-arrow" />
    <article><Terminal /><b>{nodes[1][0]}</b><span>{nodes[1][1]}</span></article><ChevronRight class="thread-arrow" />
    <article><Check /><b>{nodes[2][0]}</b><span>{nodes[2][1]}</span></article><img src={luxConfident} alt="Lux" />
  </div>
</div>
