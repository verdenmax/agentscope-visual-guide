# Developer docs — AgentScope Visual Guide generator

Layered documentation for the **generator** (the `src/` Python that builds the site).
The *product* (the lessons) lives in `lessons/` + `index.html`; this folder documents
the *code that produces it*.

| Layer | File | Scope |
|-------|------|-------|
| **L1** | [L1-overview.md](L1-overview.md) | What the generator is + the end-to-end build flow |
| **L2** | [L2-components.md](L2-components.md) | Each module's responsibility & public interface |
| **L3** | [L3-details.md](L3-details.md) | Bilingual mechanism, DSL semantics, highlighter, CSS, CI |
| **L4** | [L4-api/](L4-api/) | Per-file API reference (one file per source module) |

The design spec and implementation plan live under [`../superpowers/`](../superpowers/).
