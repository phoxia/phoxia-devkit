# Phoxia Kit Homepage Motion and Navigation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the approved Productive Motion homepage with useful navigation, explicit locale/theme controls, purposeful terminal motion and a richer footer.

**Architecture:** Reuse the existing locale and theme stores. Keep behavior inside the existing Svelte components and CSS; add no dependencies. Represent the terminal sequence as semantic markup whose animation is CSS-driven and disabled by `prefers-reduced-motion`.

**Tech Stack:** Svelte 5, SvelteKit, TypeScript, CSS, lucide-svelte, Playwright

## Global Constraints

- Remove Guided setup and GitHub from the header.
- Theme controls use sun, moon and monitor icons for light, dark and system.
- Language controls use visible `PT` and `EN` buttons.
- Icon-only controls require accessible names, tooltips, selected state and visible focus.
- Motion must respect `prefers-reduced-motion`.
- Add no dependencies.

---

### Task 1: Header controls

**Files:**
- Modify: `site/src/lib/components/Header.svelte`
- Modify: `site/src/app.css`
- Test: `site/tests/e2e/landing.spec.ts`
- Test: `site/tests/e2e/foundation.spec.ts`

- [ ] Replace select-based assertions with buttons named `English`, `Português`, `System theme`, `Light theme` and `Dark theme`; assert `aria-pressed` and persistence.
- [ ] Run `npm run test:e2e -- landing.spec.ts foundation.spec.ts` and confirm the new assertions fail.
- [ ] Replace both selects and the two unwanted header actions with native buttons calling existing `setLocale()` and `setTheme()` functions.
- [ ] Add compact segmented-control CSS with 44px targets, focus-visible styling and responsive wrapping.
- [ ] Run the focused Playwright tests and confirm they pass.

### Task 2: Productive terminal motion

**Files:**
- Modify: `site/src/routes/+page.svelte`
- Modify: `site/src/app.css`
- Test: `site/tests/e2e/landing.spec.ts`

- [ ] Add assertions for semantic terminal steps and the final ready state.
- [ ] Run the focused test and confirm it fails.
- [ ] Replace the monolithic terminal text with separate command, reading, connection and ready lines.
- [ ] Animate each line once with staggered opacity/translation and a blinking cursor; expose every line immediately under `prefers-reduced-motion: reduce`.
- [ ] Keep Lux anchored to the terminal's upper-right edge and verify no mobile overflow.
- [ ] Run the focused test and confirm it passes.

### Task 3: Footer information architecture

**Files:**
- Modify: `site/src/lib/components/Footer.svelte`
- Modify: `site/src/lib/i18n/landing.ts`
- Modify: `site/src/app.css`
- Test: `site/tests/e2e/landing.spec.ts`

- [ ] Assert the footer exposes product, resources and project/community groups.
- [ ] Run the focused test and confirm it fails.
- [ ] Add links for Docs, Changelog, Security, Support, GitHub, Contributing and AGPLv3 using existing repository-relative or canonical URLs.
- [ ] Add responsive three-column footer CSS without adding another component.
- [ ] Run the focused test and confirm it passes.

### Task 4: Verification and handoff

**Files:**
- Modify: `CHANGELOG.md`

- [ ] Record the navigation, motion and footer behavior under the current unreleased entry.
- [ ] Run `npm test`, `npm run check`, `npm run build`, `npm run validate:locales`, `npm run validate:public` and `npm run test:e2e` from `site/`.
- [ ] Run `git diff --check` and inspect the final diff for unrelated changes.
- [ ] Commit the implementation with `feat(site): improve landing navigation and motion`.
