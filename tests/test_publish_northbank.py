import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import publish_northbank as northbank  # noqa: E402


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout.strip()


class PublishNorthbankTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.repo, self.origin = base / "work", base / "origin.git"
        git(base, "init", "-q", "--template=", "--bare", str(self.origin))
        git(base, "init", "-q", "--template=", "-b", "main", str(self.repo))
        git(self.repo, "config", "user.name", "Pages Test")
        git(self.repo, "config", "user.email", "pages-test@example.com")
        git(self.repo, "remote", "add", "origin", str(self.origin))
        site = self.repo / northbank.SITE
        site.mkdir(parents=True)
        (site / "index.html").write_text("<h1>Fictional club</h1>\n", encoding="utf-8", newline="\n")
        (site / "styles.css").write_text("body { margin: 0 }\n", encoding="utf-8", newline="\n")
        (self.repo / "README.md").write_text("Not part of the site.\n", encoding="utf-8")
        (self.repo / ".gitignore").write_text(".work/\n", encoding="utf-8")
        git(self.repo, "add", "-A")
        git(self.repo, "-c", "commit.gpgsign=false", "commit", "-qm", "Fictional site")
        git(self.repo, "push", "-q", "origin", "main")
        self.head = git(self.repo, "rev-parse", "HEAD")

    def tearDown(self):
        self.tmp.cleanup()

    def publish(self, *args):
        with patch("sys.stdout"), patch("sys.stderr"):
            return northbank.main(list(args), repo=self.repo)

    def test_dry_run_builds_the_site_and_pushes_nothing(self):
        self.assertEqual(self.publish(), 0)
        built = self.repo / ".work" / "northbank" / "site"
        self.assertEqual(sorted(p.name for p in built.iterdir()),
                         [".nojekyll", "index.html", "release.json", "styles.css"])
        self.assertEqual(json.loads((built / "release.json").read_text(encoding="utf-8")), {"commit": self.head})
        self.assertEqual(git(self.origin, "branch", "--list", "gh-pages"), "")

    def test_publish_pushes_the_site_and_marker_to_gh_pages(self):
        self.assertEqual(self.publish("--publish"), 0)
        files = git(self.origin, "ls-tree", "-r", "--name-only", "gh-pages").splitlines()
        self.assertEqual(sorted(files), [".nojekyll", "index.html", "release.json", "styles.css"])
        marker = git(self.origin, "show", "gh-pages:release.json")
        self.assertEqual(marker, json.dumps({"commit": self.head}, separators=(",", ":")))
        self.assertEqual(git(self.origin, "show", "gh-pages:index.html"), "<h1>Fictional club</h1>")
        self.assertEqual(git(self.repo, "status", "--porcelain"), "")
        self.assertEqual(git(self.repo, "rev-parse", "--abbrev-ref", "HEAD"), "main")

    def test_publishing_the_same_commit_again_pushes_nothing_new(self):
        self.publish("--publish")
        first = git(self.origin, "rev-parse", "gh-pages")
        self.assertEqual(self.publish("--publish"), 0)
        self.assertEqual(git(self.origin, "rev-parse", "gh-pages"), first)

    def test_a_later_site_builds_on_the_published_branch(self):
        self.publish("--publish")
        first = git(self.origin, "rev-parse", "gh-pages")
        (self.repo / northbank.SITE / "index.html").write_text("<h1>Updated</h1>\n", encoding="utf-8")
        git(self.repo, "-c", "commit.gpgsign=false", "commit", "-qam", "Update the site")
        git(self.repo, "push", "-q", "origin", "main")
        self.assertEqual(self.publish("--publish"), 0)
        self.assertEqual(git(self.origin, "rev-parse", "gh-pages^"), first)

    def test_publishing_refuses_a_commit_that_is_not_on_main(self):
        (self.repo / "README.md").write_text("Local only.\n", encoding="utf-8")
        git(self.repo, "-c", "commit.gpgsign=false", "commit", "-qam", "Local change")
        self.assertEqual(self.publish("--publish"), 1)
        self.assertEqual(git(self.origin, "branch", "--list", "gh-pages"), "")


if __name__ == "__main__":
    unittest.main()
