# Clojure

- Prefer immutable data and explicit transformations.
- Use protocols or multimethods when dispatch semantics require them.
- Avoid global mutable atoms as hidden application state.
- Watch lazy sequence retention and repeated realization.
- Use transducers only when profiling supports the complexity.
- Test with clojure.test and property tools used by the project.
- Keep Java interop boundaries explicit.
