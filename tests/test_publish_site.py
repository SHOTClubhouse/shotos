import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build_site  # noqa: E402
import publish_site as publisher  # noqa: E402


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout.strip()


class PublishSiteTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.repo, self.origin = base / "work", base / "origin.git"
        git(base, "init", "-q", "--template=", "--bare", str(self.origin))
        git(base, "init", "-q", "--template=", "-b", "main", str(self.repo))
        git(self.repo, "config", "user.name", "Pages Test")
        git(self.repo, "config", "user.email", "pages-test@example.com")
        git(self.repo, "remote", "add", "origin", str(self.origin))
        (self.repo / "README.md").write_text("Source, not part of the site.\n", encoding="utf-8")
        git(self.repo, "add", "-A")
        git(self.repo, "-c", "commit.gpgsign=false", "commit", "-qm", "Fictional source")
        git(self.repo, "push", "-q", "origin", "main")
        self.head = git(self.repo, "rev-parse", "HEAD")
        self.files = {"index.html": b"<h1>Site</h1>\n", "guides/a.html": b"<p>A</p>\n", "release.json": b"{}\n"}

    def tearDown(self):
        self.tmp.cleanup()

    def publish(self, *args, files=None):
        site = SimpleNamespace(files=files or self.files, commit=git(self.repo, "rev-parse", "HEAD"), clean=True)
        with patch.object(publisher, "checked_build", return_value=site), patch("sys.stdout"), patch("sys.stderr"):
            return publisher.main(list(args), repo=self.repo)

    def published(self):
        return sorted(git(self.origin, "ls-tree", "-r", "--name-only", "gh-pages").splitlines())

    def test_dry_run_pushes_nothing(self):
        self.assertEqual(self.publish(), 0)
        self.assertEqual(git(self.origin, "branch", "--list", "gh-pages"), "")

    def test_publish_pushes_only_the_built_files(self):
        self.assertEqual(self.publish("--publish"), 0)
        self.assertEqual(self.published(), [".nojekyll", "guides/a.html", "index.html", "release.json"])
        self.assertEqual(git(self.origin, "show", "gh-pages:index.html"), "<h1>Site</h1>")
        self.assertIn(self.head, git(self.origin, "log", "-1", "--format=%s", "gh-pages"))
        self.assertEqual(git(self.repo, "status", "--porcelain"), "")
        self.assertEqual(git(self.repo, "rev-parse", "--abbrev-ref", "HEAD"), "main")

    def test_publishing_the_same_site_again_pushes_nothing_new(self):
        self.publish("--publish")
        first = git(self.origin, "rev-parse", "gh-pages")
        self.assertEqual(self.publish("--publish"), 0)
        self.assertEqual(git(self.origin, "rev-parse", "gh-pages"), first)

    def test_a_later_site_replaces_files_and_builds_on_the_branch(self):
        self.publish("--publish")
        first = git(self.origin, "rev-parse", "gh-pages")
        self.assertEqual(self.publish("--publish", files={"index.html": b"<h1>New</h1>\n"}), 0)
        self.assertEqual(git(self.origin, "rev-parse", "gh-pages^"), first)
        self.assertEqual(self.published(), [".nojekyll", "index.html"])

    def test_refuses_a_commit_that_is_not_on_main(self):
        (self.repo / "README.md").write_text("Local only.\n", encoding="utf-8")
        git(self.repo, "-c", "commit.gpgsign=false", "commit", "-qam", "Local change")
        self.assertEqual(self.publish("--publish"), 1)
        self.assertEqual(git(self.origin, "branch", "--list", "gh-pages"), "")


class CheckedBuildTests(unittest.TestCase):
    def site(self, clean):
        return build_site.Site(ROOT, ROOT / ".work" / "site", "1.0.0", "0" * 40, clean)

    def test_refuses_uncommitted_sources(self):
        with patch.object(build_site, "build", return_value=self.site(False)):
            with self.assertRaisesRegex(publisher.Stopped, "uncommitted"):
                publisher.checked_build(ROOT, None)

    def test_refuses_without_a_denylist(self):
        with patch.object(build_site, "build", return_value=self.site(True)), \
                patch.dict("os.environ", {"SHOTOS_DENYLIST": ""}):
            with self.assertRaisesRegex(publisher.Stopped, "no denylist"):
                publisher.checked_build(ROOT, None)

    def test_refuses_private_terms_in_the_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            denylist = Path(tmp) / "deny.txt"
            denylist.write_text("Secretterm\n", encoding="utf-8")
            site = self.site(True)
            site.files["index.html"] = b"<p>Secretterm</p>\n"
            with patch.object(build_site, "build", return_value=site):
                with self.assertRaisesRegex(publisher.Stopped, "denylist line 1") as caught:
                    publisher.checked_build(ROOT, str(denylist))
            self.assertNotIn("Secretterm", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
