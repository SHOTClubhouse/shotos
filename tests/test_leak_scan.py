import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import leak_scan  # noqa: E402

# Every term in this fixture is invented. Line 2 is a plain word, line 3 is case-insensitive,
# line 4 is a path and line 6 is a two-word name.
FIXTURE = ROOT / "tests" / "fixtures" / "leak-denylist.txt"
TERMS = ("Quillbury", "marrow lane", "fictional-owner", "Zentrix")


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout.strip()


class LeakScanTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        git(self.repo, "init", "-q", "--template=")
        git(self.repo, "config", "user.name", "Leak Test")
        git(self.repo, "config", "user.email", "leak-test@example.com")
        self.entries = leak_scan.load_denylist(FIXTURE)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, text):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def commit(self, message="fictional change"):
        git(self.repo, "add", "-A")
        git(self.repo, "-c", "commit.gpgsign=false", "commit", "-qm", message)
        return git(self.repo, "rev-parse", "HEAD")

    def cli(self, *args):
        env = {**os.environ, "SHOTOS_DENYLIST": ""}
        return subprocess.run([sys.executable, str(ROOT / "tools" / "leak_scan.py"), "--repo", str(self.repo), *args],
                              capture_output=True, text=True, env=env)

    def test_reads_each_kind_of_entry_with_its_line_number(self):
        self.assertEqual([(e.line, e.kind) for e in self.entries],
                         [(2, "word"), (3, "iword"), (4, "path"), (6, "word")])

    def test_plain_terms_are_whole_words_and_case_sensitive(self):
        hits = lambda text: [entry for _, entry in leak_scan.text_hits(text, self.entries)]
        self.assertEqual(hits("Visit Quillbury's office."), [2])
        self.assertEqual(hits("Quillburyshire and quillbury are different words."), [])
        self.assertEqual(hits("Sent by Zentrix Ltd."), [6])
        self.assertEqual(hits("Zentrix Ltda"), [])

    def test_case_insensitive_terms_match_any_case(self):
        self.assertEqual(leak_scan.text_hits("No 4, MARROW Lane", self.entries), [(1, 3)])
        self.assertEqual(leak_scan.text_hits("marrow lanes", self.entries), [])

    def test_path_terms_match_inside_words_and_with_any_slash(self):
        for text in ("see /home/fictional-owner/notes", "C:\\home\\fictional-owner\\notes",
                     '{"path": "\\\\home\\\\fictional-owner\\\\notes"}', "x/home/fictional-owner/y"):
            with self.subTest(text=text):
                self.assertEqual(leak_scan.text_hits(text, self.entries), [(1, 4)])

    def test_reports_file_line_and_denylist_line_but_never_the_term(self):
        self.write("docs/notes.md", "Line one.\nThe Quillbury office.\n")
        self.write("README.md", "Nothing private here.\n")
        self.write("untracked.md", "Quillbury\n")
        git(self.repo, "add", "docs/notes.md", "README.md")
        run = self.cli("--denylist", str(FIXTURE))
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertIn("docs/notes.md:2: denylist line 2", run.stdout)
        self.assertNotIn("untracked.md", run.stdout)
        for term in TERMS:
            self.assertNotIn(term, run.stdout + run.stderr)

    def test_a_clean_repository_passes_and_binary_files_are_counted(self):
        self.write("README.md", "Nothing private here.\n")
        (self.repo / "image.png").write_bytes(b"\x89PNG\0\0Quillbury")
        self.commit()
        run = self.cli("--denylist", str(FIXTURE))
        self.assertEqual(run.returncode, 0, run.stdout)
        self.assertIn("1 binary file(s) not read", run.stdout)

    def test_file_names_are_checked(self):
        self.write("people/zentrix ltd.md", "Fictional.\n")
        self.commit()
        hits, _ = leak_scan.scan_tree(self.repo, self.entries)
        self.assertEqual([h.describe() for h in hits], [])
        self.write("suppliers/Zentrix Ltd.md", "Fictional.\n")
        self.commit()
        hits, _ = leak_scan.scan_tree(self.repo, self.entries)
        self.assertEqual([h.describe() for h in hits], ["suppliers/Zentrix Ltd.md (file name): denylist line 6"])

    def test_history_finds_a_term_that_a_later_commit_removed(self):
        self.write("README.md", "Start.\n")
        base = self.commit()
        self.write("README.md", "Start.\nmarrow lane\n")
        added = self.commit()
        self.write("README.md", "Start.\n")
        self.commit("Remove the Quillbury line")
        result = leak_scan.scan(self.repo, self.entries, history=[[f"{base}..HEAD"]])
        found = [h.describe() for h in result["hits"]]
        self.assertIn(f"commit {added[:12]} README.md:2: denylist line 3", found)
        self.assertTrue(any(line.endswith("message line 1: denylist line 2") for line in found), found)
        self.assertEqual(leak_scan.scan(self.repo, self.entries)["hits"], [])

    def test_allowlist_names_a_file_and_a_denylist_line_only(self):
        self.write("MAINTAINERS.md", "Quillbury\nmarrow lane\n")
        self.write("tools/leak-allowlist.txt", "# Deliberate public uses\nMAINTAINERS.md 2\nREADME.md 6\n")
        self.commit()
        run = self.cli("--denylist", str(FIXTURE))
        self.assertEqual(run.returncode, 1)
        self.assertNotIn("denylist line 2", run.stdout.split("note:")[0])
        self.assertIn("MAINTAINERS.md:2: denylist line 3", run.stdout)
        self.assertIn("1 allowed by the allowlist", run.stdout)
        self.assertIn("allowlist entry README.md 6 no longer matches anything", run.stdout)

    def test_an_allowlist_line_holding_anything_else_is_refused(self):
        self.write("allow.txt", "MAINTAINERS.md Quillbury\n")
        self.commit()
        run = self.cli("--denylist", str(FIXTURE), "--allowlist", str(self.repo / "allow.txt"))
        self.assertEqual(run.returncode, 2)
        self.assertNotIn("Quillbury", run.stdout + run.stderr)

    def test_no_denylist_means_the_scan_cannot_run(self):
        run = self.cli()
        self.assertEqual(run.returncode, 2)
        self.assertIn("SHOTOS_DENYLIST", run.stderr)
        self.assertIsNone(leak_scan.denylist_path(str(self.repo / "missing.txt")))

    def test_redact_withholds_whole_matching_lines(self):
        text = "Safe line.\nFrom the Quillbury office.\n"
        self.assertEqual(leak_scan.redact(text, self.entries),
                         "Safe line.\n[withheld: matches denylist line 2]\n")


if __name__ == "__main__":
    unittest.main()
