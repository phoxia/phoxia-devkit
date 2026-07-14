# Rich Local Footer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the compact DevKit footer with a rich local sitemap footer and remove the visual highlight from the recommended setup mode.

**Architecture:** Keep `Footer.svelte` local and write its three link groups directly in semantic markup. Reuse the Phoxia glyph from the installed `@phoxia/lux` package, existing locale objects and native CSS.

**Tech Stack:** Svelte 5, TypeScript, native CSS, `lucide-svelte`, `@phoxia/lux`, Playwright.

## Global Constraints

- Do not create configuration, shared infrastructure or a package export.
- Do not show Lux in the footer or repeat the installation CTA.
- Preserve themes, locale switching, visible focus and 390 px responsiveness.
- All repository URLs target existing files under `github.com/phoxia/phoxia-devkit`.

---

### Task 1: Remove mode priority and establish footer semantics

**Files:**
- Modify: `site/tests/e2e/landing.spec.ts`
- Modify: `site/src/routes/+page.svelte`
- Modify: `site/src/lib/components/Footer.svelte`
- Modify: `site/src/lib/i18n/landing.ts`

**Interfaces:**
- Consumes: existing `landingTranslations`, `translations`, locale state and `phoxia-glyph.svg` package asset.
- Produces: `.footer-main`, `.footer-nav`, three `.footer-group` sections, ten sitemap links and `.footer-bottom`.

- [ ] **Step 1: Write failing browser coverage**

```ts
test("keeps setup modes visually equal", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator(".mode-card.recommended")).toHaveCount(0);
  const borders = await page.locator(".mode-card").evaluateAll((cards) =>
    cards.map((card) => getComputedStyle(card).borderTopColor),
  );
  expect(new Set(borders).size).toBe(1);
});

test("renders the rich local footer sitemap", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("footer .footer-group")).toHaveCount(3);
  await expect(page.locator("footer .footer-nav a")).toHaveCount(10);
  await expect(page.locator("footer .footer-bottom")).toHaveCount(1);
  await expect(page.locator("footer img")).toHaveAttribute("src", /phoxia-glyph/);
  await expect(page.locator("footer")).not.toContainText("Lux");
});
```

- [ ] **Step 2: Run RED**

Run: `cd site && npx playwright test tests/e2e/landing.spec.ts --project=desktop-1440 -g "setup modes visually equal|rich local footer"`

Expected: FAIL because the route still emits `.recommended` and the current footer has two groups.

- [ ] **Step 3: Implement the smallest semantic markup**

Remove `class:recommended={i === 0}` from the three mode articles.

In `Footer.svelte`, import `phoxiaGlyph` from `@phoxia/lux/assets/brand/phoxia-glyph.svg?url` and render:

```svelte
<footer>
  <div class="footer-inner">
    <div class="footer-main">
      <div class="footer-brand">
        <a href="/" class="footer-logo" aria-label={landing.brandHome}>
          <img src={phoxiaGlyph} alt="" /><b>Phoxia DevKit</b>
        </a>
        <p>{landing.footer}</p>
      </div>
      <nav class="footer-nav" aria-label={landing.footerNavigation}>
        <div class="footer-group"><b>{landing.product}</b><a href="/docs">{copy.docs}</a><a href="/quick-start">{landing.quickStart}</a><a href="/changelog">{copy.changelog}</a></div>
        <div class="footer-group"><b>{landing.project}</b><a href="https://github.com/phoxia/phoxia-devkit">GitHub</a><a href="https://github.com/phoxia/phoxia-devkit/blob/main/CONTRIBUTING.md">{landing.contributing}</a><a href="https://github.com/phoxia/phoxia-devkit/blob/main/GOVERNANCE.md">{landing.governance}</a></div>
        <div class="footer-group"><b>{landing.trustSupport}</b><a href="https://github.com/phoxia/phoxia-devkit/blob/main/SECURITY.md">{landing.security}</a><a href="https://github.com/phoxia/phoxia-devkit/issues">{landing.support}</a><a href="https://github.com/phoxia/phoxia-devkit/blob/main/CODE_OF_CONDUCT.md">{landing.codeOfConduct}</a><a href="https://github.com/phoxia/phoxia-devkit/blob/main/LICENSE">AGPLv3</a></div>
      </nav>
    </div>
    <div class="footer-bottom"><span>© {new Date().getFullYear()} Phoxia · AGPLv3 · phoxia.org</span><div class="footer-external"><a href="https://discord.gg/HD2p367Zb5">Discord</a><a href="https://github.com/phoxia/phoxia-devkit"><Github size={14} aria-hidden="true" /> GitHub</a></div></div>
  </div>
</footer>
```

