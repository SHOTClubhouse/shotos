"""Resources that travel with a skill in an install or upload ZIP."""

from pathlib import Path


def example_files(skill: Path):
    """Yield each fictional example with its installed name."""
    examples = skill.parent.parent / "examples" / skill.name
    for kind in ("input", "output"):
        path = examples / f"{kind}.md"
        if path.is_file():
            yield path, f"example-{kind}.md"
