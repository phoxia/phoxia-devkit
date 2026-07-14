# Phoxia DevKit Landing Pipeline Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the repetitive twelve-section landing with an eight-section product pipeline, distinctive information components and one accessible animated workflow.

**Architecture:** Keep the landing in the existing Svelte route and reuse `EvidenceThread.svelte` as the focused pipeline component. Consolidate duplicated copy and section inventory in the existing content modules, then use semantic route markup plus native CSS Grid and keyframes for layout and motion.

**Tech Stack:** Svelte 5, TypeScript, native CSS, `lucide-svelte`, Node test runner and Playwright.

## Global Constraints

- Use existing Svelte components, `lucide-svelte`, native CSS Grid and CSS animations.
- Add no dependencies and no generic card abstraction.
- Preserve commands, paths, target names, setup-mode behavior, URLs, locale/theme stores, header, footer, terminal sequence and installation behavior.
- Preserve English and Brazilian Portuguese coverage.
- Keep 44 px interactive targets, keyboard focus, theme contrast and `prefers-reduced-motion` support.
- Avoid horizontal overflow at 390 px.

---

### Task 1: Consolidate the landing information architecture

**Files:**
- Modify: `site/src/lib/content/landing.test.ts`
- Modify: `site/src/lib/content/landing.ts`
- Modify: `site/src/lib/i18n/landing.ts`
- Modify: `site/src/routes/+page.svelte`
- Modify: `site/tests/e2e/landing.spec.ts`

**Interfaces:**
- Consumes: immutable `landingContent.commands`, `paths`, `workflow`, `profiles` and `urls`.
- Produces: `landingContent.sections` with exactly `hero`, `problem`, `pipeline`, `workflow`, `files-impact`, `configuration-trust`, `profiles`, `install`.

- [ ] **Step 1: Change the unit test to require the eight-section inventory**

Replace the current inventory assertion with:

```ts
test("keeps the approved eight-section landing inventory", () => {
  assert.deepEqual(landingContent.sections, [
    "hero",
    "problem",
    "pipeline",
    "workflow",
    "files-impact",
    "configuration-trust",
    "profiles",
    "install",
  ]);
});
```

- [ ] **Step 2: Change the browser hierarchy test to require eight sections and removed duplication**

In `site/tests/e2e/landing.spec.ts`, replace the twelve-section test count and add these assertions:

```ts
await expect(page.locator("main > section[data-section]")).toHaveCount(8);
await expect(page.locator('[data-section="pipeline"]')).toHaveCount(1);
await expect(page.locator('[data-section="files-impact"]')).toHaveCount(1);
await expect(page.locator('[data-section="configuration-trust"]')).toHaveCount(1);
await expect(page.locator('[data-section="newcomer"]')).toHaveCount(0);
```

- [ ] **Step 3: Run the two tests and verify RED**

Run:

```bash
cd site
node --test src/lib/content/landing.test.ts
npx playwright test tests/e2e/landing.spec.ts --project=desktop-1440
```

Expected: the unit test reports the old twelve-section inventory and Playwright reports twelve sections with no consolidated section identifiers.

- [ ] **Step 4: Update the immutable section inventory**

Set `landingContent.sections` to:

```ts
sections: Object.freeze([
  "hero",
  "problem",
  "pipeline",
  "workflow",
  "files-impact",
  "configuration-trust",
  "profiles",
  "install",
] as const),
```

- [ ] **Step 5: Consolidate localized copy without changing public tokens**

Keep `problemCards`, `evidenceNodes`, `modeCards`, `trustCards`, `impact` and `profileCards`. Rename the former evidence headings to pipeline headings in both locales:

```ts
pipeline: "THE DEVKIT PIPELINE",
pipelineTitle: "From project context to a change you can verify.",
```

```ts
pipeline: "O PIPELINE DO DEVKIT",
pipelineTitle: "Do contexto do projeto a uma mudança que você pode verificar.",
```

Remove only `help`, `helpTitle`, `helpText`, `newcomer`, `newcomerTitle` and `newcomerSteps`, because those sections are merged or deleted. Add combined headings:

```ts
filesImpact: "FILES & REPOSITORY IMPACT",
filesImpactTitle: "Plain files and an explicit change set. Nothing hidden.",
configurationTrust: "CONFIGURATION & TRUST",
configurationTrustTitle: "Safe setup modes, executed locally on your terms.",
```

and their Brazilian Portuguese equivalents:

```ts
filesImpact: "ARQUIVOS E IMPACTO NO REPOSITÓRIO",
filesImpactTitle: "Arquivos simples e um conjunto explícito de mudanças. Nada oculto.",
configurationTrust: "CONFIGURAÇÃO E CONFIANÇA",
configurationTrustTitle: "Modos seguros, executados localmente nos seus termos.",
```

