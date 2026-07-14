# Phoxia Kit homepage motion and navigation design

## Goal

Make the landing page more engaging while keeping motion purposeful, navigation concise and controls immediately understandable.

## Approved direction

- Use the “Productive motion” direction selected by the owner.
- Remove Guided setup and the GitHub action from the header.
- Keep only useful product navigation in the header.
- Replace dropdown-like theme and language controls with two compact groups:
  - language: `PT | EN`, with the active locale visibly selected;
  - theme: sun, moon and monitor icons for light, dark and system, with accessible labels, tooltips and selected state.
- Animate the terminal as a short deterministic setup sequence, respecting `prefers-reduced-motion`.
- Position Lux over the terminal's upper-right edge so it belongs to the composition rather than floating beside it.
- Use subtle section entrance motion only when it improves hierarchy; no continuous decorative movement.
- Expand the footer into three useful areas: product description, product resources and project/community resources.
- Keep the existing Phoxia visual tokens, copy, locale behavior and responsive breakpoints.

## Responsive and accessibility contract

- Desktop navigation remains a single balanced row without crowding.
- Mobile controls remain reachable and do not overflow the header.
- Every icon-only control has an accessible name and visible focus state.
- Active locale and theme expose their selected state programmatically.
- Reduced-motion users receive the final terminal state immediately and no entrance animation.

## Verification

- `npm run check`
- `npm run build`
- Existing Playwright coverage plus focused assertions for header controls and reduced-motion behavior.
- Visual inspection at desktop, tablet and mobile widths.

## Approved visual correction

- Match the compact controls already used by `phoxia.org`: one language button cycles between Portuguese and English, and one theme button cycles between system, light and dark while showing the resulting mode icon.
- Remove the segmented control containers and active-state pills. Preserve accessible names, titles, focus treatment and persisted preferences.
- Move the confused Lux from above “The Problem” to the right of that section heading, aligned with the title instead of occupying its own row. Stack it naturally below the heading on narrow screens.
- Keep Lux as supporting artwork only. Footer copy must describe the DevKit itself: shared project context, repeatable workflows and verifiable changes for Claude Code and Codex.
- Do not change the remaining navigation, terminal sequence, page structure or footer links in this correction.
