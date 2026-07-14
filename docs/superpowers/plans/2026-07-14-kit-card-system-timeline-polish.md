# Phoxia DevKit Card System and Timeline Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove speculative community publishing and establish a stronger technical-surface, hover, verification and timeline system.

**Architecture:** Keep the route and translation modules intact, deleting only obsolete profile data. Use semantic nested markup for preset/workflow cells and verification rows, then implement all interaction with existing native CSS and Lucide icons.

**Tech Stack:** Svelte 5, TypeScript, native CSS, `lucide-svelte`, Node test runner and Playwright.

## Global Constraints

- Add no dependencies, generic card component or JavaScript animation.
- Preserve locale, theme, header, footer, terminal and installation behavior.
- Content remains understandable without hover.
- Hover transforms apply only to hover-capable pointers.
- Reduced motion removes elevation, timeline travel and pulsing.
- No horizontal overflow at 390 px.

---

### Task 1: Replace speculative publishing with useful profile grids

**Files:**
- Modify: `site/src/lib/i18n/landing.ts`
- Modify: `site/src/routes/+page.svelte`
- Modify: `site/src/app.css`
- Modify: `site/tests/e2e/landing.spec.ts`

**Interfaces:**
- Consumes: exact profile and workflow paths already present in localized copy.
- Produces: `.profile-panel`, four `.preset-cell` items and two `.workflow-cell` items.

- [ ] Write a failing Playwright test asserting two profile panels, four preset cells, two workflow cells and no `Community publishing` or `# coming soon` text.
- [ ] Run `cd site && npx playwright test tests/e2e/landing.spec.ts --project=desktop-1440 -g "profile paths"`; expect the old third profile article and zero nested cells.
- [ ] Change `profileCards` in both locales from three tuples to two objects represented by the existing tuple shape: Official presets and Run a workflow. Store preset paths as `profiles/personal · profiles/work · profiles/phoxia · profiles/specialist` and workflow paths as `~/.agents/skills/phoxia-dev · /phoxia-core:devkit`.
- [ ] In `+page.svelte`, split each path string on ` · ` and render:

```svelte
<div class="profile-panels">
  <article class="profile-panel presets-panel">
    <h3>{copy.profileCards[0][0]}</h3><p>{copy.profileCards[0][1]}</p>
    <div class="preset-grid">{#each copy.profileCards[0][2].split(" · ") as path}<code class="preset-cell">{path}</code>{/each}</div>
  </article>
  <article class="profile-panel workflows-panel">
    <h3>{copy.profileCards[1][0]}</h3><p>{copy.profileCards[1][1]}</p>
    <div class="workflow-grid">{#each copy.profileCards[1][2].split(" · ") as path}<code class="workflow-cell">{path}</code>{/each}</div>
  </article>
</div>
```

- [ ] Style `.profile-panels` as two equal columns, `.preset-grid` as `2 × 2` at every viewport and `.workflow-grid` as two equal rows. Stack only the top-level panels below 600 px.
- [ ] Run the focused test and `npm run validate:locales`; expect both to pass.

---

### Task 2: Apply the technical-surface system and rebuild verification output

**Files:**
- Modify: `site/src/routes/+page.svelte`
- Modify: `site/src/app.css`
- Modify: `site/tests/e2e/landing.spec.ts`

**Interfaces:**
- Consumes: existing problem, file, impact and mode articles plus `phxdk doctor` and `phxdk status`.
- Produces: shared theme-aware hover foundation and `.verification-terminal` with two `.verification-row` elements.

- [ ] Add failing browser assertions for two verification rows and both exact commands.
- [ ] Run the focused test; expect `.verification-terminal` and `.verification-row` counts to be zero.
- [ ] Import `Check` in the route and replace `.verify` with:

```svelte
<div class="verification-block">
  <div><h3>{copy.verify}</h3><p>{copy.verifyText}</p></div>
  <div class="verification-terminal">
    <div class="verification-bar"><i></i><span>Verification</span></div>
    <div class="verification-body">
      <div class="verification-row"><Check size={15} aria-hidden="true" /><code>phxdk doctor</code></div>
      <div class="verification-row"><Check size={15} aria-hidden="true" /><code>phxdk status</code></div>
    </div>
  </div>
</div>
```

- [ ] Group `.problem-card`, `.file-card`, `.impact-card`, `.mode-card` and `.profile-panel` selectors for the shared border, radius, background, shadow and 180 ms transition. Under `@media (hover: hover) and (pointer: fine)`, apply `translateY(-3px)`, accent border and glow; move `.problem-card .icon-tile` upward 2 px.
- [ ] Add a top accent and subtle gradient to problem cards. Ensure informational articles receive no button role, tabindex or click behavior.
- [ ] Style verification as a two-column explanatory block with a dark terminal, green indicator and separate success rows; stack it on mobile.
- [ ] Run focused E2E, `npm run check` and light/dark screenshots; expect green tests and legible terminal contrast.

---

### Task 3: Synchronize colored timeline activation and verify the release

**Files:**
- Modify: `site/src/app.css`
- Modify: `site/tests/e2e/landing.spec.ts`
- Modify: `CHANGELOG.md`
- Regenerate: `MANIFEST.json`
- Regenerate: `SHA256SUMS.txt`

**Interfaces:**
- Consumes: five existing `.timeline-step` elements with `--step` indexes.
- Produces: five fixed `--step-color` values, circles above the line and synchronized final/reduced-motion states.

- [ ] Add a Playwright assertion that every step has a distinct non-transparent circle border color and that reduced-motion steps have opacity `1` and no animation.
- [ ] Run the focused test; expect repeated neutral border colors.
- [ ] Assign colors with `.timeline-step:nth-child(1..5)` from `var(--amber)` through `#d3803f`, `#b16372`, `#8f45a6` to `var(--violet)`.
- [ ] Put track/progress at `z-index: 0`, circles at `z-index: 2` with opaque `var(--bg)`, then animate circle border, fill, glow and heading color using the same 7-second duration and `calc(var(--step) * 1.05s)` delay.
- [ ] In reduced motion, color every circle border/title with `--step-color`, remove all timeline animations and keep the completed progress line.
- [ ] Run the full site suite:

```bash
cd site
npm test
npm run check
npm run build
npm run validate:locales
npm run validate:public
npm run test:e2e
```

- [ ] Inspect 1440×900, 768×1024 and 390×844 screenshots in both themes. Confirm hover-capable CSS does not hide meaning, preset grid remains `2 × 2`, workflow paths are one per row, timeline circles cover the line and verification is readable.
- [ ] Add changelog entries for profile cleanup, surface interactions and colored timeline; regenerate and verify package evidence:

```bash
python3 tools/package_manifest.py . @phoxia/devkit 1.0.1
python3 tools/package_manifest.py --check . @phoxia/devkit 1.0.1
python3 -m unittest discover -s tests -v
npm pack --dry-run
git diff --check
```

- [ ] Commit with `git commit -m "feat(site): strengthen landing card interactions"`.