- [ ] **Step 6: Replace the route's twelve sections with the approved eight**

Keep the current hero and install sections. Order the middle route markup as:

```svelte
<section data-section="problem" class="section problem-section">…</section>
<section data-section="pipeline" id="product" class="wrapper">
  <EvidenceThread eyebrow={copy.pipeline} title={copy.pipelineTitle} nodes={copy.evidenceNodes} ariaLabel={copy.evidenceAria} />
</section>
<section data-section="workflow" id="how" class="section workflow-section">…</section>
<section data-section="files-impact" class="section files-impact-section">…</section>
<section data-section="configuration-trust" class="section configuration-trust-section">…</section>
<section data-section="profiles" class="section profiles-section">…</section>
```

Move the existing generated-file cards, verification output and impact list inside `files-impact`. Move setup modes and trust facts inside `configuration-trust`. Delete the old evidence, help, generated-files, transparency, setup-modes, trust and newcomer section wrappers.

- [ ] **Step 7: Run unit, locale and focused desktop tests and verify GREEN**

Run:

```bash
cd site
npm test
npm run validate:locales
npx playwright test tests/e2e/landing.spec.ts --project=desktop-1440
```

Expected: all commands exit 0 and the landing exposes exactly eight sections.

- [ ] **Step 8: Commit the structural consolidation**

```bash
git add site/src/lib/content/landing.test.ts site/src/lib/content/landing.ts site/src/lib/i18n/landing.ts site/src/routes/+page.svelte site/tests/e2e/landing.spec.ts
git commit -m "refactor(site): consolidate landing product narrative"
```

---

### Task 2: Give each content family a distinct semantic component treatment

**Files:**
- Modify: `site/src/lib/components/EvidenceThread.svelte`
- Modify: `site/src/routes/+page.svelte`
- Modify: `site/src/app.css`
- Modify: `site/tests/e2e/landing.spec.ts`

**Interfaces:**
- Consumes: the arrays retained in Task 1 and existing `@phoxia/lux` asset URLs.
- Produces: `.problem-card`, `.pipeline`, `.file-card`, `.impact-card`, `.mode-card`, `.trust-fact` and `.profile-strip` semantic treatments.

- [ ] **Step 1: Add failing structural assertions for icons, pipeline and impact layout**

Add one Playwright test:

```ts
test("uses distinct product components instead of a repeated card grid", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator(".problem-card > .icon-tile")).toHaveCount(4);
  await expect(page.locator(".pipeline-node")).toHaveCount(3);
  await expect(page.locator(".file-card")).toHaveCount(3);
  await expect(page.locator(".impact-card")).toHaveCount(5);
  await expect(page.locator(".mode-card")).toHaveCount(3);
  await expect(page.locator(".trust-fact")).toHaveCount(3);
  await expect(page.locator(".profile-strip")).toHaveCount(1);
});
```

- [ ] **Step 2: Run the new test and verify RED**

Run:

```bash
cd site
npx playwright test tests/e2e/landing.spec.ts --project=desktop-1440 -g "distinct product components"
```

Expected: every new class count is zero.

- [ ] **Step 3: Add existing Lucide icons directly to semantic markup**

Extend the route import with:

```ts
import {
  ArrowRight,
  BadgeAlert,
  BrainCircuit,
  Braces,
  Check,
  FileWarning,
  Github,
  HardDrive,
  LockKeyhole,
  UserCheck,
} from "lucide-svelte";

const problemIcons = [BrainCircuit, Braces, FileWarning, BadgeAlert] as const;
const trustIcons = [HardDrive, LockKeyhole, UserCheck] as const;
```

Render problem cards with their indexed icon component and `aria-hidden="true"`. Render trust facts as a list using `trustIcons`. Give Add the `.recommended` class; do not add click handlers or button roles to setup modes.

- [ ] **Step 4: Refocus `EvidenceThread.svelte` as the connected pipeline**

Keep its public props unchanged. Replace `.thread` markup with:

```svelte
<div class="pipeline" aria-label={ariaLabel}>
  <article class="pipeline-node"><FileCode2 aria-hidden="true" /><b>{nodes[0][0]}</b><code>{nodes[0][1]}</code></article>
  <ChevronRight class="pipeline-arrow" aria-hidden="true" />
  <article class="pipeline-node"><Terminal aria-hidden="true" /><b>{nodes[1][0]}</b><span>{nodes[1][1]}</span></article>
  <ChevronRight class="pipeline-arrow" aria-hidden="true" />
  <article class="pipeline-node"><Check aria-hidden="true" /><b>{nodes[2][0]}</b><span>{nodes[2][1]}</span></article>
  <img src={luxConfident} alt="" />
</div>
```

- [ ] **Step 5: Replace generic card CSS with the minimum distinct treatments**

Implement:

