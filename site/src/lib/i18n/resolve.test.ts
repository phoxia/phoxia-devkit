import assert from "node:assert/strict";
import test from "node:test";

import { resolveLocale } from "./resolve.ts";

test("prefers a supported stored locale", () => {
  assert.equal(resolveLocale("pt-BR", ["en-US"]), "pt-BR");
  assert.equal(resolveLocale("en-GB", ["pt-BR"]), "en-US");
  assert.equal(resolveLocale("pt-PT", ["en-US"]), "pt-BR");
});

test("maps English and Portuguese variants", () => {
  assert.equal(resolveLocale(null, ["en-GB"]), "en-US");
  assert.equal(resolveLocale(null, ["pt-PT"]), "pt-BR");
});

test("falls back to English for unsupported stored and browser locales", () => {
  assert.equal(resolveLocale("de", ["pt-BR"]), "pt-BR");
  assert.equal(resolveLocale(null, ["de-AT"]), "en-US");
});

test("falls back to English for invalid preferences", () => {
  assert.equal(resolveLocale("invalid", ["xx"]), "en-US");
});
