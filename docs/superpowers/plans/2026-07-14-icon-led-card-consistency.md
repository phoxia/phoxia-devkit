# Icon-led Card Consistency Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give every technical card a consistent icon-led hierarchy and make setup modes read as descriptive policies rather than ordered actions.

**Architecture:** Reuse the existing `.icon-tile`, card surfaces and installed `lucide-svelte` package. Add only semantic markup in the existing route and evidence component, then share the smallest necessary CSS rules.

**Tech Stack:** Svelte 5, TypeScript, native CSS, `lucide-svelte`, Playwright.

## Global Constraints

- Add no dependency, generic card component or JavaScript behavior.
- Replace `Choose a safe setup mode` / `Escolha um modo de configuração seguro` with descriptive headings in both locales.
- Preserve the existing 3+2 impact grid, profile grids, themes, responsive behavior and reduced motion.
- Icons are decorative and use `aria-hidden="true"`; visible text carries meaning.
- Use `Phoxia • Page` title rules and no em dashes in product copy.

---

### Task 1: Add semantic icon-led markup

**Files:**
- Modify: `site/tests/e2e/landing.spec.ts`
- Modify: `site/src/lib/components/EvidenceThread.svelte`
- Modify: `site/src/routes/+page.svelte`

**Interfaces:**
- Consumes: existing `copy`, `landingContent.paths`, `impact`, `modeCards` and `profileCards` arrays.
- Produces: `.file-title`, `.verification-title`, `.impact-title`, `.mode-icon` and `.profile-title` elements.

- [ ] **Step 1: Write the failing browser test**

```ts
test("uses semantic icons across technical card groups", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator(".pipeline-node > .icon-tile")).toHaveCount(3);
  await expect(page.locator(".file-title > svg")).toHaveCount(3);
  await expect(page.locator(".verification-title > .icon-tile")).toHaveCount(1);
  await expect(page.locator(".impact-title > .icon-tile")).toHaveCount(5);
  await expect(page.locator(".mode-card > .mode-icon")).toHaveCount(3);
  await expect(page.locator(".profile-title > .icon-tile")).toHaveCount(2);
  await expect(page.locator(".mode-card > span:not(.mode-icon)")).toHaveCount(0);
});
```

- [ ] **Step 2: Run the test and verify RED**

Run: `cd site && npx playwright test tests/e2e/landing.spec.ts --project=desktop-1440 -g "semantic icons"`

Expected: FAIL because the new icon-led selectors do not exist.

- [ ] **Step 3: Reuse existing and installed icons**

In `EvidenceThread.svelte`, wrap the three existing icons:

```svelte
<span class="icon-tile"><FileCode2 aria-hidden="true" /></span>
<span class="icon-tile"><Terminal aria-hidden="true" /></span>
<span class="icon-tile"><Check aria-hidden="true" /></span>
```

In `+page.svelte`, import `Archive`, `CircleCheckBig`, `FileCode2`, `FilePlus2`, `Layers3`, `Plus`, `RefreshCw`, `Replace`, `ShieldCheck`, `Trash2` and `Workflow`. Define only the mappings required by the existing arrays:

```ts
const impactIcons = [FilePlus2, RefreshCw, ShieldCheck, Trash2, Archive] as const;
const modeIcons = [Plus, Replace, RefreshCw] as const;
```

Render each file name as `.file-title`, verification heading as `.verification-title`, each impact heading as `.impact-title`, each mode icon as `.mode-icon.icon-tile`, and both profile headings as `.profile-title`. Use the mapped icon index already available in each `{#each}` block.

- [ ] **Step 4: Run focused test and Svelte check**

Run: `cd site && npx playwright test tests/e2e/landing.spec.ts --project=desktop-1440 -g "semantic icons" && npm run check`

Expected: one Playwright test passes and Svelte reports 0 errors and 0 warnings.

- [ ] **Step 5: Commit**

```bash
git add site/tests/e2e/landing.spec.ts site/src/lib/components/EvidenceThread.svelte site/src/routes/+page.svelte
git commit -m "feat(site): add semantic card icons"
```

---

### Task 2: Unify hierarchy, spacing and package evidence

**Files:**
- Modify: `site/src/app.css`
- Modify: `site/src/lib/i18n/landing.ts`
- Modify: `CHANGELOG.md`
- Regenerate: `MANIFEST.json`
- Regenerate: `SHA256SUMS.txt`

**Interfaces:**
- Consumes: icon-led classes from Task 1.
- Produces: one consistent title-row rhythm across the landing page.

- [ ] **Step 1: Apply the smallest shared CSS system**

```css
.problem-card .icon-tile { margin-bottom: 24px; }
.file-title,
.verification-title,
.impact-title,
.profile-title {
  display: flex;
  align-items: center;
  gap: 10px;
}
.file-title { padding: 12px 16px; }
.file-title code { color: var(--violet); font: 600 12px "JetBrains Mono", monospace; }
.pipeline-node .icon-tile,
.impact-title .icon-tile,
.mode-icon,
.profile-title .icon-tile { width: 34px; height: 34px; }
.mode-icon { margin-bottom: 24px; }
```

Remove the obsolete `.mode-card > span` number rule and preserve the existing card/hover foundation.

Replace the mode heading with `Safe setup modes` and `Modos de configuração seguros`.

- [ ] **Step 2: Verify responsive behavior**

Run: `cd site && npm test && npm run check && npm run build && npm run validate:locales && npm run validate:public && npm run test:e2e`

Expected: all checks pass at 1440, 768 and 390 px with no overflow.

- [ ] **Step 3: Inspect visual output**

Capture desktop and mobile screenshots in light and dark themes. Confirm that file names, verification, impact, modes and profile headings align; mode cards show no numbers; problem-card icon spacing is 24 px.

- [ ] **Step 4: Update release evidence**

Add an Unreleased changelog bullet for semantic card icons, then run:

```bash
python3 tools/package_manifest.py . @phoxia/devkit 1.0.1
python3 tools/package_manifest.py --check . @phoxia/devkit 1.0.1
python3 -m unittest discover -s tests -v
npm pack --dry-run
git diff --check
```

Expected: package metadata passes, 18 Python tests pass and the dry-run tarball remains `@phoxia/devkit@1.0.1`.

- [ ] **Step 5: Commit**

```bash
git add CHANGELOG.md MANIFEST.json SHA256SUMS.txt site/src/app.css
git commit -m "feat(site): unify technical card hierarchy"
```
