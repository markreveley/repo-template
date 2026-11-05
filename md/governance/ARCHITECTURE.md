# Architecture

> Status: template · 2026-11-04 · replace this body with the repo's own, or delete the file

**What this file is for.** How the thing is built: the parts, what flows
between them, where the boundaries are, and the decisions that shaped it
with their reasons. A reader who is about to change how the parts fit reads
this first. It describes what is built; where it describes a target instead,
the status line says so and names what gates the build.

**Belongs here:** the parts and their responsibilities; the data and
control flow between them; the interfaces at the boundaries; the invariants
the design keeps; each design decision with the alternatives considered and
why they lost; the milestones, if the architecture is being built in
stages.

**Does not:** how to use the thing (`../docs/`), the file formats
(`SCHEMA.md`), the rules of conduct (`POLICY.md`), the order of work
(`../plans/`).

**Form.**

```
# <name>: architecture

> Status: <draft vN | built> · YYYY-MM-DD · <describes what is built | the target, gated by ...>

## 1. Thesis
<one paragraph: what the thing is, in a sentence a reader can test the rest against>

## 2. Parts
## 3. Flow
## 4. Boundaries and invariants
## 5. Decisions
### D1. <decision>
<the choice, the alternatives, why>
```

Sections and decisions are numbered so other documents cite them
(`ARCHITECTURE §4`, `ARCHITECTURE D3`). A plan's decision, once accepted
and built, moves here under the next number.
