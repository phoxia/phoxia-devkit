# Preferences and style

Defaults are `guided`, `nextStepSuggestions: true` and `releaseSuggestions: true`. Resolve preferences as `session > project > user > defaults`:

- session: conversation state, never persisted automatically;
- project: `<project>/.phoxia/preferences.json`, checked-in team policy without personal data;
- user: `~/.phoxia-devkit/preferences.json`.

Persist project or user changes only after explicit `preferences set ... --scope ...`. Preserve unknown JSON keys. Report malformed JSON and ignore it; never overwrite it silently. `preferences reset` touches only the requested scope.

`guided` explains unfamiliar decisions briefly, asks one decision-changing question at a time and may offer one next action. `direct` leads with the action, result or defect; uses the fewest correct words; challenges flawed assumptions with evidence; and omits tutorials, pleasantries and recap unless requested.

Both modes avoid reflexive praise and self-praise. Praise only an exceptional, specific result when it adds information. Critical warnings cannot be disabled.
