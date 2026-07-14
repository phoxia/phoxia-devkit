<script lang="ts">
  import { Check, Copy } from "lucide-svelte";
  let { command, label, copy, copiedLabel, failedLabel }: { command: string; label: string; copy: string; copiedLabel: string; failedLabel: string } = $props();
  let copied = $state(false);
  let failed = $state(false);
  async function copyCommand() {
    try {
      await navigator.clipboard.writeText(command);
      copied = true;
      failed = false;
      window.setTimeout(() => (copied = false), 1800);
    } catch {
      failed = true;
    }
  }
</script>
<div class="copy-command">
  <code>{command}</code>
  <button type="button" aria-label={label} onclick={copyCommand}>
    {#if copied}<Check size={15} />{:else}<Copy size={15} />{/if}<span>{copied ? copiedLabel : copy}</span>
  </button>
  <span class="sr-only" role="status" aria-live="polite">{failed ? failedLabel : copied ? copiedLabel : ""}</span>
</div>
