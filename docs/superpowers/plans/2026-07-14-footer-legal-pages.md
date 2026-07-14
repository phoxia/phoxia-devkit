# Compact Footer and Kit Legal Pages Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make footer navigation compact and centered on mobile, then publish bilingual Kit-specific privacy and terms drafts.

**Architecture:** Keep the footer local and fix its existing global `nav a` style collision with a footer-specific override. Add one reusable `LegalPage.svelte` shell and one typed bilingual content module consumed by two thin routes; do not couple the Kit build to phoxia-org.

**Tech Stack:** Svelte 5, SvelteKit static adapter, TypeScript, CSS, Playwright.

## Global Constraints

- Use `Phoxia • Page` for page titles.
- Avoid em dashes in normal product copy.
- Do not add dependencies.
- Keep `/privacy` and `/terms` bilingual in `en-US` and `pt-BR` through `localeState.current`.
- Treat legal content as a draft pending human legal review; implementation does not constitute legal approval.
- Do not copy unverified infrastructure, retention, TLS-version, analytics, account, payment, or data-processing claims from phoxia-org.
- Keep facts about DevKit local behavior consistent with repository tests and documentation.

---

### Task 1: Compact responsive footer

**Files:**
- Modify: `site/tests/e2e/landing.spec.ts`
- Modify: `site/src/lib/components/Footer.svelte`
- Modify: `site/src/lib/i18n/landing.ts`
- Modify: `site/src/app.css`

**Interfaces:**
- Consumes: `landingTranslations[localeState.current]` and the existing footer structure.
- Produces: footer-local Privacy and Terms links plus compact `.footer-group` navigation unaffected by the global `nav a` rule.

- [ ] **Step 1: Write failing footer tests**

Extend `renders the rich local footer sitemap` and `lays out the rich footer without mobile overflow`:

```ts
await expect(page.locator("footer .footer-nav a")).toHaveCount(11);
await expect(page.locator("footer .footer-group").last().getByRole("link")).toHaveText([
  "Security",
  "Support",
  "Privacy",
  "Terms",
  "Code of Conduct",
]);
await expect(page.locator('footer a[href="mailto:support@phoxia.org"]')).toHaveCount(1);
await expect(page.locator('footer a[href="/privacy"]')).toHaveCount(1);
await expect(page.locator('footer a[href="/terms"]')).toHaveCount(1);
await expect(page.locator("footer .footer-group").last()).not.toContainText("AGPLv3");
await expect(page.locator("footer .footer-bottom")).toContainText("AGPLv3");
await expect(page.locator("footer .footer-group").first()).toHaveCSS("gap", "8px");
await expect(page.locator("footer .footer-nav a").first()).toHaveCSS("min-height", "0px");
await expect(page.locator("footer .footer-nav a").first()).toHaveCSS("padding", "0px");

if (testInfo.project.name === "mobile-390") {
  await expect(page.locator(".footer-brand")).toHaveCSS("align-items", "center");
  await expect(page.locator(".footer-bottom")).toHaveCSS("align-items", "center");
  await expect(page.locator(".footer-bottom")).toHaveCSS("text-align", "center");
}
```

- [ ] **Step 2: Run the tests and verify RED**

Run:

```bash
cd site
npm run test:e2e -- --grep "rich local footer|rich footer without mobile"
```

Expected: FAIL because the old Trust & support group contains AGPLv3, Support points to GitHub Issues, legal links are absent, and generic `nav a` padding/min-height remains active.

- [ ] **Step 3: Implement the minimum footer markup and translations**

Add `privacy` and `terms` to both locale entries in `landing.ts`:

```ts
privacy: "Privacy",
terms: "Terms",
```

```ts
privacy: "Privacidade",
terms: "Termos",
```

Replace the Trust & support group in `Footer.svelte` with:

```svelte
<div class="footer-group">
  <b>{landing.trustSupport}</b>
  <a href="https://github.com/phoxia/phoxia-devkit/blob/main/SECURITY.md">{landing.security}</a>
  <a href="mailto:support@phoxia.org">{landing.support}</a>
  <a href="/privacy">{landing.privacy}</a>
  <a href="/terms">{landing.terms}</a>
  <a href="https://github.com/phoxia/phoxia-devkit/blob/main/CODE_OF_CONDUCT.md">{landing.codeOfConduct}</a>
</div>
```

