# Icon-led Card Consistency Design

## Goal

Make the landing page's technical cards read as one product system while keeping each section's information hierarchy distinct.

## Visual contract

- Reuse the existing 38 px `.icon-tile`, card border, radius, surface, shadow and hover treatment.
- Reduce the problem-card icon-to-title gap from 38 px to 24 px.
- Keep the evidence pipeline as a sequence, but place each existing icon in an `.icon-tile` so its cards match the rest of the page.
- Add `FileCode2` before every managed filename in the repository file cards.
- Add an icon-led title row to readable verification output while preserving the two-command terminal.
- Give each repository-impact item a semantic icon: create, update, preserve, remove and backup.
- Replace setup-mode numbers with semantic icons. The section remains descriptive, with no buttons, selection state or action language.
- Add icon-led headings to Official presets and Run a workflow. Individual profile paths remain compact code cells.

## Icon mapping

- Files: `FileCode2`
- Verification: `CircleCheckBig`
- Impact: `FilePlus2`, `RefreshCw`, `ShieldCheck`, `Trash2`, `Archive`
- Setup modes: `Plus`, `Replace`, `RefreshCw`
- Profiles: `Layers3`, `Workflow`

All icons are decorative and use `aria-hidden="true"`; visible text continues to carry meaning.

## Layout and interaction

- Title rows use flex alignment, an 8–10 px gap and the existing typographic scale.
- Repository-impact cards use the currently approved 3+2 grid and spend freed space on a stronger icon/title row.
- Setup-mode cards keep three equal columns, but their icon/title grouping makes them read as available policies rather than ordered steps.
- Existing hover, dark theme, responsive layout and reduced-motion behavior remain unchanged.

## Scope

Use only `lucide-svelte`, existing markup and native CSS. Add no dependency, generic card component, JavaScript behavior or new translated copy.

## Verification

- Browser tests assert icon counts for pipeline, files, verification, impact, modes and profiles.
- Existing responsive, localization, accessibility and overflow coverage remains green.
- Inspect desktop and mobile in light and dark themes.
