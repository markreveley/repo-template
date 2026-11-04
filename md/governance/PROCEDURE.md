# Procedure

> Status: template · 2026-11-04 · replace this body with the repo's own, or delete the file

**What this file is for.** The step-by-step methods the repo runs: how a
release is cut, how a pilot is run, how a document is decomposed, how a
finding is ratified. A procedure is followed in order, by a person or an
agent, and each step says which. A procedure under test (a pilot) says so
in its status and is not adopted until it says it is.

**Belongs here:** each procedure with its roles, its inputs, its numbered
steps, what each step produces, and how a step that fails is retried or
sent back; the tools that run the steps.

**Does not:** the rules the procedure satisfies (`POLICY.md`, cited by
number); the results of running it (`../analysis/` or the pilot's own
folder); the next thing to do (`next-agents.md`).

**Form.**

```
# Procedure: <name>

> Status: <under test in ... | adopted YYYY-MM-DD>

## Roles
| role | does | sees | does not see |

## Steps
1. **<verb>.** <who does it; what it produces; what sends it back>
```

Procedures are numbered within the file (`PROC-2`) when there is more than
one, so policies and plans cite them.
