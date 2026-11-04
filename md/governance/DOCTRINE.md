# Doctrine

> Status: template · 2026-11-04 · replace this body with the repo's own, or delete the file

**What this file is for.** What the repo holds to be true and what it
values: the principles its policies derive from and its architecture
serves. A doctrine statement is not checkable and nothing enforces it; it
is the reason a policy exists, and it is argued for in an analysis the
statement cites. When a doctrine changes, the policies that cited it are
reread.

**Belongs here:** each principle as one statement, numbered; the analysis
or source that argues it; the policies and architecture decisions that
rest on it.

**Does not:** a rule (`POLICY.md`); a description of what is built
(`ARCHITECTURE.md`); the argument itself (`../analysis/`); anything a tool
could check (then it is a policy with a check).

**Form.**

```
# Doctrine

> Status: held · YYYY-MM-DD

**T1. <the principle, as a statement that could be false>.** <one sentence
on what it means here>. *From:* <analysis or source>. *Serves:* P2, P7,
ARCHITECTURE D1.
```

In a repo that keeps a DAG of claims, each statement here is a claim and
this file is generated from them.