Add footer-specific CSS after `.footer-group` and update the mobile block:

```css
.footer-group {
  gap: 8px;
}
.footer-nav a {
  min-height: 0;
  padding: 0;
  border-radius: 0;
  background: transparent;
}
.footer-nav a:hover {
  background: transparent;
}

@media (max-width: 600px) {
  .footer-brand,
  .footer-group {
    align-items: center;
    text-align: center;
  }
  .footer-nav {
    grid-template-columns: 1fr 1fr;
    gap: 30px 16px;
  }
  .footer-bottom {
    align-items: center;
    text-align: center;
  }
}
```

- [ ] **Step 4: Run footer tests and verify GREEN**

Run:

```bash
cd site
npm run test:e2e -- --grep "rich local footer|rich footer without mobile"
```

Expected: all selected tests pass in desktop, tablet, and mobile projects.

- [ ] **Step 5: Commit the footer change**

```bash
git add site/tests/e2e/landing.spec.ts site/src/lib/components/Footer.svelte site/src/lib/i18n/landing.ts site/src/app.css
git commit -m "fix(site): compact footer navigation"
```

---

### Task 2: Bilingual Kit legal pages

**Files:**
- Create: `site/src/lib/i18n/legal.ts`
- Create: `site/src/lib/components/LegalPage.svelte`
- Create: `site/src/routes/privacy/+page.svelte`
- Create: `site/src/routes/terms/+page.svelte`
- Create: `site/tests/e2e/legal.spec.ts`
- Modify: `site/scripts/validate-locales.mjs`

**Interfaces:**
- Produces: `LegalSection`, `LegalPageCopy`, and `legalTranslations: Record<Locale, { privacy: LegalPageCopy; terms: LegalPageCopy }>`.
- Consumes: `localeState.current`, `Header.svelte`, and `Footer.svelte`.

- [ ] **Step 1: Write failing route and localization tests**

Create `site/tests/e2e/legal.spec.ts`:

```ts
import { expect, test } from "@playwright/test";

for (const [path, title, heading] of [
  ["/privacy", "Phoxia • Privacy", "Privacy Policy"],
  ["/terms", "Phoxia • Terms", "Terms of Use"],
] as const) {
  test(`${path} renders a bilingual Kit legal draft`, async ({ page }) => {
    await page.goto(path);
    await expect(page).toHaveTitle(title);
    await expect(page.getByRole("heading", { level: 1, name: heading })).toBeVisible();
    await expect(page.getByText("Draft pending legal review", { exact: true })).toBeVisible();
    await expect(page.locator(".legal-section")).not.toHaveCount(0);
    await expect(page.locator('a[href^="#"]')).not.toHaveCount(0);
    await page.getByRole("button", { name: "Language: Português (Brasil)" }).click();
    await expect(page.getByText("Minuta pendente de revisão jurídica", { exact: true })).toBeVisible();
    await expect(page.locator("html")).toHaveAttribute("lang", "pt-BR");
  });
}

test("legal pages expose product-specific contacts and no unverified claims", async ({ page }) => {
  await page.goto("/privacy");
  await expect(page.locator("main")).toContainText("kit.phoxia.org");
  await expect(page.locator("main")).toContainText("privacy@phoxia.org");
  await expect(page.locator("main")).not.toContainText("TLS 1.3");
  await expect(page.locator("main")).not.toContainText("30-day");
  await page.goto("/terms");
  await expect(page.locator("main")).toContainText("legal@phoxia.org");
  await expect(page.locator("main")).toContainText("AGPLv3");
});
```

- [ ] **Step 2: Run legal tests and verify RED**

Run:

```bash
cd site
npm run test:e2e -- tests/e2e/legal.spec.ts
```

Expected: FAIL with 404 pages because neither route exists.

- [ ] **Step 3: Add typed legal copy**

Create `site/src/lib/i18n/legal.ts` with the following public shape:

