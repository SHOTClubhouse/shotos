import io
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
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
