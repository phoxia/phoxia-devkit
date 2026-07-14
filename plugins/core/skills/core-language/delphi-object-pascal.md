# Delphi and Object Pascal

Delphi is strongest for Windows-native business applications, VCL and FireMonkey interfaces, industrial tools, database software, existing Pascal teams and legacy integration.

It is not the default bare-metal embedded technology.

Free Pascal can target selected embedded platforms, but C, C++, Rust and Ada/SPARK usually have stronger hardware support, vendor libraries, debuggers, real-time ecosystems and safety tools.

Use `case` for closed enum dispatch. Use `TDictionary<Key, TProc>` or method references for dynamic registries.

Use `try..finally` for deterministic cleanup. Avoid `with`. Make object ownership and interface reference counting explicit.