```ts
import type { Locale } from "./locales.ts";

export type LegalSection = { id: string; title: string; content: string };
export type LegalPageCopy = {
  title: string;
  updated: string;
  status: string;
  contents: string;
  sections: LegalSection[];
};

type LegalPages = { privacy: LegalPageCopy; terms: LegalPageCopy };

export const legalTranslations: Record<Locale, LegalPages> = {
  "en-US": {
    privacy: {
      title: "Privacy Policy",
      updated: "Last updated: July 14, 2026 · Draft 1.0",
      status: "Draft pending legal review",
      contents: "Contents",
      sections: [
        { id: "scope", title: "1. Scope and controller", content: "This policy covers kit.phoxia.org, the public website for Phoxia DevKit. Phoxia, operated by Lucas Christian, is responsible for this website. Privacy inquiries: privacy@phoxia.org." },
        { id: "website-data", title: "2. Website data", content: "The Kit website does not provide user accounts or payment features. Infrastructure providers may process technical request data needed to deliver, secure, and operate the website under their own policies and applicable agreements. This policy does not claim a fixed retention period that Phoxia has not independently verified." },
        { id: "preferences", title: "3. Browser preferences", content: "The website stores your language and theme preferences in your browser. These preferences remain on your device and can be removed through your browser storage controls." },
        { id: "devkit", title: "4. DevKit local behavior", content: "Installing or using Phoxia DevKit is separate from visiting this website. The DevKit setup reads and writes project files locally. The published setup workflow does not require a Phoxia account and does not upload source code to Phoxia." },
        { id: "third-parties", title: "5. External services", content: "Links to GitHub, Discord, and email open services operated by third parties. Information you send to those services is handled under their terms and privacy policies." },
        { id: "rights", title: "6. Your rights", content: "Depending on applicable law, including the LGPD and GDPR, you may request access, correction, deletion, portability, or information about personal data processing. Send requests to privacy@phoxia.org." },
        { id: "changes", title: "7. Changes and contact", content: "Material changes will update the date on this page and the public phoxia-devkit repository. Privacy: privacy@phoxia.org. Security reports: security@phoxia.org. General support: support@phoxia.org." },
      ],
    },
    terms: {
      title: "Terms of Use",
      updated: "Last updated: July 14, 2026 · Draft 1.0",
      status: "Draft pending legal review",
      contents: "Contents",
      sections: [
        { id: "scope", title: "1. Scope", content: "These terms govern access to kit.phoxia.org and its public information about Phoxia DevKit. The DevKit software is distributed separately under its repository license." },
        { id: "use", title: "2. Acceptable use", content: "You may use the website for lawful purposes. You may not attempt unauthorized access, disrupt availability, distribute malicious content, or impersonate Phoxia or its contributors." },
        { id: "license", title: "3. Open-source license", content: "Phoxia DevKit source code is distributed under the GNU Affero General Public License v3.0, AGPLv3. Your rights to use, study, modify, and distribute the software are governed by the license text in the phoxia-devkit repository." },
        { id: "content", title: "4. Website content", content: "Website and documentation content is provided for informational purposes and may change as the DevKit evolves. Project instructions, accepted RFCs, schemas, releases, and repository license files remain authoritative." },
        { id: "third-parties", title: "5. Third-party links", content: "The website links to external services including GitHub and Discord. Phoxia does not control their availability, security, content, terms, or privacy practices." },
        { id: "disclaimer", title: "6. Disclaimer", content: "To the extent permitted by applicable law, the website and software are provided as available and without warranties beyond those that cannot legally be excluded. Review generated changes before applying them to a repository." },
        { id: "liability", title: "7. Limitation and applicable law", content: "Liability is limited to the extent permitted by applicable law. These terms are governed by the laws of Brazil, without limiting mandatory rights that apply where you live." },
        { id: "changes", title: "8. Changes and contact", content: "Material changes will update the date on this page and the public phoxia-devkit repository. Legal questions: legal@phoxia.org. Privacy: privacy@phoxia.org. Support: support@phoxia.org." },
      ],
    },
  },
  "pt-BR": {
    privacy: {
      title: "Política de Privacidade",
      updated: "Última atualização: 14 de julho de 2026 · Minuta 1.0",
      status: "Minuta pendente de revisão jurídica",
      contents: "Conteúdo",
      sections: [
        { id: "scope", title: "1. Escopo e controlador", content: "Esta política cobre o kit.phoxia.org, site público do Phoxia DevKit. A Phoxia, operada por Lucas Christian, é responsável por este site. Questões de privacidade: privacy@phoxia.org." },
        { id: "website-data", title: "2. Dados do site", content: "O site do Kit não oferece contas de usuário nem recursos de pagamento. Provedores de infraestrutura podem tratar dados técnicos de requisição necessários para entregar, proteger e operar o site, conforme suas próprias políticas e os acordos aplicáveis. Esta política não declara um prazo fixo de retenção que a Phoxia não tenha verificado de forma independente." },
        { id: "preferences", title: "3. Preferências do navegador", content: "O site armazena suas preferências de idioma e tema no navegador. Essas preferências permanecem no seu dispositivo e podem ser removidas pelos controles de armazenamento do navegador." },
        { id: "devkit", title: "4. Comportamento local do DevKit", content: "Instalar ou usar o Phoxia DevKit é diferente de visitar este site. A configuração do DevKit lê e grava arquivos do projeto localmente. O fluxo publicado não exige uma conta Phoxia e não envia código-fonte para a Phoxia." },
        { id: "third-parties", title: "5. Serviços externos", content: "Links para GitHub, Discord e e-mail abrem serviços operados por terceiros. Informações enviadas a esses serviços são tratadas conforme seus termos e políticas de privacidade." },
        { id: "rights", title: "6. Seus direitos", content: "Conforme a legislação aplicável, incluindo LGPD e GDPR, você pode solicitar acesso, correção, exclusão, portabilidade ou informações sobre o tratamento de dados pessoais. Envie solicitações para privacy@phoxia.org." },
        { id: "changes", title: "7. Alterações e contato", content: "Mudanças relevantes atualizarão a data desta página e o repositório público phoxia-devkit. Privacidade: privacy@phoxia.org. Segurança: security@phoxia.org. Suporte geral: support@phoxia.org." },
      ],
    },
    terms: {
      title: "Termos de Uso",
      updated: "Última atualização: 14 de julho de 2026 · Minuta 1.0",
      status: "Minuta pendente de revisão jurídica",
      contents: "Conteúdo",
      sections: [
        { id: "scope", title: "1. Escopo", content: "Estes termos regem o acesso ao kit.phoxia.org e às informações públicas sobre o Phoxia DevKit. O software DevKit é distribuído separadamente sob a licença do seu repositório." },
        { id: "use", title: "2. Uso aceitável", content: "Você pode usar o site para finalidades lícitas. Você não pode tentar obter acesso não autorizado, interromper a disponibilidade, distribuir conteúdo malicioso ou personificar a Phoxia ou seus colaboradores." },
        { id: "license", title: "3. Licença open source", content: "O código-fonte do Phoxia DevKit é distribuído sob a GNU Affero General Public License v3.0, AGPLv3. Seus direitos de usar, estudar, modificar e distribuir o software são regidos pelo texto da licença no repositório phoxia-devkit." },
        { id: "content", title: "4. Conteúdo do site", content: "O conteúdo do site e da documentação é fornecido para fins informativos e pode mudar conforme o DevKit evolui. Instruções do projeto, RFCs aceitas, schemas, releases e arquivos de licença do repositório permanecem autoritativos." },
        { id: "third-parties", title: "5. Links de terceiros", content: "O site possui links para serviços externos, incluindo GitHub e Discord. A Phoxia não controla a disponibilidade, segurança, conteúdo, termos ou práticas de privacidade desses serviços." },
        { id: "disclaimer", title: "6. Isenção", content: "Na extensão permitida pela legislação aplicável, o site e o software são fornecidos conforme disponíveis e sem garantias além daquelas que não podem ser legalmente excluídas. Revise as mudanças geradas antes de aplicá-las a um repositório." },
        { id: "liability", title: "7. Limitação e legislação aplicável", content: "A responsabilidade é limitada na extensão permitida pela legislação aplicável. Estes termos são regidos pelas leis do Brasil, sem limitar direitos obrigatórios aplicáveis no local onde você vive." },
        { id: "changes", title: "8. Alterações e contato", content: "Mudanças relevantes atualizarão a data desta página e o repositório público phoxia-devkit. Questões jurídicas: legal@phoxia.org. Privacidade: privacy@phoxia.org. Suporte: support@phoxia.org." },
      ],
    },
  },
};
```