```css
.section-heading-row { width: 100%; max-width: none; }
.problem-cards { grid-template-columns: repeat(4, 1fr); margin-top: 32px; }
.problem-card { padding: 22px; border: 1px solid var(--border); border-radius: 14px; background: var(--surface); }
.icon-tile { width: 38px; height: 38px; display: grid; place-items: center; margin-bottom: 28px; border-radius: 9px; background: var(--surface2); color: var(--amber); }
.pipeline { display: grid; grid-template-columns: 1fr auto 1fr auto 1fr 72px; align-items: stretch; gap: 14px; margin-top: 42px; }
.pipeline-node { min-height: 150px; display: flex; flex-direction: column; justify-content: space-between; padding: 22px; border: 1px solid var(--border); border-radius: 14px; background: var(--surface); }
.file-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.file-card { overflow: hidden; border: 1px solid var(--border); border-radius: 12px; background: var(--surface); }
.file-card > code { display: block; padding: 12px 16px; border-bottom: 1px solid var(--border); color: var(--violet); }
.impact { grid-template-columns: repeat(6, 1fr); }
.impact-card { grid-column: span 2; }
.impact-card:nth-child(n + 4) { grid-column: span 3; }
.trust-list { display: grid; gap: 0; border-block: 1px solid var(--border); }
.trust-fact { display: grid; grid-template-columns: 44px minmax(180px, .7fr) 1fr; gap: 18px; align-items: center; padding: 20px 0; border-bottom: 1px solid var(--border); }
.trust-fact:last-child { border-bottom: 0; }
.profile-strip { display: grid; grid-template-columns: 1fr 1fr auto; gap: 24px; align-items: center; padding: 22px; border: 1px solid var(--border); border-radius: 14px; background: var(--surface); }
```

Delete selectors whose only callers were the removed `.source`, `.newcomer` and generic evidence `.thread` markup.

- [ ] **Step 6: Run the focused test and verify GREEN**

Run:

```bash
cd site
npx playwright test tests/e2e/landing.spec.ts --project=desktop-1440 -g "distinct product components"
```

Expected: one test passes with all semantic component counts.

- [ ] **Step 7: Commit the component redesign**

```bash
git add site/src/lib/components/EvidenceThread.svelte site/src/routes/+page.svelte site/src/app.css site/tests/e2e/landing.spec.ts
git commit -m "feat(site): differentiate landing product components"
```

---

### Task 3: Build the animated responsive workflow timeline

**Files:**
- Modify: `site/src/routes/+page.svelte`
- Modify: `site/src/app.css`
- Modify: `site/tests/e2e/landing.spec.ts`

**Interfaces:**
- Consumes: the five immutable `landingContent.workflow` entries.
- Produces: `.workflow-timeline`, `.timeline-progress`, five `.timeline-step` elements and reduced-motion final state.

- [ ] **Step 1: Add failing timeline and reduced-motion assertions**

Add:

```ts
test("renders an ordered animated workflow with an accessible reduced-motion state", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator(".workflow-timeline")).toHaveCount(1);
  await expect(page.locator(".timeline-step")).toHaveCount(5);
  await expect(page.locator(".timeline-progress")).toHaveCount(1);
});

test("stops workflow motion when reduced motion is requested", async ({ page }) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/");
  await expect(page.locator(".timeline-progress")).toHaveCSS("animation-name", "none");
  for (const step of await page.locator(".timeline-step").all())
    await expect(step).toHaveCSS("opacity", "1");
});
```

- [ ] **Step 2: Run the timeline tests and verify RED**

Run:

```bash
cd site
npx playwright test tests/e2e/landing.spec.ts --project=desktop-1440 -g "workflow|workflow motion"
```

Expected: timeline class counts are zero.

- [ ] **Step 3: Implement semantic timeline markup**

Replace the current `.steps` list with:

```svelte
<ol class="workflow-timeline">
  <i class="timeline-track" aria-hidden="true"></i>
  <i class="timeline-progress" aria-hidden="true"></i>
  {#each landingContent.workflow as step, i}
    <li class="timeline-step" style={`--step:${i}`}>
      <span>{i + 1}</span>
      <h3>{localeState.current === "pt-BR" ? ["Inicializar", "Descrever projeto", "Trabalhar com IA", "Verificar", "Manter sincronizado"][i] : step}</h3>
    </li>
  {/each}
</ol>
```

- [ ] **Step 4: Implement one CSS timeline animation**

Use a 7-second sequence and a delayed node pulse:

