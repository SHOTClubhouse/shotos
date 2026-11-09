import io
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from skill_resources import PUBLIC_REPO
from verify_release import verify_archive


class VerifyReleaseTests(unittest.TestCase):
    def test_matching_download_is_insufficient_if_the_skill_differs_from_source(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "sample" / "SKILL.md"
            skill.parent.mkdir()
            skill.write_bytes(b"current fictional skill")
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, "w") as archive:
                archive.writestr("sample/SKILL.md", b"earlier fictional skill")
            with self.assertRaisesRegex(ValueError, "do not match the release source"):
                verify_archive("sample.zip", buffer.getvalue(), skill)

    def check_links(self, readme):
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "sample" / "SKILL.md"
            skill.parent.mkdir()
            skill.write_bytes(b"fictional skill")
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, "w") as archive:
                archive.writestr("sample/SKILL.md", b"fictional skill")
                archive.writestr("sample/template.md", b"template")
                archive.writestr("sample/README.md", readme)
            verify_archive("sample.zip", buffer.getvalue(), skill, "a" * 40, Path(directory))

    def test_bundled_links_pass_the_release_link_check(self):
        self.check_links(b"See [the template](template.md).")

    def test_a_link_missing_from_the_zip_fails_the_readback(self):
        with self.assertRaisesRegex(ValueError, "file missing from the ZIP"):
            self.check_links(b"See [the guide](guide.md).")

    def test_a_link_to_another_source_ref_fails_the_readback(self):
        link = f"{PUBLIC_REPO}/blob/main/README.md".encode()
        with self.assertRaisesRegex(ValueError, "instead of"):
            self.check_links(b"See [the readme](" + link + b").")