Update `site/scripts/validate-locales.mjs`:

```ts
import { legalTranslations } from "../src/lib/i18n/legal.ts";

validateLocaleSet(legalTranslations);
```

- [ ] **Step 4: Add the reusable legal shell**

Create `site/src/lib/components/LegalPage.svelte`:

```svelte
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
  .legal-header svg { flex: none; margin-top: 5px; color: var(--amber); }
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
```

- [ ] **Step 5: Add the two thin routes**

Create `site/src/routes/privacy/+page.svelte`:

```svelte
<script lang="ts">
  import LegalPage from "$lib/components/LegalPage.svelte";
  import { legalTranslations } from "$lib/i18n/legal.ts";
  import { localeState } from "$lib/i18n/store.svelte.ts";
  let copy = $derived(legalTranslations[localeState.current].privacy);
</script>
<svelte:head><title>Phoxia • Privacy</title><meta name="description" content="Privacy policy for kit.phoxia.org and Phoxia DevKit." /><link rel="canonical" href="https://kit.phoxia.org/privacy" /></svelte:head>
<LegalPage {copy} kind="privacy" />
```

Create `site/src/routes/terms/+page.svelte`:

```svelte
<script lang="ts">
  import LegalPage from "$lib/components/LegalPage.svelte";
  import { legalTranslations } from "$lib/i18n/legal.ts";
  import { localeState } from "$lib/i18n/store.svelte.ts";
  let copy = $derived(legalTranslations[localeState.current].terms);
</script>
<svelte:head><title>Phoxia • Terms</title><meta name="description" content="Terms of use for kit.phoxia.org and Phoxia DevKit." /><link rel="canonical" href="https://kit.phoxia.org/terms" /></svelte:head>
<LegalPage {copy} kind="terms" />
```

