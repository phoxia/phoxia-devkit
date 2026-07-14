# Technology decision matrix

| Scenario | Strong defaults |
|---|---|
| Web frontend | TypeScript with React/Next.js or SvelteKit |
| General API | TypeScript/NestJS, Go, Java/Kotlin or C# |
| High-performance safe backend | Rust |
| Mobile native | Kotlin and Swift |
| Cross-platform mobile | Flutter or React Native |
| Desktop cross-platform | Rust/Tauri, Flutter or Electron |
| Windows business desktop | C#/.NET or Delphi |
| AI and ML | Python, with C++ or Rust for runtime performance |
| Data engineering | SQL with Python, Go or Rust |
| CLI | Rust or Go |
| OS, kernels and drivers | C and Rust |
| Bare-metal embedded | C, Rust, C++ or Ada/SPARK |
| Embedded Linux | C, C++, Rust, plus Go for user-space services |
| IoT prototypes | MicroPython or C++ |
| Games | C++, C#, GDScript or selected Rust stacks |
| Scientific computing | Python, Julia, R and native kernels |
| Automation | Python, Bash and PowerShell |

## Delphi

Delphi is not the default bare-metal embedded choice.

It is strong for Windows-native business software, VCL and FireMonkey applications, industrial tooling, database applications, existing Pascal teams and legacy integration.

Free Pascal can target some embedded platforms, but C, C++, Rust and Ada/SPARK usually have stronger hardware support, vendor tools, debuggers and real-time ecosystems.

## PostgreSQL

Use PostgreSQL as the general default, including pgvector when vector search belongs with transactional data.

Choose another store only for a durable requirement, such as local SQLite, specialized analytical scale, hard real-time storage or a graph workload that PostgreSQL cannot serve adequately.
