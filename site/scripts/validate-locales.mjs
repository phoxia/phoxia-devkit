import { SUPPORTED_LOCALES } from "../src/lib/i18n/locales.ts";
import { localeNames, translations } from "../src/lib/i18n/content.ts";
import { validateLocaleSet } from "../src/lib/i18n/validate.ts";
import { landingTranslations } from "../src/lib/i18n/landing.ts";
import { legalTranslations } from "../src/lib/i18n/legal.ts";

validateLocaleSet(translations);
validateLocaleSet(landingTranslations);
validateLocaleSet(legalTranslations);
for (const locale of SUPPORTED_LOCALES) {
  if (!translations[locale])
    throw new Error(`${locale}: translation is missing`);
  if (!localeNames[locale])
    throw new Error(`${locale}: native name is missing`);
}
if (Object.keys(translations).length !== SUPPORTED_LOCALES.length)
  throw new Error("Unexpected locale entry");
console.log(`Locale coverage passed: ${SUPPORTED_LOCALES.length} locales.`);
