# Rich Local Footer Design

## Goal

Give the DevKit a polished footer for a larger link inventory while removing the unnecessary visual priority from the recommended setup mode.

## Scope

The footer remains a local `Footer.svelte` implementation. It is not configurable infrastructure, a shared package or part of `@phoxia/lux`. Other sites may copy and adapt it later when explicitly requested.

## Setup modes

- Remove the special amber top border and accent border from `Add · recommended`.
- Keep all three setup modes visually equal.
- Preserve the existing descriptive copy and semantic icons.

## Footer structure

The main footer uses four columns on wide screens:

1. Brand: Phoxia DevKit name, concise product description and `AGPL-3.0-only · Phoxia` metadata.
2. Product: Documentation, Quick start and Changelog.
3. Project: GitHub, Contributing and Governance.
4. Trust & support: Security, Support, Code of Conduct and AGPLv3.

A separated bottom bar contains `© 2026 Phoxia`, the license identifier and an external GitHub link.

## Visual contract

- Reuse the site's existing background, border, text, muted text and mono typography tokens.
- Use one top hairline for the footer and one internal hairline above the bottom bar.
- Use the Phoxia symbol already provided by `@phoxia/lux`; do not show the Lux mascot.
- Link groups use compact uppercase mono labels and restrained vertical spacing.
- Hover changes text color only. Keyboard focus remains clearly visible.
- Do not repeat the installation CTA from the preceding section.

## Responsive behavior

- Desktop: `1.7fr repeat(3, 1fr)` main grid.
- Tablet: brand spans the full first row; three link groups share the second row.
- Mobile: brand first, link groups in a two-column grid; bottom bar stacks with left alignment.
- No horizontal overflow at 390 px and no hidden links.

## Localization and links

Reuse existing localized labels where available and add only the missing group/link labels to both locales. All repository links target existing files on `github.com/phoxia/phoxia-devkit`; internal links use the current canonical routes.

## Verification

- Browser coverage checks the three groups, ten navigation links, bottom bar and absence of Lux.
- Existing locale, theme, responsive and 44 px interactive-target coverage remains green.
- Inspect desktop and mobile screenshots in light and dark themes.