- [ ] **Step 6: Run legal and locale tests and verify GREEN**

Run:

```bash
cd site
npm run validate:locales
npm run test:e2e -- tests/e2e/legal.spec.ts
```

Expected: locale coverage passes and all legal-page tests pass in three Playwright projects.

- [ ] **Step 7: Commit legal pages**

```bash
git add site/src/lib/i18n/legal.ts site/src/lib/components/LegalPage.svelte site/src/routes/privacy/+page.svelte site/src/routes/terms/+page.svelte site/tests/e2e/legal.spec.ts site/scripts/validate-locales.mjs
git commit -m "feat(site): add Kit legal pages"
```

---

### Task 3: Documentation and complete verification

**Files:**
- Modify: `CHANGELOG.md`
- Modify: `MANIFEST.json`
- Modify: `SHA256SUMS.txt`

**Interfaces:**
- Consumes: completed footer and legal pages.
- Produces: release documentation and deterministic package metadata.

- [ ] **Step 1: Document the user-facing change**

Add under `## Unreleased` in `CHANGELOG.md`:

```markdown
- Compacted footer navigation, centered its mobile layout, and added bilingual Kit privacy and terms drafts pending legal review.
```

- [ ] **Step 2: Run complete site verification**

Run:

```bash
cd site
npm run check
npm test
npm run validate:locales
npm run validate:public
CI=1 npm run test:e2e
```

Expected: zero Svelte diagnostics, 10 unit tests pass, both validators pass, production build succeeds through Playwright's web server, and all responsive E2E tests pass.

- [ ] **Step 3: Refresh and verify package metadata**

Run from the repository root:

```bash
python3 tools/package_manifest.py . @phoxia/devkit 1.0.1
python3 tools/package_manifest.py --check . @phoxia/devkit 1.0.1
python3 -m unittest discover -s tests -p 'test_*.py'
npm pack --dry-run
git diff --check
```

Expected: package metadata passes, 18 Python tests pass, dry-run pack lists `@phoxia/devkit@1.0.1`, and `git diff --check` prints nothing.

- [ ] **Step 4: Commit documentation and metadata**

```bash
git add CHANGELOG.md MANIFEST.json SHA256SUMS.txt
git commit -m "docs: record footer and legal pages"
```

- [ ] **Step 5: Verify the committed result**

Run:

```bash
git status --short
git log -3 --oneline
```

Expected: clean status and the three implementation commits at the top of `main`.
