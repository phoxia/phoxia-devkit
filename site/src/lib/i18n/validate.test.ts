import assert from "node:assert/strict";
import test from "node:test";

import { validateLocaleSet } from "./validate.ts";

test("rejects a missing translation key with its path", () => {
  assert.throws(
    () =>
      validateLocaleSet({
        "en-US": { nav: { home: "Home", docs: "Docs" } },
        pt: { nav: { home: "Início" } },
      }),
    /pt: missing nav\.docs/,
  );
});

test("rejects translated technical tokens", () => {
  assert.throws(
    () =>
      validateLocaleSet({
        "en-US": { title: "Use Claude Code" },
        pt: { title: "Use Código Claude" },
      }),
    /pt: title must preserve Claude Code/,
  );
});
