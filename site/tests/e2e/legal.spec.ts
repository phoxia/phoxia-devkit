import { expect, test } from "@playwright/test";

for (const [path, title, heading] of [
  ["/privacy", "Phoxia • Privacy", "Privacy Policy"],
  ["/terms", "Phoxia • Terms", "Terms of Use"],
] as const) {
  test(`${path} renders an effective bilingual Kit legal page`, async ({ page }, testInfo) => {
    await page.goto(path);
    await expect(page).toHaveTitle(title);
    await expect(page.getByRole("heading", { level: 1, name: heading })).toBeVisible();
    await expect(page.getByText("Last updated: July 14, 2026", { exact: true })).toBeVisible();
    await expect(page.locator("main")).not.toContainText("Draft");
    expect(await page.locator(".legal-section").count()).toBeGreaterThan(0);
    expect(await page.locator(".legal-toc a").count()).toBeGreaterThan(0);
    if (testInfo.project.name.includes("desktop")) {
      const titleBox = await page.locator(".legal-header h1").boundingBox();
      const sectionBox = await page.locator(".legal-section h2").first().boundingBox();
      expect(titleBox).not.toBeNull();
      expect(sectionBox).not.toBeNull();
      expect(titleBox!.x).toBeCloseTo(sectionBox!.x, 0);
    }
    await expect(page.locator('header a[href="/#product"]')).toHaveCount(1);
    await expect(page.locator('header a[href="/#how"]')).toHaveCount(1);
    await expect(page.locator("html")).toHaveAttribute("data-hydrated", "true");
    await page.getByRole("button", { name: "Language: Português (Brasil)" }).click();
    await expect(page.getByText("Última atualização: 14 de julho de 2026", { exact: true })).toBeVisible();
    await expect(page.locator("main")).not.toContainText("Minuta");
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

test("legal contacts render one per line", async ({ page }) => {
  await page.goto("/terms");
  expect(await page.locator("#changes p").textContent()).toContain(
    "\n\nLegal questions: legal@phoxia.org\nPrivacy: privacy@phoxia.org\nSupport: support@phoxia.org",
  );

  await page.goto("/privacy");
  expect(await page.locator("#changes p").textContent()).toContain(
    "\n\nPrivacy: privacy@phoxia.org\nSecurity reports: security@phoxia.org\nGeneral support: support@phoxia.org",
  );
});