Add localized `quickStart`, `governance`, `codeOfConduct`, `trustSupport` and `footerNavigation` labels in English and Portuguese.

- [ ] **Step 4: Run GREEN and check types/locales**

Run: `cd site && npx playwright test tests/e2e/landing.spec.ts --project=desktop-1440 -g "setup modes visually equal|rich local footer" && npm run check && npm run validate:locales`

Expected: two Playwright tests pass, Svelte has 0 diagnostics and both locales pass.

- [ ] **Step 5: Commit**

```bash
git add site/tests/e2e/landing.spec.ts site/src/routes/+page.svelte site/src/lib/components/Footer.svelte site/src/lib/i18n/landing.ts
git commit -m "feat(site): add rich local footer structure"
```

---

### Task 2: Apply responsive footer layout and release evidence

**Files:**
- Modify: `site/src/app.css`
- Modify: `CHANGELOG.md`
- Regenerate: `MANIFEST.json`
- Regenerate: `SHA256SUMS.txt`

**Interfaces:**
- Consumes: footer classes produced by Task 1.
- Produces: four-column desktop, two-row tablet and two-column mobile footer layouts.

- [ ] **Step 1: Replace obsolete footer and recommendation CSS**

Delete `.mode-card.recommended` and replace the old footer grid with:

```css
.footer-inner { max-width: 1120px; margin: auto; padding: 56px 24px 24px; }
.footer-main { display: grid; grid-template-columns: 1.7fr 3fr; gap: 64px; }
.footer-nav { display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; }
.footer-group { display: flex; flex-direction: column; gap: 10px; }
.footer-bottom { display: flex; justify-content: space-between; margin-top: 42px; padding-top: 20px; border-top: 1px solid var(--border); }
@media (max-width: 900px) { .footer-main { grid-template-columns: 1fr; } }
@media (max-width: 600px) { .footer-nav { grid-template-columns: 1fr 1fr; } .footer-bottom { align-items: flex-start; flex-direction: column; } }
```

Use existing token colors and mono type for group labels/legal metadata. Link hover changes text color only.

- [ ] **Step 2: Run full site verification**

Run: `cd site && npm test && npm run check && npm run build && npm run validate:locales && npm run validate:public && npm run test:e2e`

Expected: all site and browser tests pass at 1440, 768 and 390 px.

- [ ] **Step 3: Inspect four screenshots**

Inspect desktop and mobile in light and dark themes. Confirm all ten links remain visible, mobile has no overflow, the glyph is not Lux and all setup-mode borders match.

- [ ] **Step 4: Update package evidence**

Add an Unreleased changelog bullet, then run:

```bash
python3 tools/package_manifest.py . @phoxia/devkit 1.0.1
python3 tools/package_manifest.py --check . @phoxia/devkit 1.0.1
python3 -m unittest discover -s tests -v
npm pack --dry-run
git diff --check
```

Expected: package metadata passes, 18 Python tests pass and the dry-run remains `@phoxia/devkit@1.0.1`.

- [ ] **Step 5: Commit**

```bash
git add CHANGELOG.md MANIFEST.json SHA256SUMS.txt site/src/app.css
git commit -m "feat(site): finish rich local footer"
```
