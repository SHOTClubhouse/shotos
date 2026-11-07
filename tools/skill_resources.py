"""Resources that travel with a skill in an install or upload ZIP."""

import re
from pathlib import Path
from urllib.parse import quote

PUBLIC_REPO = "https://github.com/SHOTClubhouse/shotos"
PARENT_LINK = re.compile(r"(?<=\]\()((?:\.\./)+[^\s)#]+)(#[^\s)]*)?")


def example_files(skill: Path):
    """Yield fictional examples and their supporting resources with installed names."""
    examples = skill.parent.parent / "examples" / skill.name
    for kind in ("input", "output"):
        path = examples / f"{kind}.md"
        if path.is_file():
            yield path, f"example-{kind}.md"

    pack = skill.parent.parent
    if skill.name == "success-handoff" and pack.name == "customer-success":
        proposal = pack.parent / "win-the-work" / "skills" / "contextual-proposal"
        for name in ("worked-deal.md", "organisation-templates.md", "template.md"):
            yield proposal / name, f"proposal/{name}"


def portable_readme(skill: Path, repo: Path, *, source_ref: str = "main") -> str:
    """Keep bundled resources local and link other resources to their public source."""
    resources = {path.resolve(): name for path, name in example_files(skill)}
    return portable_markdown(skill / "README.md", repo, resources, source_ref=source_ref)


def portable_markdown(source: Path, repo: Path, bundled_links: dict, *, source_ref: str = "main") -> str:
    """Rewrite parent links for Markdown moved out of its repository folder."""
    def destination(match):
        path = (source.parent / match[1]).resolve()
        fragment = match[2] or ""
        if path in bundled_links:
            return bundled_links[path] + fragment
        kind = "tree" if path.is_dir() else "blob"
        return f"{PUBLIC_REPO}/{kind}/{source_ref}/{quote(path.relative_to(repo).as_posix())}{fragment}"

    return PARENT_LINK.sub(destination, source.read_text(encoding="utf-8"))