```css
.workflow-timeline { position: relative; display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; list-style: none; margin: 48px 0 0; padding: 0; }
.timeline-track, .timeline-progress { position: absolute; top: 14px; left: 10%; right: 10%; height: 2px; }
.timeline-track { background: var(--border-strong); }
.timeline-progress { right: auto; width: 80%; transform: scaleX(0); transform-origin: left; background: linear-gradient(90deg, var(--amber), var(--violet)); animation: timeline-travel 7s ease-in-out infinite; }
.timeline-step { position: relative; text-align: center; opacity: .58; animation: timeline-step-pulse 7s ease-in-out infinite; animation-delay: calc(var(--step) * 1.05s); }
.timeline-step > span { position: relative; z-index: 1; width: 30px; height: 30px; display: grid; place-items: center; margin: 0 auto 20px; border: 2px solid var(--border-strong); border-radius: 50%; background: var(--bg); font: 11px "JetBrains Mono", monospace; }
@keyframes timeline-travel { 0%, 8% { transform: scaleX(0); } 78%, 100% { transform: scaleX(1); } }
@keyframes timeline-step-pulse { 0%, 12%, 100% { opacity: .58; } 18%, 42% { opacity: 1; } }
```

At `max-width: 600px`, make the grid one column, move the track to the left and animate `scaleY` from top to bottom. In reduced motion, set `.timeline-progress { animation: none; transform: scaleX(1); }` and `.timeline-step { animation: none; opacity: 1; }`; use `scaleY(1)` on mobile.

- [ ] **Step 5: Run timeline tests in all viewports and verify GREEN**

Run:

```bash
cd site
npx playwright test tests/e2e/landing.spec.ts -g "workflow|workflow motion"
```

Expected: timeline and reduced-motion tests pass at 1440, 768 and 390 px.

- [ ] **Step 6: Commit the timeline**

```bash
git add site/src/routes/+page.svelte site/src/app.css site/tests/e2e/landing.spec.ts
git commit -m "feat(site): animate the workflow timeline"
```

---

### Task 4: Verify responsive polish and package evidence

**Files:**
- Modify: `site/src/app.css`
- Modify: `site/tests/e2e/landing.spec.ts`
- Modify: `CHANGELOG.md`
- Regenerate: `MANIFEST.json`
- Regenerate: `SHA256SUMS.txt`

**Interfaces:**
- Consumes: all markup and classes produced by Tasks 1–3.
- Produces: verified desktop, tablet and mobile layouts plus current package evidence.

- [ ] **Step 1: Add responsive layout assertions**

Add a test that inspects the final computed layout:

```ts
test("fills repository impact rows and avoids mobile overflow", async ({ page }, testInfo) => {
  await page.goto("/");
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
  expect(overflow).toBe(false);
  if (testInfo.project.name === "desktop-1440") {
    const boxes = await page.locator(".impact-card").evaluateAll((items) => items.map((item) => item.getBoundingClientRect()));
    expect(boxes[0].width).toBeCloseTo(boxes[1].width, 0);
    expect(boxes[3].width).toBeGreaterThan(boxes[0].width);
    expect(boxes[4].width).toBeCloseTo(boxes[3].width, 0);
  }
});
```

- [ ] **Step 2: Run the responsive test and correct only evidenced layout failures**

Run:

```bash
cd site
npx playwright test tests/e2e/landing.spec.ts -g "repository impact"
```

Expected: the test passes at 1440, 768 and 390 px. If it fails, adjust only the affected media query in `site/src/app.css`; do not create JavaScript layout logic.

- [ ] **Step 3: Run full site verification**

```bash
cd site
npm test
npm run check
npm run build
npm run validate:locales
npm run validate:public
npm run test:e2e
```

Expected: all commands exit 0, Svelte reports zero diagnostics and all Playwright projects pass.

- [ ] **Step 4: Inspect screenshots at the contract viewports**

Start the production preview and capture full-page screenshots at 1440×900, 768×1024 and 390×844 in both themes. Verify: Lux reaches the problem heading's right edge; problem icons are visible; the pipeline reads in order; impact uses `3 + 2` on desktop; mobile timeline is vertical; footer and header remain unchanged.

- [ ] **Step 5: Update changelog and package evidence**

Add under `Unreleased`:

```md
- Consolidated the Kit landing into an eight-section product pipeline with distinct problem, file, impact, configuration and trust treatments.
- Added an accessible responsive workflow timeline and reduced-motion fallback.
```

Then run:

```bash
python3 tools/package_manifest.py . @phoxia/devkit 1.0.1
python3 tools/package_manifest.py --check . @phoxia/devkit 1.0.1
python3 -m unittest discover -s tests -v
npm pack --dry-run
git diff --check
```

Expected: 18 Python tests pass, package metadata is current, dry-run packaging succeeds and the diff has no whitespace errors.

- [ ] **Step 6: Commit the verified redesign**

```bash
git add CHANGELOG.md MANIFEST.json SHA256SUMS.txt site/src/app.css site/tests/e2e/landing.spec.ts
git commit -m "chore(site): verify landing pipeline redesign"
```
