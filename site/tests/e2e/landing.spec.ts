import { expect, test } from "@playwright/test";

test("exposes the approved hierarchy", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveTitle("Phoxia • Kit");
  await expect(page.getByRole("heading", { level: 1 })).toContainText(
    "Keep AI-assisted development",
  );
  await expect(page.getByText("THE DEVKIT PIPELINE")).toBeVisible();
  await expect(page.getByText("npx @phoxia/devkit init").first()).toBeVisible();
  await expect(page.getByText("Reading project context")).toBeVisible();
  await expect(page.getByText("Ready locally")).toBeVisible();
  await expect(
    page.getByRole("link", { name: "Skip to content" }),
  ).toBeAttached();
});

test("keeps the command selectable when clipboard access fails", async ({ page }) => {
  await page.goto("/");
  await page.evaluate(() => {
    Object.defineProperty(navigator, "clipboard", {
      configurable: true,
      value: { writeText: () => Promise.reject(new Error("denied")) },
    });
  });
  await page.getByRole("button", { name: "Copy setup command" }).click();
  await expect(page.getByRole("status")).toContainText("Select and copy the command manually");
  await expect(page.locator(".copy-command code")).toHaveText("npx @phoxia/devkit init");
});

test("copies the setup command with an announced status", async ({
  page,
  context,
}) => {
  await context.grantPermissions(["clipboard-read", "clipboard-write"]);
  await page.goto("/");
  await page.getByRole("button", { name: "Copy setup command" }).click();
  await expect(page.getByRole("status")).toHaveText("Copied");
  await expect(
    page.evaluate(() => navigator.clipboard.readText()),
  ).resolves.toBe("npx @phoxia/devkit init");
});

test("renders eight complete localized sections", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("main > section[data-section]")).toHaveCount(8);
  await expect(page.locator('[data-section="pipeline"]')).toHaveCount(1);
  await expect(page.locator('[data-section="files-impact"]')).toHaveCount(1);
  await expect(page.locator('[data-section="configuration-trust"]')).toHaveCount(1);
  await expect(page.locator('[data-section="newcomer"]')).toHaveCount(0);
  await page.getByRole("button", { name: "Language: Português (Brasil)" }).click();
  await expect(
    page.getByRole("heading", { name: "O que muda no meu repositório?" }),
  ).toBeVisible();
  await expect(
    page.getByRole("heading", {
      name: "Executado na sua máquina. Nos seus termos.",
    }),
  ).toBeVisible();
  await expect(page.getByText("THE PROBLEM")).toHaveCount(0);
  await expect(page.getByText("Configure este repositório?")).toBeVisible();
  await expect(page.getByRole("button", { name: "Copiar comando de configuração" })).toBeVisible();
  await expect(page.locator('[data-section="pipeline"] .pipeline')).toHaveAttribute("aria-label", "Fio de evidências do contexto do projeto ao resultado verificado");
});

test("keeps every landing section visible before scrolling", async ({ page }) => {
  await page.goto("/");
  const opacities = await page.locator("main > section[data-section]").evaluateAll((sections) =>
    sections.map((section) => getComputedStyle(section).opacity),
  );
  expect(opacities).toEqual(Array(8).fill("1"));
});

test("navigation anchors target real sections", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("#product")).toHaveCount(1);
  await expect(page.locator("#how")).toHaveCount(1);
  await expect(page.locator("header").getByText("GitHub")).toHaveCount(0);
  await expect(page.getByText("Start the guided setup")).toHaveCount(0);
  await expect(page.getByRole("link", { name: "Install Phoxia DevKit" }).first()).toBeVisible();
  await expect(page.locator("footer").getByRole("link", { name: "Security" })).toBeVisible();
  await expect(page.locator("footer").getByRole("link", { name: "AGPLv3" })).toBeVisible();
});

test("blocked locale storage does not prevent theme initialization", async ({ page }) => {
  await page.addInitScript(() => { Storage.prototype.getItem = () => { throw new Error("blocked"); }; Storage.prototype.setItem = () => { throw new Error("blocked"); }; });
  await page.goto("/");
  await expect(page.locator("html")).toHaveAttribute("data-theme", /light|dark/);
});

test("reduced motion exposes the complete terminal immediately", async ({ page }) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/");
  const lines = page.locator(".terminal-line");
  await expect(lines).toHaveCount(7);
  for (const line of await lines.all()) {
    await expect(line).toHaveCSS("animation-name", "none");
    await expect(line).toHaveCSS("opacity", "1");
  }
});

