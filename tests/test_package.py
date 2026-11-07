import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE = [p for p in ROOT.rglob("*") if p.is_file()
           and not any(part in {".git", ".work", "__pycache__"} for part in p.parts)
           and p.suffix in {".md", ".py", ".json", ".cff", ".yml", ".txt", ".gs", ".js", ".sh"}
           and p.name not in {"release_terms.sha256", "test_package.py"}]
PRIVATE_TERMS = ROOT / "tests/release_terms.sha256"
BANNED = ({line.strip() for line in PRIVATE_TERMS.read_text(encoding="utf-8").splitlines()
           if line.strip() and not line.startswith("#")} if PRIVATE_TERMS.is_file() else set())


def phrases(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    for size in range(1, 5):
        for i in range(len(words) - size + 1):
            yield " ".join(words[i:i + size])


class PackageTests(unittest.TestCase):
    def all_cases(self):
        files = [ROOT / "evals/cases.json"] + sorted((ROOT / "evals").glob("core/*.json")) + sorted((ROOT / "evals").glob("packs/*.json"))
        cases = []
        for f in files:
            cases += json.loads(f.read_text(encoding="utf-8"))["cases"]
        return cases

    def all_skills(self):
        """(skill folder, examples folder) for core skills and every pack skill."""
        found = [(p, ROOT / "examples" / p.name) for p in (ROOT / "skills").iterdir() if p.is_dir()]
        for pack in sorted((ROOT / "packs").iterdir()) if (ROOT / "packs").is_dir() else []:
            if (pack / "skills").is_dir():
                found += [(p, pack / "examples" / p.name) for p in (pack / "skills").iterdir() if p.is_dir()]
        return sorted(found)

    def test_every_skill_has_valid_frontmatter_readme_example_and_cases(self):
        cases = self.all_cases()
        skills = self.all_skills()
        self.assertGreaterEqual(len(skills), 4)
        for skill, examples in skills:
            with self.subTest(skill=skill.name):
                text = (skill / "SKILL.md").read_text(encoding="utf-8")
                self.assertTrue(text.startswith("---\n"))
                front = text.split("---", 2)[1]
                self.assertEqual(re.search(r"^name: (.+)$", front, re.M).group(1).strip(), skill.name)
                description = re.search(r"^description: (.+)$", front, re.M).group(1)
                self.assertLessEqual(len(description), 1024)
                readme = (skill / "README.md").read_text(encoding="utf-8")
                for label in ("Evidence", "Needs"):
                    self.assertRegex(readme, rf"(?im)^\s*(?:#+\s+|\*\*){label}\b")
                self.assertTrue((examples / "output.md").is_file())
                kinds = {c["type"] for c in cases if c["skill"] == skill.name}
                self.assertEqual(kinds, {"normal", "contrary"})

    def test_skill_names_are_unique(self):
        names = [skill.name for skill, _ in self.all_skills()]
        self.assertEqual(sorted(names), sorted(set(names)))

    def test_case_ids_are_unique_and_well_formed(self):
        cases = self.all_cases()
        ids = [c["id"] for c in cases]
        self.assertEqual(len(ids), len(set(ids)))
        for c in cases:
            with self.subTest(case=c["id"]):
                self.assertIn(c["type"], {"normal", "contrary"})
                self.assertTrue(c["prompt"].strip())
                self.assertIsInstance(c["must_contain"], list)
                self.assertIsInstance(c["must_not_contain"], list)

    def test_every_pack_has_readme_and_plugin_manifest(self):
        for pack in sorted(p for p in (ROOT / "packs").iterdir() if p.is_dir()):
            with self.subTest(pack=pack.name):
                self.assertTrue((pack / "README.md").is_file())
                manifest = json.loads((pack / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
                self.assertEqual(manifest["name"], f"shotos-{pack.name}")
        market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        listed = {p["name"] for p in market["plugins"]}
        for pack in (p for p in (ROOT / "packs").iterdir() if p.is_dir()):
            self.assertIn(f"shotos-{pack.name}", listed)

    def test_skill_frontmatter_is_valid_yaml(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed")
        skills = list((ROOT / "skills").glob("*/SKILL.md")) + list((ROOT / "packs").glob("*/skills/*/SKILL.md"))
        for skill in skills:
            with self.subTest(skill=skill.parent.name):
                front = skill.read_text(encoding="utf-8").split("---")[1]
                data = yaml.safe_load(front)
                self.assertEqual(data["name"], skill.parent.name)
                self.assertLessEqual(len(data["description"].split()), 45)

    def test_skill_links_survive_a_flat_install(self):
        # Installed skills sit side by side, so a link may only reach a sibling skill.
        link = re.compile(r"\]\(((?:\.\./)+)([^)]*)\)")
        skills = list((ROOT / "skills").glob("*/SKILL.md")) + list((ROOT / "packs").glob("*/skills/*/SKILL.md"))
        for skill in skills:
            for ups, target in link.findall(skill.read_text(encoding="utf-8")):
                with self.subTest(skill=skill.parent.name, target=target):
                    self.assertEqual(ups, "../")
                    self.assertRegex(target, r"^[a-z0-9-]+/(README|SKILL)\.md$")

    def test_evidence_updater_finds_every_skill_readme(self):
        sys.path.insert(0, str(ROOT / "evals"))
        import update_evidence
        found = update_evidence.readmes()
        skills = [p.parent for p in (ROOT / "skills").glob("*/SKILL.md")] + [p.parent for p in (ROOT / "packs").glob("*/skills/*/SKILL.md")]
        for skill in skills:
            self.assertEqual(found.get(skill.name), skill / "README.md", skill.name)

    def test_core_plugin_lists_every_agent_but_not_the_readme(self):
        manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        expected = [f"./agents/{a.name}" for a in sorted((ROOT / "agents").glob("*.md")) if a.name != "README.md"]
        self.assertEqual(manifest["agents"], expected)

    def test_role_agents_have_frontmatter(self):
        for agent in sorted((ROOT / "agents").glob("*.md")):
            if agent.name == "README.md":
                continue
            with self.subTest(agent=agent.name):
                front = agent.read_text(encoding="utf-8").split("---", 2)[1]
                self.assertEqual(re.search(r"^name: (.+)$", front, re.M).group(1).strip(), agent.stem)
                self.assertRegex(front, r"(?m)^description: .+")

    def test_relative_links_resolve(self):
        for path in (p for p in RELEASE if p.suffix == ".md"):
            for target in re.findall(r"\]\(([^)#\s]+)", path.read_text(encoding="utf-8")):
                if re.match(r"[a-z]+:", target):
                    continue
                with self.subTest(file=str(path.relative_to(ROOT)), link=target):
                    self.assertTrue((path.parent / target).exists())

    def test_no_restricted_names_or_local_details_in_release_files(self):
        local = re.compile(r"[A-Za-z]:[\/]+Users|liam@|@shotclubhouse\.com|codex://", re.I)
        for path in RELEASE:
            text = path.read_text(encoding="utf-8")
            if path.name in {"CODE_OF_CONDUCT.md", "SECURITY.md", "PROVENANCE.md"}:
                # Liam approved this exact public reporting address on 6 November 2026.
                text = text.replace("liam@shotclubhouse.com", "")
            with self.subTest(file=str(path.relative_to(ROOT))):
                self.assertIsNone(local.search(text))
                hits = {p for p in phrases(text) if hashlib.sha256(p.encode()).hexdigest() in BANNED}
                self.assertEqual(hits, set())

    def test_no_em_dashes_in_prose(self):
        for path in (p for p in RELEASE if p.suffix == ".md"):
            with self.subTest(file=str(path.relative_to(ROOT))):
                self.assertNotIn("—", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
