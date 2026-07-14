# Opaque Timeline Nodes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Keep timeline node backgrounds opaque throughout animation and capitalize two repository-impact values.

**Architecture:** Remove opacity from the timeline-step parent instead of adding another layer. Update existing locale values directly and preserve all node/title animation behavior.

**Tech Stack:** Svelte 5, native CSS, TypeScript localization data, Playwright.

## Global Constraints

- Add no markup, pseudo-element, dependency or new animation.
- Preserve timing, colors, z-indexes, mobile layout and reduced-motion behavior.
- Capitalize the corresponding values in both locales.

---

### Task 1: Keep node isolation opaque and correct impact copy

**Files:**
- Modify: `site/tests/e2e/landing.spec.ts`
- Modify: `site/src/app.css`
- Modify: `site/src/lib/i18n/landing.ts`
- Modify: `CHANGELOG.md`
- Regenerate: `MANIFEST.json`
- Regenerate: `SHA256SUMS.txt`

**Interfaces:**
- Consumes: existing `.timeline-step`, node/title keyframes and `impact` locale arrays.
- Produces: timeline steps with computed opacity `1` during normal motion.

- [ ] **Step 1: Write the failing browser test**

```ts
test("keeps timeline node backgrounds opaque during motion", async ({ page }) => {
  await page.goto("/");
  for (const step of await page.locator(".timeline-step").all())
    await expect(step).toHaveCSS("opacity", "1");
  await expect(page.getByText("Your source code", { exact: true })).toBeVisible();
  await expect(page.getByText("Nothing, by default", { exact: true })).toBeVisible();
});
```

- [ ] **Step 2: Run RED**

Run: `cd site && npx playwright test tests/e2e/landing.spec.ts --project=desktop-1440 -g "node backgrounds opaque"`

Expected: FAIL because normal-motion steps compute below opacity `1` and the impact values start lowercase.

- [ ] **Step 3: Apply the root-cause fix**

Remove these declarations from `.timeline-step`:

```css
opacity: 0.58;
animation: timeline-step-pulse 7s ease-in-out infinite;
animation-delay: calc(var(--step) * 1.05s);
```

Delete the unused `@keyframes timeline-step-pulse`. Leave `timeline-node-pulse` and `timeline-title-pulse` unchanged.

Change locale values to:

```ts
["Preserve", "Your source code"],
["Remove", "Nothing, by default"],
["Preservar", "Seu código-fonte"],
["Remover", "Nada, por padrão"],
```

- [ ] **Step 4: Run GREEN and full verification**

Run:

```bash
cd site
npx playwright test tests/e2e/landing.spec.ts --project=desktop-1440 -g "node backgrounds opaque"
npm test
npm run check
npm run build
npm run validate:locales
npm run validate:public
npm run test:e2e
```

Expected: focused coverage and the complete site suite pass.

- [ ] **Step 5: Refresh package evidence and commit**

Add an Unreleased changelog bullet, then run:

```bash
python3 tools/package_manifest.py . @phoxia/devkit 1.0.1
python3 tools/package_manifest.py --check . @phoxia/devkit 1.0.1
python3 -m unittest discover -s tests -v
git diff --check
git add CHANGELOG.md MANIFEST.json SHA256SUMS.txt site/src/app.css site/src/lib/i18n/landing.ts site/tests/e2e/landing.spec.ts
git commit -m "fix(site): keep timeline nodes opaque"
```
