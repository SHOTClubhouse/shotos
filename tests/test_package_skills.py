import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

TOOL = Path(__file__).resolve().parents[1] / "tools" / "package_skills.py"


class PackageSkillsTests(unittest.TestCase):
    def assert_markdown_links_resolve(self, archive):
        names = set(archive.namelist())
        for name in sorted(names):
            if not name.endswith(".md"):
                continue
            fence = None
            for line in archive.read(name).decode("utf-8").splitlines():
                marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
                if marker:
                    delimiter = marker[1]
                    if fence is None:
                        fence = delimiter
                    elif delimiter[0] == fence[0] and len(delimiter) >= len(fence):
                        fence = None
                    continue
                if fence:
                    continue
                for destination in re.findall(r"\]\(([^)\s]+)\)", line):
                    link = urlsplit(destination)
                    if link.scheme or link.netloc or not link.path:
                        continue
                    target = posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(link.path)))
                    exists = target in names or any(member.startswith(target + "/") for member in names)
                    self.assertTrue(exists, f"{name} links to missing {destination}")

    def test_linked_source_cannot_enter_a_skill_zip(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            repo = workspace / "repo"
            tools = repo / "tools"
            tools.mkdir(parents=True)
            for source in (TOOL, TOOL.with_name("skill_resources.py")):
                shutil.copy2(source, tools)
            skill = repo / "skills" / "sample"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("# Sample", encoding="utf-8")
            for name in ("LICENSE", "LICENSE-docs.md"):
                (repo / name).write_text("Fictional licence fixture", encoding="utf-8")
            outside = workspace / "private-fixture.txt"
            outside.write_text("Synthetic content outside the source checkout", encoding="utf-8")
            try:
                (skill / "linked.txt").symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks are not available here")
            out = workspace / "out"
            result = subprocess.run([sys.executable, str(tools / TOOL.name), "--out", str(out)],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertIn("linked package source", result.stderr)
            self.assertFalse((out / "sample.zip").exists())

    def fixture_repo(self, workspace: Path, files: dict) -> Path:
        repo = workspace / "repo"
        tools = repo / "tools"
        tools.mkdir(parents=True)
        for source in (TOOL, TOOL.with_name("skill_resources.py")):
            shutil.copy2(source, tools)
        for name in ("LICENSE", "LICENSE-docs.md"):
            (repo / name).write_text("Fictional licence fixture", encoding="utf-8")
        for name, content in files.items():
            (repo / name).parent.mkdir(parents=True, exist_ok=True)
            (repo / name).write_bytes(content)
        return repo

    def test_links_that_leave_a_skill_zip_point_at_the_pinned_source(self):
        source_commit = "c" * 40
        template = b"# Template\r\n\r\nFill in [the case](scenarios/case.md).\r\n"
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.fixture_repo(Path(tmp), {
                "docs/controls.md": b"# Controls",
                "skills/other/SKILL.md": b"# Other",
                "skills/sample/SKILL.md": b"# Sample\n\nUse [the template](template.md), then [other](../other/SKILL.md).\n",
                "skills/sample/template.md": template,
                "skills/sample/scenarios/case.md":
                    b"Back to [the template](../template.md). See [rule 1](../../../docs/controls.md#rule-1).\n",
            })
            out = Path(tmp) / "out"
            subprocess.run([sys.executable, str(repo / "tools" / TOOL.name), "--out", str(out),
                            "--source-commit", source_commit], check=True, capture_output=True)
            source = f"https://github.com/SHOTClubhouse/shotos/blob/{source_commit}"
            with zipfile.ZipFile(out / "sample.zip") as archive:
                self.assertEqual({name.split("/")[0] for name in archive.namelist()}, {"sample"})
                skill = archive.read("sample/SKILL.md").decode("utf-8")
                self.assertIn("(template.md)", skill)
                self.assertIn(f"({source}/skills/other/SKILL.md)", skill)
                case = archive.read("sample/scenarios/case.md").decode("utf-8")
                self.assertIn("(../template.md)", case)
                self.assertIn(f"({source}/docs/controls.md#rule-1)", case)
                self.assertEqual(archive.read("sample/template.md"), template)
                self.assert_markdown_links_resolve(archive)

    def test_a_broken_zip_link_stops_the_build(self):
        broken = {
            "missing local file": (b"Use [the template](template.md).\n", "template.md"),
            "unpinned repository link": (
                b"See [controls](https://github.com/SHOTClubhouse/shotos/blob/main/docs/controls.md).\n", "main"),
            "missing repository file": (b"See [the guide](../../docs/gone.md).\n", "docs/gone.md"),
        }
        for case, (skill, reported) in broken.items():
            with self.subTest(case=case), tempfile.TemporaryDirectory() as tmp:
                repo = self.fixture_repo(Path(tmp), {"skills/sample/SKILL.md": b"# Sample\n\n" + skill})
                out = Path(tmp) / "out"
                result = subprocess.run([sys.executable, str(repo / "tools" / TOOL.name), "--out", str(out),
                                         "--source-commit", "d" * 40], capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("sample.zip has broken links", result.stderr)
                self.assertIn(reported, result.stderr)
                self.assertFalse((out / "sample.zip").exists())

    def test_each_zip_holds_one_skill_folder_with_skill_md(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(TOOL), "--all-packs", "--out", tmp],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            zips = sorted(Path(tmp).glob("*.zip"))
            repo = TOOL.parents[1]
            sources = [*repo.glob("skills/*/SKILL.md"), *repo.glob("packs/*/skills/*/SKILL.md")]
            self.assertCountEqual((z.stem for z in zips), (source.parent.name for source in sources))
            by_name = {source.parent.name: source for source in sources}
            for z in zips:
                with zipfile.ZipFile(z) as archive:
                    names = archive.namelist()
                    self.assertIsNone(archive.testzip())
                    self.assertEqual(len(names), len(set(names)), z.name)
                    top = {n.split("/")[0] for n in names}
                    self.assertEqual(top, {z.stem})
                    self.assertEqual(archive.read(f"{z.stem}/SKILL.md"), by_name[z.stem].read_bytes())
                    self.assertTrue(all(entry.date_time == (1980, 1, 1, 0, 0, 0) for entry in archive.infolist()))
                    self.assertIn(f"{z.stem}/example-input.md", names)
                    self.assertIn(f"{z.stem}/example-output.md", names)
                    self.assertIn(f"{z.stem}/LICENSE-docs.md", names)
                    self.assertIn(f"{z.stem}/LICENSE", names)
                    self.assert_markdown_links_resolve(archive)

    def test_executive_review_travels_with_decision_brief(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            repo = TOOL.parents[1]
            subprocess.run([sys.executable, str(repo / "install.py"), "--runtime", "claude",
                            "--scope", "project", "--target", tmp, "--pack", "exec-ops"],
                           check=True, capture_output=True)
            subprocess.run([sys.executable, str(TOOL), "--pack", "exec-ops", "--out", tmp],
                           check=True, capture_output=True)
            installed = target / ".claude" / "skills" / "decision-brief"
            workflow = (installed / "review-cycle.md").read_bytes()
            self.assertIn("(review-cycle.md)", (installed / "SKILL.md").read_text(encoding="utf-8"))
            with zipfile.ZipFile(target / "decision-brief.zip") as archive:
                self.assertEqual(archive.read("decision-brief/review-cycle.md"), workflow)
                desktop_guide = archive.read("decision-brief/guides/codex-claude-code.md")
                self.assertIn(b"(chat-assistants.md#run-the-retail-scenario)", desktop_guide)
                chat_guide = archive.read("decision-brief/guides/chat-assistants.md")
                for name in ("retail-trial", "bank-remediation", "startup-proposal"):
                    with self.subTest(scenario=name):
                        relative = f"scenarios/{name}.md"
                        self.assertIn(f"({relative})", workflow.decode("utf-8"))
                        content = (installed / relative).read_bytes()
                        self.assertIn(b"Fictional scenario", content)
                        self.assertEqual(archive.read(f"decision-brief/{relative}"), content)
                        if name != "retail-trial":
                            for phase in ("initial", "follow-up"):
                                filename = f"{name}-{phase}.md"
                                input_path = f"scenarios/{filename}"
                                self.assertIn(f"({filename})".encode("ascii"), content)
                                self.assertIn(f"(../{input_path})".encode("ascii"), chat_guide)
                                self.assertEqual(archive.read(f"decision-brief/{input_path}"),
                                                 (installed / input_path).read_bytes())
                retail_example = (installed / "scenarios/retail-trial.md").read_text(encoding="utf-8")
                for phase, record_ids in (("initial", [b"1", b"2", b"3"]),
                                          ("follow-up", [b"4", b"5", b"6"])):
                    with self.subTest(phase=phase):
                        name = f"retail-trial-{phase}.md"
                        self.assertIn(f"({name})", retail_example)
                        relative = f"scenarios/{name}"
                        content = (installed / relative).read_bytes()
                        self.assertEqual(archive.read(f"decision-brief/{relative}"), content)
                        self.assertIn(f"(../{relative})".encode("ascii"), chat_guide)
                        self.assertEqual(re.findall(rb"(?m)^- \*\*R([1-6]),", content), record_ids)

    def test_proposal_resources_travel_in_both_skill_zips(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable, str(TOOL), "--pack", "win-the-work",
                            "--pack", "customer-success", "--out", tmp],
                           check=True, capture_output=True)
            target = Path(tmp)
            with zipfile.ZipFile(target / "contextual-proposal.zip") as proposal, \
                    zipfile.ZipFile(target / "success-handoff.zip") as handoff:
                for name in ("worked-deal.md", "organisation-templates.md", "template.md"):
                    with self.subTest(resource=name):
                        self.assertEqual(proposal.read(f"contextual-proposal/{name}"),
                                         handoff.read(f"success-handoff/proposal/{name}"))
                self.assertIn(b"(proposal/worked-deal.md)", handoff.read("success-handoff/README.md"))

    def test_release_zip_pins_repository_links_and_keeps_bundled_links_local(self):
        source_commit = "b" * 40
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable, str(TOOL), "--pack", "exec-ops",
                            "--source-commit", source_commit, "--out", tmp],
                           check=True, capture_output=True)
            with zipfile.ZipFile(Path(tmp) / "decision-brief.zip") as archive:
                guide = archive.read("decision-brief/guides/chat-assistants.md")
                self.assertIn(f"/blob/{source_commit}/templates/AGENTS.md".encode("ascii"), guide)
                self.assertIn(b"(../scenarios/retail-trial-initial.md)", guide)
                self.assertIn("decision-brief/scenarios/retail-trial-initial.md", archive.namelist())
            with zipfile.ZipFile(Path(tmp) / "graduation-ladder.zip") as archive:
                example = archive.read("graduation-ladder/example-output.md")
                self.assertIn(f"/blob/{source_commit}/skills/skill-quality-gate/README.md".encode("ascii"), example)

    def test_unknown_pack_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(TOOL), "--pack", "no-such-pack", "--out", tmp],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
