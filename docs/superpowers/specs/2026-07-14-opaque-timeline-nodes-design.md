# Opaque Timeline Nodes Design

## Goal

Keep the timeline line fully hidden behind every numbered node from the initial state onward and correct capitalization in two repository-impact values.

## Root cause and fix

The node already uses the opaque `var(--bg)` background, but `.timeline-step` applies `opacity: 0.58` to the entire subtree. That makes the node background translucent and exposes the line beneath it.

Remove opacity and the pulse animation from `.timeline-step`. Keep the existing node-border and title animations, colors, timing, z-indexes, responsive layout and reduced-motion state unchanged. Do not add a pseudo-element or another isolation layer.

## Copy

- English: `Your source code` and `Nothing, by default`.
- Portuguese: `Seu código-fonte` and `Nada, por padrão`.

## Verification

- Browser coverage confirms every timeline step remains at opacity `1` during normal motion.
- Existing reduced-motion and five-color timeline coverage remains green.
- Locale validation confirms matching translation keys.
