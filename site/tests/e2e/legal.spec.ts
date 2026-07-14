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
    expect(await page.locator(".legal-section").count()).toBeGreaterThan(0);
    expect(await page.locator(".legal-toc a").count()).toBeGreaterThan(0);
    await expect(page.locator('header a[href="/#product"]')).toHaveCount(1);
    await expect(page.locator('header a[href="/#how"]')).toHaveCount(1);
    await expect(page.locator("html")).toHaveAttribute("data-hydrated", "true");
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
