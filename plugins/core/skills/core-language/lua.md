# Lua

- Respect the target runtime: Lua, LuaJIT, Luau or embedded variants.
- Use local variables and modules; avoid accidental globals.
- Tables are both records and maps, so document shape and ownership.
- Use table dispatch for dynamic registries and conditionals for small cases.
- Avoid metatable magic that hides core behavior.
- Profile with runtime-specific tools and account for LuaJIT warmup.
- Test C bindings and resource lifetimes carefully.
