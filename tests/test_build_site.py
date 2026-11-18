import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build_site as site  # noqa: E402


def render(text, links=None):
    seen = links if links is not None else []

    def fix(url, source, path):
        seen.append(url)
        return "FIXED:" + url

    page = site.Page("docs/guides/x.md", "guides/x.html", fix)
    return site.markdown(text, page), page


class MarkdownTests(unittest.TestCase):
    def test_headings_get_github_anchors_and_the_first_is_the_title(self):
        out, page = render("# Start here: a founder\n\n## Try one task (5 min)\n\n## Try one task (5 min)")
        self.assertIn('<h1 id="start-here-a-founder">', out)
        self.assertIn('id="try-one-task-5-min"', out)
        self.assertIn('id="try-one-task-5-min-1"', out)
        self.assertEqual(page.title, "Start here: a founder")

    def test_a_list_can_follow_a_paragraph_and_nest(self):
        out, _ = render("**Route 1.**\n1. One\n2. Two\n   - inner\n3. Three")
        self.assertIn("<p><strong>Route 1.</strong></p>\n<ol>", out)
        self.assertIn("<li>Two\n<ul>\n<li>inner</li>\n</ul></li>", out)
        self.assertEqual(out.count("<li>"), 4)

    def test_tables_code_quotes_and_details(self):
        text = ("| A | B |\n|---|:-:|\n| `x|y` | **b** |\n\n~~~text\n<raw> & co\n~~~\n\n> quoted\n\n"
                "<details>\n<summary>Compare</summary>\n\n1. Hold\n\n</details>")
        out, _ = render(text)
        self.assertIn('<div class="table"><table>', out)
        self.assertIn('<th style="text-align:center">B</th>', out)
        self.assertIn("<pre><code>&lt;raw&gt; &amp; co</code></pre>", out)
        self.assertIn("<blockquote>\n<p>quoted</p>\n</blockquote>", out)
        self.assertIn("<details>\n<summary>Compare</summary>\n<ol>", out)

    def test_raw_html_with_attributes_or_scripts_is_escaped(self):
        out, _ = render('<details open ontoggle="alert(1)"><script>alert(2)</script>\n\n'
                        "<summary><img src=x onerror=alert(3)></summary>")
        self.assertNotIn("<script", out)
        self.assertNotIn("<img", out)
        self.assertNotIn("<details open ontoggle", out)
        self.assertIn("&lt;details open ontoggle", out)

    def test_html_in_text_is_escaped_and_links_go_through_the_fixer(self):
        links = []
        out, _ = render("Use <b> and [the guide](../x.md#top) or [![logo](../images/a.svg)](https://e.org)", links)
        self.assertIn("&lt;b&gt;", out)
        self.assertEqual(links, ["../images/a.svg", "../x.md#top", "https://e.org"])
        self.assertIn('<a href="FIXED:https://e.org"><img src="FIXED:../images/a.svg"', out)


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name) / "site"

    def tearDown(self):
        self.tmp.cleanup()

    def test_builds_only_the_site_with_relative_links_and_a_marker(self):
        built = site.build(ROOT, self.out)
        files = {p.relative_to(self.out).as_posix() for p in self.out.rglob("*") if p.is_file()}
        self.assertIn("index.html", files)
        self.assertIn("examples/northbank/index.html", files)
        self.assertEqual({f for f in files if f.startswith("guides/")},
                         {f"guides/{name}.html" for _, group in site.GUIDES for name, _ in group} | {"guides/index.html"})
        self.assertFalse([f for f in files if f.endswith(".md") or f.endswith(".py")])
        marker = json.loads((self.out / "release.json").read_text(encoding="utf-8"))
        self.assertEqual(marker["commit"], built.commit)
        self.assertEqual(set(marker["files"]), files - {"release.json", site.BUILD_MARKER})
        self.assertNotIn(site.BUILD_MARKER, built.files)  # the local build marker is never published
        landing = (self.out / "index.html").read_text(encoding="utf-8")
        self.assertIn(f"{site.GITHUB}/releases/tag/v{built.version}", landing)
        self.assertIn("install.py --runtime claude", landing)
        self.assertNotIn('href="/', landing)

    def test_two_builds_are_identical(self):
        first = site.build(ROOT, self.out).files
        self.assertEqual(first, site.build(ROOT, self.out).files)

    def test_a_link_to_a_missing_file_stops_the_build(self):
        built = site.Site(ROOT, self.out, "1.0.0", "0" * 40, True)
        with self.assertRaisesRegex(site.BuildError, "points to nothing"):
            built.fix_link("../no-such-file.md", "docs/guides/x.md", "guides/x.html")

    def test_every_built_page_is_link_checked_including_copied_ones(self):
        built = site.Site(ROOT, self.out, "1.0.0", "0" * 40, True)
        built.files["guides/a.html"] = b'<h2 id="real">A</h2><a href="#real">ok</a>'
        built.files["index.html"] = b'<a href="guides/a.html#gone">x</a><a href="./">home</a>'
        built.files["examples/northbank/index.html"] = (b'<a href="missing.html">m</a><img src="/root.svg">'
                                                         b'<a href="javascript:alert(1)">j</a>')
        with self.assertRaises(site.BuildError) as caught:
            site.check_links(built)
        message = str(caught.exception)
        for expected in ("#gone", "missing.html", "/root.svg starts with a slash", "javascript:"):
            self.assertIn(expected, message)
        self.assertNotIn("./ leads", message)

    def test_unsafe_and_root_links_in_markdown_stop_the_build(self):
        built = site.Site(ROOT, self.out, "1.0.0", "0" * 40, True, tracked=site.tracked_files(ROOT))
        for url in ("javascript:alert(1)", "file:///C:/private/notes.txt", "/docs/x.md", "//evil.example/x"):
            with self.assertRaises(site.BuildError, msg=url):
                built.fix_link(url, "docs/guides/x.md", "guides/x.html")
        self.assertEqual(built.fix_link("mailto:a@example.org", "docs/guides/x.md", "guides/x.html"),
                         "mailto:a@example.org")

    def test_only_tracked_regular_files_are_copied(self):
        built = site.Site(ROOT, self.out, "1.0.0", "0" * 40, True,
                          tracked={"docs/images/shotos-mark.svg": "120000"})
        built.copies["images/shotos-mark.svg"] = "docs/images/shotos-mark.svg"
        with self.assertRaisesRegex(site.BuildError, "not a tracked regular file"):
            site.copy_files(built)
        built.tracked = {}
        with self.assertRaisesRegex(site.BuildError, "not a tracked regular file"):
            site.copy_files(built)

    def test_will_not_replace_a_folder_that_is_not_a_site_build(self):
        self.out.mkdir()
        (self.out / "keep.txt").write_text("mine", encoding="utf-8")
        (self.out / "release.json").write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(site.BuildError, "not an earlier site build"):
            site.build(ROOT, self.out)
        self.assertTrue((self.out / "keep.txt").exists())
        site.build(ROOT, self.out / "inner")
        site.build(ROOT, self.out / "inner")  # an earlier build carries the marker and is replaced

    def test_the_denylist_scan_reports_terms_without_printing_them(self):
        built = site.build(ROOT, self.out)
        denylist = Path(self.tmp.name) / "deny.txt"
        denylist.write_text("# test\nNorthbank\n", encoding="utf-8")
        hits = site.scan(built, denylist)
        self.assertTrue(hits)
        self.assertTrue(all("denylist line 2" in hit for hit in hits))
        self.assertFalse([hit for hit in hits if "Northbank" in hit])


if __name__ == "__main__":
    unittest.main()
