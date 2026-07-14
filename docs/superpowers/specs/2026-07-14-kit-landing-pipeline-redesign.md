# Phoxia DevKit landing pipeline redesign

## Goal

Turn the landing page into a clear product narrative from repository context to verified change, while reducing repetition and giving each kind of information an appropriate visual treatment.

## Information architecture

Reduce the landing from twelve sections to eight:

1. Hero: product thesis, terminal demonstration and primary actions.
2. Problem: four concrete failures caused by missing project context.
3. DevKit pipeline: project context, assistant action and verified result.
4. Workflow: five ordered steps from initialization to synchronization.
5. Files and repository impact: generated files, verification output and the five effects on the repository.
6. Configuration and trust: setup modes plus local-behavior facts.
7. Profiles and workflows: official presets, named workflows and compact community-publishing status.
8. Installation: command, documentation and repository actions.

Remove the separate recommended-path section because it duplicates the five-step workflow. Merge the former evidence and help sections into the DevKit pipeline. Merge generated files and transparency. Merge setup modes and trust without making their component treatments identical.

## Visual system

Preserve the existing Phoxia palette, typefaces, spacing scale, light/dark themes and overall page identity. Avoid introducing another visual language or dependency.

Use distinct component families:

- Problem cards use a restrained icon tile, strong title and concise description. Use `BrainCircuit`, `Braces`, `FileWarning` and `BadgeAlert` for lost context, ignored conventions, stale documentation and unverified changes.
- The pipeline uses three larger connected nodes rather than generic cards. Project Context presents `.phoxia/project.yaml`; Assistant Action presents instruction reading; Verified Result presents visible checks. Lux appears at the end as supporting artwork, not as a pipeline step.
- File examples look like files: monospaced header, short representative content and restrained surface treatment.
- Setup modes read as operational choices. Add has a visible recommended status; Replace and Update retain their risk/maintenance meanings without looking interactive.
- Trust facts form a horizontal fact list with local execution, privacy and human approval icons, not another three-card grid.
- Profiles form a compact strip. Community publishing is a secondary `Coming soon` status rather than a full-size promotional card.

## Problem heading and Lux

The problem heading row spans the full section width. The text retains a readable maximum width, while the confused Lux sits against the far-right edge through `justify-content: space-between`. Do not apply a maximum width to the row itself.

On narrow screens, keep the title first and position Lux at the right edge beneath it without creating a large empty row.

## Workflow timeline and motion

The five workflow numbers sit directly on one continuous line. A luminous marker travels from left to right, briefly pulsing each numbered node and emphasizing its title. The sequence loops with a calm pause after the fifth step.

The timeline is the page's single signature motion. Other animation is limited to short section entrances and subtle hover feedback.

On mobile, the timeline becomes vertical and the marker travels downward. With `prefers-reduced-motion: reduce`, remove the moving marker and pulse, render all nodes in their completed visual state and preserve the full information hierarchy.

## Repository impact layout

Use a six-column grid for the five impact items:

- Create, Update and Preserve occupy two columns each in the first row.
- Remove and Backup occupy three columns each in the second row.

This `3 + 2` arrangement fills the available width and can return to an automatic responsive grid if future impact items are added. Tablet uses two columns where practical; mobile uses one column.

## Responsive contract

- Desktop uses the full section width for heading relationships, connected flows and repository-impact rows.
- Tablet changes four-card grids to two columns. Keep the pipeline horizontal only while its content remains readable.
- Mobile stacks cards, makes pipeline connectors vertical and converts the timeline to a vertical sequence.
- Avoid horizontal overflow at 390 px.
- Preserve minimum 44 px interactive targets, visible keyboard focus and sufficient contrast in both themes.

## Content contract

Keep public technical tokens and facts unchanged: commands, paths, target names, setup-mode behavior and URLs. Preserve English and Brazilian Portuguese coverage.

Remove copy only when it duplicates another landing section. Detailed configuration and profile material remains available through documentation links.

## Implementation constraints

- Use existing Svelte components, `lucide-svelte`, native CSS Grid and CSS animations.
- Add no dependencies and no speculative component abstraction.
- Keep the existing locale and theme stores, header, footer, terminal sequence and installation command behavior.
- Split a component only when it has a distinct reusable responsibility; do not create generic card abstractions solely to reduce markup.

## Verification

- Unit tests preserve the new eight-section inventory and immutable public tokens.
- Playwright verifies section count, content hierarchy, `3 + 2` impact layout, timeline structure, compact profiles, locale behavior and reduced-motion state.
- `svelte-check`, production build, locale validation and public-boundary validation pass.
- Visual inspection covers 1440 px, 768 px and 390 px in light and dark themes.
