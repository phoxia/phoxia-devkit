# Direct lookup and dispatch

Use object, hash or map lookup when behavior is homogeneous and data-driven.

Use exhaustive language constructs when the state set is closed and domain branches differ.

TypeScript example:

```ts
type Action = "a" | "b";

const handlers = {
  a: () => doA(),
  b: () => doB(),
} satisfies Record<Action, () => void>;

handlers[action]();
```

Validate untrusted string keys.

Use `Map` for runtime registration, non-string keys or frequent mutation.

Rust usually prefers `match` for enums. Go uses `switch` for static dispatch. C and C++ compilers may turn switches into jump tables. Delphi uses `case` for closed enums.

No dispatch form is universally faster. Measure real workloads.
