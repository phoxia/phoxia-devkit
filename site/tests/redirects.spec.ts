import { readFile } from "node:fs/promises";
import { expect, test } from "@playwright/test";

const redirects = [
  ["/docs", "https://docs.phoxia.org/kit", "docs.html"],
  ["/quickstart", "https://docs.phoxia.org/kit/quickstart", "quickstart.html"],
  ["/quick-start", "https://docs.phoxia.org/kit/quickstart", "quick-start.html"],
  ["/changelog", "https://changelog.phoxia.org/kit", "changelog.html"],
] as const;

test("Vercel deployment contract serves canonical redirects as HTTP 308", async () => {
  const config = JSON.parse(await readFile(new URL("../vercel.json", import.meta.url), "utf8"));
  const rules = redirects.map(([source, destination]) => ({ source, destination, permanent: true }));
  expect(config.redirects).toEqual(rules);
  // Vercel's redirects contract maps permanent:true to 308, and false to 307.
  expect(rules.map((rule) => rule.permanent ? 308 : 307)).toEqual([308, 308, 308, 308]);
});

for (const [source, target, artifact] of redirects) {
  test(`${source} has a static redirect artifact`, async () => {
    const html = await readFile(new URL(`../build/${artifact}`, import.meta.url), "utf8");
    expect(html).toContain(`<meta http-equiv="refresh" content="0;url=${target}">`);
  });
}
