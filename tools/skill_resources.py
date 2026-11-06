"""Resources that travel with a skill in an install or upload ZIP."""

import re
from pathlib import Path
from urllib.parse import quote

PUBLIC_REPO = "https://github.com/SHOTClubhouse/shotos"
PARENT_LINK = re.compile(r"(?<=\]\()((?:\.\./)+[^\s)#]+)(#[^\s)]*)?")


def example_files(skill: Path):
    """Yield each fictional example with its installed name."""
    examples = skill.parent.parent / "examples" / skill.name
    for kind in ("input", "output"):
        path = examples / f"{kind}.md"
        if path.is_file():
            yield path, f"example-{kind}.md"


def portable_readme(skill: Path, repo: Path) -> str:
    """Keep bundled resources local and link other resources to their public source."""
    examples = {path.resolve(): name for path, name in example_files(skill)}

    def destination(match):
        path = (skill / match[1]).resolve()
        fragment = match[2] or ""
        if path in examples:
            return examples[path] + fragment
        kind = "tree" if path.is_dir() else "blob"
        return f"{PUBLIC_REPO}/{kind}/main/{quote(path.relative_to(repo).as_posix())}{fragment}"

    return PARENT_LINK.sub(destination, (skill / "README.md").read_text(encoding="utf-8"))