test("cycles persistent themes with one compact control", async ({
  page,
}) => {
  await page.emulateMedia({ colorScheme: "light" });
  await page.goto("/");
  await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
  const theme = page.getByRole("button", { name: "Theme: System" });
  await expect(theme).toHaveCount(1);
  await theme.click();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  await page.getByRole("button", { name: "Theme: Dark" }).click();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
  await page.getByRole("button", { name: "Theme: Light" }).click();
  await page.reload();
  await expect(page.getByRole("button", { name: "Theme: System" })).toHaveCount(1);
});

test("uses compact preference controls and product-focused footer copy", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("header .header-actions button")).toHaveCount(2);
  await expect(page.locator("header .segmented")).toHaveCount(0);
  await expect(page.locator('[data-section="problem"] .section-heading-row .lux-side')).toHaveCount(1);
  await expect(page.locator("footer")).toContainText("Project context");
  await expect(page.locator("footer")).not.toContainText("Lux");
});

test("uses distinct product components instead of a repeated card grid", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator(".problem-card > .icon-tile")).toHaveCount(4);
  await expect(page.locator(".pipeline-node")).toHaveCount(3);
  await expect(page.locator(".file-card")).toHaveCount(3);
  await expect(page.locator(".impact-card")).toHaveCount(5);
  await expect(page.locator(".mode-card")).toHaveCount(3);
  await expect(page.locator(".trust-fact")).toHaveCount(3);
  await expect(page.locator(".profile-panels")).toHaveCount(1);
});

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

test("aligns technical card icons with their titles", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator(".problem-card .icon-tile").first()).toHaveCSS("margin-bottom", "24px");
  await expect(page.locator(".file-title").first()).toHaveCSS("display", "flex");
  await expect(page.locator(".pipeline-node .icon-tile").first()).toHaveCSS("width", "34px");
  await expect(page.locator(".mode-icon").first()).toHaveCSS("margin-bottom", "24px");
});

test("describes setup modes without presenting an action", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Safe setup modes", exact: true })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Choose a safe setup mode", exact: true })).toHaveCount(0);
});

test("shows profile paths without speculative community publishing", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator(".profile-panel")).toHaveCount(2);
  await expect(page.locator(".preset-cell")).toHaveCount(4);
  await expect(page.locator(".workflow-cell")).toHaveCount(2);
  await expect(page.getByText("Community publishing")).toHaveCount(0);
  await expect(page.getByText("# coming soon")).toHaveCount(0);
});

test("presents verification as two readable terminal checks", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator(".verification-terminal")).toHaveCount(1);
  await expect(page.locator(".verification-row")).toHaveCount(2);
  await expect(page.locator(".verification-terminal")).toContainText("phxdk doctor");
  await expect(page.locator(".verification-terminal")).toContainText("phxdk status");
});

test("renders an ordered animated workflow", async ({ page }) => {
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

test("keeps all workflow stages visibly color coded without motion", async ({ page }) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/");
  const colors = await page.locator(".timeline-step > span").evaluateAll((items) =>
    items.map((item) => getComputedStyle(item).borderColor),
  );
  expect(new Set(colors).size).toBe(5);
  for (const node of await page.locator(".timeline-step > span").all())
    await expect(node).toHaveCSS("animation-name", "none");
});

test("fills repository impact rows and avoids mobile overflow", async ({ page }, testInfo) => {
  await page.goto("/");
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
  expect(overflow).toBe(false);
  if (testInfo.project.name === "desktop-1440") {
    const boxes = await page.locator(".impact-card").evaluateAll((items) => items.map((item) => item.getBoundingClientRect()));
    expect(boxes[0].width).toBeCloseTo(boxes[1].width, 0);
    expect(boxes[3].width).toBeGreaterThan(boxes[0].width);
    expect(boxes[4].width).toBeCloseTo(boxes[3].width, 0);
    const section = await page.locator('[data-section="problem"]').boundingBox();
    const lux = await page.locator('[data-section="problem"] .lux-side').boundingBox();
    expect((section?.x ?? 0) + (section?.width ?? 0) - ((lux?.x ?? 0) + (lux?.width ?? 0))).toBeLessThan(40);
  }
});

test("uses offline fonts and 44px interactive targets", async ({ page }) => {
  const externalFonts: string[] = [];
  page.on("request", (request) => {
    if (/fonts\.googleapis|fonts\.gstatic/.test(request.url()))
      externalFonts.push(request.url());
  });
  await page.goto("/");
  expect(externalFonts).toEqual([]);
  for (const locator of [
    page.getByRole("button", { name: "Language: Português (Brasil)" }),
    page.getByRole("button", { name: "Theme: System" }),
    page.getByRole("button", { name: "Copy setup command" }),
  ]) {
    expect((await locator.boundingBox())?.height).toBeGreaterThanOrEqual(44);
  }
  for (const link of await page.locator("header nav a:visible").all()) expect((await link.boundingBox())?.height).toBeGreaterThanOrEqual(44);
});
