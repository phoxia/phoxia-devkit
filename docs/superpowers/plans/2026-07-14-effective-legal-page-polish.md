# Effective Legal Page Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Align legal-page titles with their content, publish effective updated dates without draft labels, and render contacts one per line.

**Architecture:** Keep the existing `LegalPage.svelte` and typed legal copy. Use the same two-column grid for the header and body, position the decorative icon in the gutter so the title starts exactly at the content edge, and rely on the existing `white-space: pre-line` behavior for contact line breaks.

**Tech Stack:** Svelte 5, TypeScript, CSS, Playwright.

## Global Constraints

- Apply the change equally to `/privacy` and `/terms` in English and Brazilian Portuguese.
- Show only the last-updated date; remove draft, version, and pending-review labels.
- Keep page titles in `Phoxia • Page` format.
- Do not add dependencies or new components.
- Keep contacts in the final section, one address per line.

---

### Task 1: Effective legal copy and aligned presentation

**Files:**
- Modify: `site/tests/e2e/legal.spec.ts`
- Modify: `site/src/lib/i18n/legal.ts`
- Modify: `site/src/lib/components/LegalPage.svelte`
- Modify: `CHANGELOG.md`
- Modify: `MANIFEST.json`
- Modify: `SHA256SUMS.txt`

**Interfaces:**
- Consumes: existing `LegalPageCopy`, `legalTranslations`, and `LegalPage` route usage.
- Produces: `LegalPageCopy` without `status`; `LegalPage` accepts only `{ copy: LegalPageCopy }`.

- [ ] **Step 1: Write failing presentation and copy tests**

Update each route test in `site/tests/e2e/legal.spec.ts`:

```ts
await expect(page.getByText("Last updated: July 14, 2026", { exact: true })).toBeVisible();
await expect(page.locator("main")).not.toContainText("Draft");

if (testInfo.project.name === "desktop-1440") {
  const [titleBox, sectionBox] = await Promise.all([
    page.locator(".legal-header h1").boundingBox(),
    page.locator(".legal-section h2").first().boundingBox(),
  ]);
  expect(titleBox?.x).toBeCloseTo(sectionBox?.x ?? 0, 0);
}
```

After changing the locale, assert:

```ts
await expect(page.getByText("Última atualização: 14 de julho de 2026", { exact: true })).toBeVisible();
await expect(page.locator("main")).not.toContainText("Minuta");
```

Add a contact-layout test:

```ts
test("legal contacts render one per line", async ({ page }) => {
  await page.goto("/terms");
  const termsContact = await page.locator(".legal-section").last().locator("p").textContent();
  expect(termsContact).toContain("\n\nLegal questions: legal@phoxia.org\nPrivacy: privacy@phoxia.org\nSupport: support@phoxia.org");
  await page.goto("/privacy");
  const privacyContact = await page.locator(".legal-section").last().locator("p").textContent();
  expect(privacyContact).toContain("\n\nPrivacy: privacy@phoxia.org\nSecurity reports: security@phoxia.org\nGeneral support: support@phoxia.org");
});
```

- [ ] **Step 2: Run the legal suite and verify RED**

Run:

```bash
cd site
npm run test:e2e -- tests/e2e/legal.spec.ts
```

Expected: FAIL because draft labels and versions remain, the title begins left of the content, and contacts have no newline characters.

- [ ] **Step 3: Remove draft status from the typed copy and component**

Change `LegalPageCopy` in `site/src/lib/i18n/legal.ts` to:

```ts
export type LegalPageCopy = {
  title: string;
  updated: string;
  contents: string;
  sections: LegalSection[];
};
```

Use these dates in both page entries:

```ts
updated: "Last updated: July 14, 2026",
```

```ts
updated: "Última atualização: 14 de julho de 2026",
```

Delete all four `status` properties. In `LegalPage.svelte`, remove `<strong>{copy.status}</strong>` and remove the `.legal-header strong` rule.

- [ ] **Step 4: Put the legal header on the content grid**

Change the header markup in `LegalPage.svelte`:

```svelte
<header class="legal-header">
  <div class="legal-heading">
    <Icon size={22} aria-hidden="true" />
    <div><h1>{copy.title}</h1><p>{copy.updated}</p></div>
  </div>
</header>
```

Replace the header styles with:

```css
.legal-header {
  display: grid;
  grid-template-columns: 240px minmax(0, 760px);
  justify-content: center;
  gap: 48px;
  margin: 0 auto 40px;
}
.legal-heading {
  position: relative;
  grid-column: 2;
}
.legal-heading :global(svg) {
  position: absolute;
  top: 5px;
  right: calc(100% + 14px);
  color: var(--amber);
}
.legal-heading h1 { margin: 0; font-size: clamp(30px, 4vw, 44px); line-height: 1.1; }
.legal-heading p { margin: 10px 0 0; color: var(--muted); font: 11px "JetBrains Mono", monospace; }
@media (max-width: 800px) {
  .legal-header { grid-template-columns: 1fr; gap: 0; }
  .legal-heading { grid-column: 1; }
  .legal-heading :global(svg) { left: auto; right: 0; }
}
```

- [ ] **Step 5: Separate contacts in both locales**

Use these exact final-section strings in `site/src/lib/i18n/legal.ts`:

```ts
"Material changes will update the date on this page and the public phoxia-devkit repository.\n\nPrivacy: privacy@phoxia.org\nSecurity reports: security@phoxia.org\nGeneral support: support@phoxia.org."
```

```ts
"Material changes will update the date on this page and the public phoxia-devkit repository.\n\nLegal questions: legal@phoxia.org\nPrivacy: privacy@phoxia.org\nSupport: support@phoxia.org."
```

```ts
"Mudanças relevantes atualizarão a data desta página e o repositório público phoxia-devkit.\n\nPrivacidade: privacy@phoxia.org\nSegurança: security@phoxia.org\nSuporte geral: support@phoxia.org."
```

```ts
"Mudanças relevantes atualizarão a data desta página e o repositório público phoxia-devkit.\n\nQuestões jurídicas: legal@phoxia.org\nPrivacidade: privacy@phoxia.org\nSuporte: support@phoxia.org."
```

- [ ] **Step 6: Update the changelog and verify GREEN**

Replace `drafts pending legal review` in the current Unreleased footer/legal entry with `effective pages`, then run:

```bash
cd site
npm run check
npm run validate:locales
npm run test:e2e -- tests/e2e/legal.spec.ts
```

Expected: zero Svelte diagnostics, locale validation passes, and all legal tests pass across desktop, tablet, and mobile.

- [ ] **Step 7: Run full verification and refresh metadata**

Run from the repository root:

```bash
cd site
npm test
npm run validate:public
CI=1 npm run test:e2e
cd ..
python3 tools/package_manifest.py . @phoxia/devkit 1.0.1
python3 tools/package_manifest.py --check . @phoxia/devkit 1.0.1
python3 -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

Expected: 10 site unit tests pass, public validation passes, the production build and full responsive E2E suite pass, package metadata passes, 18 Python tests pass, and `git diff --check` prints nothing.

- [ ] **Step 8: Commit the verified adjustment**

```bash
git add CHANGELOG.md MANIFEST.json SHA256SUMS.txt site/src/lib/i18n/legal.ts site/src/lib/components/LegalPage.svelte site/tests/e2e/legal.spec.ts
git commit -m "fix(site): polish effective legal pages"
git status --short
```

Expected: the commit succeeds and status is clean.
