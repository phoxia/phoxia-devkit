# Phoxia DevKit card system and timeline polish

## Goal

Give the landing a consistent technical-surface system, stronger hover feedback, a clearer animated timeline and useful profile/workflow presentation without advertising speculative community publishing.

## Content changes

- Remove Community publishing and its `Coming soon` copy from both locales and from the landing markup.
- Keep only Official presets and Run a workflow in the profiles section.
- Present `profiles/personal`, `profiles/work`, `profiles/phoxia` and `profiles/specialist` as four equal monospaced cells in a `2 × 2` grid.
- Present `~/.agents/skills/phoxia-dev` and `/phoxia-core:devkit` as two equal monospaced rows.
- Preserve the exact public paths and product descriptions.

## Shared surface language

Problem cards, file cards, impact cards, setup modes and profile panels share visual foundations without introducing a generic Svelte component:

- 14 px corner radius;
- neutral border and theme-aware surface;
- short restrained shadow;
- 180 ms transition;
- hover elevation of 3 px;
- accent border and subtle theme-aware glow;
- visible icon or content response where an icon exists.

Group selectors in CSS for the shared foundation. Keep each component's internal layout semantic and distinct. Content must remain understandable without hover.

## Problem-card interaction

- Keep the existing four icons and content.
- Increase icon presence and add a restrained top accent.
- On hover, lift the card, brighten its border, reveal a soft accent gradient and move the icon upward slightly.
- Do not add JavaScript, click behavior or misleading interactive roles.

## Profile and workflow panels

Use two equal top-level panels on desktop and tablet:

- Official presets contains four equal cells in two columns and two rows.
- Run a workflow contains two equal full-width rows.

On mobile, the two panels stack, while the preset cells remain `2 × 2`. Paths use JetBrains Mono, wrap safely and never overflow at 390 px.

## Workflow timeline

The timeline line sits behind five opaque numbered circles. Each circle is visually above the line and uses a fixed step color progressing from amber to violet:

1. amber;
2. amber-violet mix leaning amber;
3. balanced amber-violet mix;
4. amber-violet mix leaning violet;
5. violet.

Synchronize line progress and step activation. When progress reaches a step, its circle fills, border brightens, glow pulses and title gains the same step color. Inactive steps remain readable but subdued.

Mobile uses the same sequence vertically. With `prefers-reduced-motion: reduce`, remove travel and pulsing and render all steps in their final colored state.

## Verification panel

Replace the plain Readable verification card with a compact dark command-output panel consistent with the hero terminal:

- explanatory title and copy remain outside the terminal body;
- header label is `Verification` with a green status indicator;
- `phxdk doctor` and `phxdk status` appear on separate rows;
- each row has a visible success check;
- terminal colors remain legible in light and dark themes.

## Responsive and accessibility contract

- Preserve all content and meaning without hover.
- Preserve visible keyboard focus for actual interactive controls; informational cards remain non-interactive articles.
- No horizontal overflow at 390 px.
- Hover transforms apply only on hover-capable pointers.
- Reduced-motion mode removes elevation transitions, timeline travel and pulses.
- Existing locale, theme, terminal, header, footer and installation behavior remain unchanged.

## Implementation constraints

- Use native CSS, existing Lucide icons and current Svelte markup.
- Add no dependency, JavaScript animation or generic card component.
- Delete obsolete Community publishing data and styles rather than hiding them.

## Verification

- Unit/localization validation proves no Community publishing copy remains.
- Playwright verifies two profile panels, four preset cells, two workflow rows, timeline step colors, reduced-motion state and the two verification commands.
- Visual inspection covers 1440 px, 768 px and 390 px in light and dark themes.
- Full site and package verification remain green.
