---
type: handoff
updated: 2026-11-25
---

# Next

> The ordered list of what's next, and nothing else. What is true now is in `state.md`. The first open step is mirrored in direction's `repo-manifest.md`: change this file with `/update-next`, or run it after a hand edit (R30).

1. **(agent)** Migrate every active client repo in direction's `repo-manifest.md` to the current rules: in each, run `/client-sync --migrate`, then `/update-next` (which merges old handoff files and moves State into `state.md`), then `/check-layout` until it passes. Skip the deprecated repos `_do`, `evals-cb`, `thread-archive` and `tuts`.
   - Old `next-agents.md` and `next-operator.md`: ableton-claude, agent-context-files-local, artifact-dag, investigations, mark-reveley-site.
   - investigations also keeps its working material at the root, in `in-progress/<topic>/`: move it into the `md/` folders it belongs in (plans, analysis, docs) and repoint links. Its `posted/` and `templates/` are content, and stay.
   - State inside `next.md`: dotfiles, bookmarks, orchestrator, thread-based-dag, voice-agent-prototype.
   - No handoff yet: artifact-todo, bias-buster, channels, direction, eval-workshop, how-does-it-work, interpretability, manifold, manifold-mark, socrates.
