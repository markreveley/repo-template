"""Tests for bin/check_layout.py and bin/client_sync.py, in throwaway repos. Run: python3 -m unittest discover tests"""
import contextlib
import io
import os
import re
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, os.path.join(HERE, "bin"))
import check_layout  # noqa: E402
import client_sync  # noqa: E402


def run(mod, *args):
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
        code = mod.main(list(args))
    return code, out.getvalue()


def write(root, rel, text):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(text)


class ClientRepo(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root)

    def findings(self):
        code, out = run(check_layout, self.root)
        return code, [l for l in out.splitlines() if not l.endswith("finding(s)") and l != "layout ok"]

    def test_init_gives_a_passing_repo(self):
        self.assertEqual(run(client_sync, "--init", self.root)[0], 0)
        code, found = self.findings()
        self.assertEqual((code, found), (0, []))
        for f in ("README.md", "AGENTS.md", "CLAUDE.md", "state.md", "next.md", ".gitignore", "md/plans/README.md"):
            self.assertTrue(os.path.isfile(os.path.join(self.root, f)), f)
        self.assertFalse(os.path.exists(os.path.join(self.root, "md/governance/POLICY.md")))

    def test_init_does_not_overwrite(self):
        write(self.root, "README.md", "mine\n")
        run(client_sync, "--init", self.root)
        with open(os.path.join(self.root, "README.md")) as f:
            self.assertEqual(f.read(), "mine\n")

    def test_empty_dir(self):
        code, found = self.findings()
        self.assertEqual(code, 1)
        self.assertIn("missing at root: next.md", found)
        self.assertIn("no md/ folder", found)

    def test_dated_lines(self):
        run(client_sync, "--init", self.root)
        write(self.root, "state.md", "---\ntype: handoff\nupdated: 2026-11-25\n---\n\n# State\n\n"
              "- On 2026-11-25 the bridge was rebuilt.\n"
              "- Moved here by session_019EzEoMb71e8tRnf.\n"
              "- The plan is md/plans/2026-11-23-derived-index/derived-index.md.\n"
              "- The grant closes December 1. <!-- dated -->\n"
              "```\ngit log --since=2026-11-01\n```\n")
        code, found = self.findings()
        self.assertEqual(code, 1)
        self.assertEqual([f.split(":")[1] for f in found], ["8", "9"])

    def test_old_handoff_pair(self):
        run(client_sync, "--init", self.root)
        os.remove(os.path.join(self.root, "next.md"))
        write(self.root, "next-agents.md", "x")
        write(self.root, "next-operator.md", "x")
        found = self.findings()[1]
        self.assertEqual(len([f for f in found if "old handoff files" in f]), 1)
        self.assertFalse(any(f.startswith("loose document") for f in found))

    def test_leftover_beside_next(self):
        run(client_sync, "--init", self.root)
        write(self.root, "next-agents.md", "x")
        self.assertEqual(self.findings()[1], ["leftover handoff file: next-agents.md (merge its steps into next.md and its state into state.md with /update-next, then delete it; R30)"])

    def test_state_still_in_agents(self):
        run(client_sync, "--init", self.root)
        os.remove(os.path.join(self.root, "state.md"))
        write(self.root, "AGENTS.md", "# x\n\n## State\n\n- y\n")
        found = self.findings()[1]
        self.assertTrue(any("move the State" in f and "AGENTS.md" in f for f in found), found)

    def test_readme_without_link(self):
        run(client_sync, "--init", self.root)
        write(self.root, "md/plans/README.md", "# plans/\n")
        self.assertEqual(len([f for f in self.findings()[1] if "does not link" in f]), 1)

    def test_migrate_strips_pins_and_empty_governing_docs(self):
        run(client_sync, "--init", self.root)
        pin = "\n---\n\n<!-- pinned from repo-template md/plans/README.md @ abc1234; refresh -->\n## About this folder\ntext\n"
        write(self.root, "md/plans/README.md", "# plans/\n\nOurs.\n" + pin)
        write(self.root, "md/governance/POLICY.md", "# Policy\n" + pin)
        write(self.root, "md/governance/SCHEMA.md", "# Schema\n\nReal content.\n" + pin)
        self.assertTrue(any("pinned template block" in f for f in self.findings()[1]))
        run(client_sync, "--migrate", self.root)
        with open(os.path.join(self.root, "md/plans/README.md")) as f:
            text = f.read()
        self.assertIn("Ours.", text)
        self.assertNotIn("pinned from", text)
        self.assertIn("template/md/plans/README.md", text)
        self.assertFalse(os.path.exists(os.path.join(self.root, "md/governance/POLICY.md")))
        with open(os.path.join(self.root, "md/governance/SCHEMA.md")) as f:
            self.assertEqual(f.read(), "# Schema\n\nReal content.\n")
        self.assertEqual(self.findings(), (0, []))

    def test_sync_report_and_mark(self):
        run(client_sync, "--init", self.root)
        self.assertEqual(run(client_sync, self.root)[0], 0)
        try:
            older = client_sync.git("rev-parse", "HEAD~5").strip()
        except RuntimeError:
            self.skipTest("repo-template clone is too shallow; fetch more history")
        client_sync.write_sync_record(self.root, older)
        code, out = run(client_sync, "--names", self.root)
        self.assertEqual(code, 1)
        self.assertIn("changed ", out)
        self.assertTrue(any("changed since" in f for f in self.findings()[1]))
        self.assertEqual(run(client_sync, "--mark", self.root)[0], 0)
        self.assertEqual(client_sync.synced_commit(self.root), client_sync.head())


class ThisRepo(unittest.TestCase):
    def test_repo_template_passes(self):
        self.assertEqual(run(check_layout, HERE)[0], 0)

    def test_readme_table_matches_checks(self):
        with open(os.path.join(HERE, "README.md")) as f:
            m = re.search(r"<!-- checks:start -->\n(.*?)\n<!-- checks:end -->", f.read(), re.S)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1).strip(), check_layout.table())


if __name__ == "__main__":
    unittest.main()
