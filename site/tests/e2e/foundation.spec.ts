import { expect, test } from "@playwright/test";

const pages = [
  ["/", "Phoxia • Kit"],
] as const;

for (const [path, title] of pages) {
  test(`${path} is readable`, async ({ page }) => {
    await page.goto(path);
    await expect(page).toHaveTitle(title);
    await expect(page.locator("main h1")).toBeVisible();
  });
}

test("language preference stays on the canonical URL", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Português (Brasil)" }).click();
  await expect(page.locator("main h1")).toContainText("Mantenha");
  await expect(page).toHaveURL("http://127.0.0.1:4173/");
  await page.reload();
  await expect(page.locator("main h1")).toContainText("Mantenha");
});
