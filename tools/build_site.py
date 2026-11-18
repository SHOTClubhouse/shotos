#!/usr/bin/env python3
"""Build the SHOTos website into .work/site so you can look at it and check it.

Examples:
  python tools/build_site.py                build the site and check it
  python tools/build_site.py --serve        build it, then serve it at http://localhost:8765
  python tools/build_site.py --out DIR      build into another folder

The site has a landing page, the role guides in docs/guides rendered to HTML
and the fictional Northbank club site as a worked example. Only built files are
written, so a host serves the site and nothing else from the repository. Every
link between pages is relative, so the same files work at a domain root or
under a sub-path such as /shotos/.

Each build fails if a link inside the site points nowhere, if a guide is not
listed below, or if a built file contains a term from the private denylist
named by SHOTOS_DENYLIST. Without the denylist the build still writes the files
for previewing but exits 2, because it cannot be checked for publishing.
release.json in the output names the commit and a hash of every file, so a
published copy can be compared with its source.

This script publishes nothing. Standard library only.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import html
import http.server
import json
import posixpath
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import leak_scan  # noqa: E402
from launch import launchable  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / ".work" / "site"
GITHUB = "https://github.com/SHOTClubhouse/shotos"
NORTHBANK = "examples/northbank-club"
GUIDES_DIR = "docs/guides"
START_HERE = "docs/start-here.md"  # the one-page front door, rendered as start-here.html when it exists
# Every guide in docs/guides, in the order the site lists them, with its card text.
GUIDES = [
    ("Start by role", [
        ("start-by-role", "Pick the job in front of you and the first skill to try."),
        ("small-business", "Take some admin off a small team without anything going to a customer unchecked."),
        ("startup-founder", "Turn one open question into a problem brief and a small test."),
        ("enterprise-operations", "Review one decision or recurring task with its owner, using fictional records first."),
        ("enterprise-risk-review", "Show a risk owner what a workflow can do, what may go wrong and who can stop it."),
    ]),
    ("Set up", [
        ("chat-assistants", "Use the skills in ChatGPT or Claude without a terminal."),
        ("codex-claude-code", "Install the skills into a Codex or Claude Code project on Windows or Mac."),
    ]),
    ("Practise", [
        ("invoice-query-exercise", "A 20-minute fictional handoff between an operator, a reviewer and a sponsor."),
        ("partner-pilot", "Run a pilot between two organisations with one record of decisions and owners."),
    ]),
]


class BuildError(Exception):
    pass


# ---------------------------------------------------------------- Markdown

FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})\s*([\w-]*)")
HEADING = re.compile(r"^ {0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
ITEM = re.compile(r"^(\s*)([-*+]|\d{1,9}[.)])\s+(.*)$")
RULE = re.compile(r"^ {0,3}([-*_])(\s*\1){2,}\s*$")
TABLE_SEP = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$")
RAW_HTML = re.compile(r"^\s*</?(details|summary)\b[^>]*>")
CODE_SPAN = re.compile(r"(`+)(.+?)\1")
IMAGE = re.compile(r"!\[([^\]]*)\]\(([^()\s]+)(?:\s+\"([^\"]*)\")?\)")
LINK = re.compile(r"\[([^\[\]]*)\]\(([^()\s]+)\)")
STRONG = re.compile(r"\*\*(?=\S)(.+?)(?<=\S)\*\*")
EMPHASIS = re.compile(r"(?<![\w*])\*(?=\S)([^*]+?)(?<=\S)\*(?![\w*])|(?<![\w_])_(?=\S)([^_]+?)(?<=\S)_(?![\w_])")
TOKEN = "\x00{}\x00"


def slug(text: str) -> str:
    """The anchor GitHub gives a heading, so links written for GitHub keep working."""
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[`*_]", "", text).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


@dataclass
class Page:
    """One Markdown page being rendered: its links are checked once every page exists."""
    source: str  # repository path of the Markdown file
    path: str  # site path of the HTML file
    fix_link: object  # callable(url, source, path) -> href
    ids: set = field(default_factory=set)
    title: str = ""

    def anchor(self, text: str) -> str:
        base = slug(text) or "section"
        name, n = base, 0
        while name in self.ids:
            n += 1
            name = f"{base}-{n}"
        self.ids.add(name)
        return name


def inline(text: str, page: Page) -> str:
    saved = []

    def keep(fragment: str) -> str:
        saved.append(fragment)
        return TOKEN.format(len(saved) - 1)

    text = CODE_SPAN.sub(lambda m: keep(f"<code>{html.escape(m[2].strip(), quote=False)}</code>"), text)
    text = html.escape(text, quote=False)

    def image(m):
        src = page.fix_link(html.unescape(m[2]), page.source, page.path)
        title = f' title="{html.escape(html.unescape(m[3]))}"' if m[3] else ""
        return keep(f'<img src="{html.escape(src)}" alt="{html.escape(html.unescape(m[1]))}"{title} loading="lazy">')

    def link(m):
        href = page.fix_link(html.unescape(m[2]), page.source, page.path)
        external = href.startswith(("http://", "https://"))
        rel = ' rel="noopener"' if external else ""
        return keep(f'<a href="{html.escape(href)}"{rel}>{emphasis(m[1])}</a>')

    text = IMAGE.sub(image, text)
    text = LINK.sub(link, text)
    text = emphasis(text)
    while "\x00" in text:
        text = re.sub("\x00(\\d+)\x00", lambda m: saved[int(m[1])], text)
    return text


def emphasis(text: str) -> str:
    text = STRONG.sub(r"<strong>\1</strong>", text)
    return EMPHASIS.sub(lambda m: f"<em>{m[1] or m[2]}</em>", text)


def indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def starts_block(line: str) -> bool:
    return bool(FENCE.match(line) or HEADING.match(line) or ITEM.match(line) or RAW_HTML.match(line)
                or line.lstrip().startswith(">") or RULE.match(line))


def cells(row: str) -> list:
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|") and not row.endswith("\\|"):
        row = row[:-1]
    return [cell.strip().replace("\\|", "|") for cell in re.split(r"(?<!\\)\|", row)]


def blocks(lines: list, page: Page, tight: bool = False) -> list:
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        fence = FENCE.match(line)
        if fence:
            marker, body, i = fence[1], [], i + 1
            while i < len(lines) and not lines[i].strip().startswith(marker):
                body.append(lines[i])
                i += 1
            i += 1
            lang = f' class="language-{fence[2]}"' if fence[2] and fence[2] != "text" else ""
            out.append(f"<pre><code{lang}>{html.escape(chr(10).join(body), quote=False)}</code></pre>")
            continue
        heading = HEADING.match(line)
        if heading:
            level, text = len(heading[1]), heading[2]
            if level == 1 and not page.title:
                page.title = re.sub(r"<[^>]+>", "", inline(text, page))
            out.append(f'<h{level} id="{page.anchor(text)}">{inline(text, page)}</h{level}>')
            i += 1
            continue
        if RAW_HTML.match(line):
            out.append(line.strip())  # only <details> and <summary>, written in the repository's own guides
            i += 1
            continue
        if RULE.match(line):
            out.append("<hr>")
            i += 1
            continue
        if line.lstrip().startswith(">"):
            quoted = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                quoted.append(re.sub(r"^\s*> ?", "", lines[i]))
                i += 1
            out.append("<blockquote>\n" + "\n".join(blocks(quoted, page)) + "\n</blockquote>")
            continue
        if "|" in line and i + 1 < len(lines) and TABLE_SEP.match(lines[i + 1]):
            head = cells(line)
            aligns = []
            for sep in cells(lines[i + 1]):
                aligns.append("center" if sep.startswith(":") and sep.endswith(":")
                              else "right" if sep.endswith(":") else "")
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip() and "|" in lines[i]:
                rows.append(cells(lines[i]))
                i += 1

            def cell(tag, n, text):
                style = f' style="text-align:{aligns[n]}"' if n < len(aligns) and aligns[n] else ""
                return f"<{tag}{style}>{inline(text, page)}</{tag}>"

            header = "".join(cell("th", n, text) for n, text in enumerate(head))
            body = "\n".join("<tr>" + "".join(cell("td", n, text) for n, text in enumerate(row[:len(head)]))
                             + "</tr>" for row in rows)
            out.append(f'<div class="table"><table>\n<thead><tr>{header}</tr></thead>\n<tbody>\n{body}\n'
                       "</tbody>\n</table></div>")
            continue
        if ITEM.match(line):
            html_list, i = render_list(lines, i, page)
            out.append(html_list)
            continue
        para = [line.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not starts_block(lines[i]):
            para.append(lines[i].strip())
            i += 1
        text = inline(" ".join(para), page)
        out.append(text if tight else f"<p>{text}</p>")
    return out


def render_list(lines: list, i: int, page: Page) -> tuple:
    first = ITEM.match(lines[i])
    base, ordered = len(first[1]), first[2][0].isdigit()
    start = int(first[2][:-1]) if ordered else 1
    items, loose, done = [], False, False
    while i < len(lines) and not done:
        item = ITEM.match(lines[i])
        if not item or len(item[1]) != base or item[2][0].isdigit() != ordered:
            break
        offset = item.start(3)
        body, i = [item[3]], i + 1
        while i < len(lines):
            line = lines[i]
            if not line.strip():
                j = i
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines) and indent(lines[j]) > base:
                    body += [""] * (j - i)
                    i, loose = j, True
                    continue
                sibling = ITEM.match(lines[j]) if j < len(lines) else None
                if sibling and len(sibling[1]) == base and sibling[2][0].isdigit() == ordered:
                    i, loose = j, True
                else:
                    done = True
                break
            nested = ITEM.match(line)
            if nested and len(nested[1]) <= base:
                break
            if indent(line) > base:
                body.append(line[min(indent(line), offset):])
            elif starts_block(line):
                done = True
                break
            else:
                body.append(line.strip())  # a lazy continuation of the item's paragraph
            i += 1
        items.append(body)
    tag = "ol" if ordered else "ul"
    attr = f' start="{start}"' if ordered and start != 1 else ""
    rendered = "\n".join("<li>" + "\n".join(blocks(body, page, tight=not loose)) + "</li>" for body in items)
    return f"<{tag}{attr}>\n{rendered}\n</{tag}>", i


def markdown(text: str, page: Page) -> str:
    return "\n".join(blocks(text.replace("\r\n", "\n").split("\n"), page))


# ---------------------------------------------------------------- the site

@dataclass
class Site:
    repo: Path
    out: Path
    version: str
    commit: str
    clean: bool
    pages: dict = field(default_factory=dict)  # site path -> Page
    links: list = field(default_factory=list)  # (from page, to site path, fragment, as written)
    copies: dict = field(default_factory=dict)  # site path -> repository path
    files: dict = field(default_factory=dict)  # site path -> bytes

    @property
    def blob(self) -> str:
        return f"{GITHUB}/blob/v{self.version}"

    @property
    def release(self) -> str:
        return f"{GITHUB}/releases/tag/v{self.version}"

    def guide_sources(self) -> dict:
        return {f"{GUIDES_DIR}/{name}.md": f"guides/{name}.html" for _, group in GUIDES for name, _ in group}

    def rendered_sources(self) -> dict:
        """Every Markdown file the site renders: the guides, and the Start here page when it exists."""
        sources = self.guide_sources()
        if (self.repo / START_HERE).is_file():
            sources[START_HERE] = "start-here.html"
        return sources

    def fix_link(self, url: str, source: str, path: str) -> str:
        if re.match(r"^[a-z][a-z0-9+.-]*:", url, re.I):
            return url
        if url.startswith("#"):
            self.links.append((path, path, url[1:], url))
            return url
        target, _, fragment = url.partition("#")
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source), target))
        if resolved.startswith("..") or not (self.repo / resolved).exists():
            raise BuildError(f"{source}: the link {url} points to nothing in the repository")
        guides = self.rendered_sources()
        if resolved in guides:
            dest = guides[resolved]
        elif resolved.startswith("docs/images/"):
            dest = "images/" + resolved[len("docs/images/"):]
            self.copies[dest] = resolved
        elif resolved in (NORTHBANK, f"{NORTHBANK}/README.md"):
            dest = "examples/index.html"
        elif resolved.startswith(f"{NORTHBANK}/site/"):
            dest = "examples/northbank/" + resolved[len(f"{NORTHBANK}/site/"):]
        else:
            kind = "tree" if (self.repo / resolved).is_dir() else "blob"
            return f"{GITHUB}/{kind}/v{self.version}/{resolved}" + (f"#{fragment}" if fragment else "")
        if dest.endswith(".html"):
            self.links.append((path, dest, fragment, url))
        return relative(dest, path) + (f"#{fragment}" if fragment else "")

    def page(self, path: str, title: str, body: str, description: str, section: str = "") -> str:
        up = relative("", path)
        nav = [("Guides", "guides/index.html", "guides"), ("Example", "examples/index.html", "examples")]
        if "start-here.html" in self.rendered_sources().values():
            nav.insert(0, ("Start here", "start-here.html", "start"))
        current = ' aria-current="page"'
        links = "".join(f'<a href="{relative(href, path)}"{current if key == section else ""}>{label}</a>'
                        for label, href, key in nav)
        return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="icon" href="{up}images/shotos-mark.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Poppins:wght@600;700&display=swap">
<link rel="stylesheet" href="{up}styles.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="bar"><div class="wrap">
<a class="brand" href="{up or './'}index.html"><img src="{up}images/shotos-mark.svg" alt="" width="32" height="32">SHOTos</a>
<nav aria-label="Site">{links}<a href="{GITHUB}" rel="noopener">GitHub</a></nav>
</div></header>
<main id="main">
{body}
</main>
<footer><div class="wrap">
<p>SHOTos {self.version} · <a href="{self.release}" rel="noopener">Release notes</a> · <a href="{GITHUB}" rel="noopener">Source on GitHub</a> · Built from <a href="{GITHUB}/commit/{self.commit}" rel="noopener"><code>{self.commit[:7]}</code></a></p>
<p>Code is MIT licensed. Documentation, skills, templates and examples are CC BY 4.0. The SHOT name and logo belong to SHOT Clubhouse Limited and are not covered by either licence.</p>
</div></footer>
</body>
</html>
"""

    def add(self, path: str, content: str):
        self.files[path] = content.encode("utf-8")


def relative(dest: str, here: str) -> str:
    """The link from the page at `here` to `dest`, both site paths."""
    depth = here.count("/")
    return "../" * depth + dest


def git(repo: Path, *args) -> str:
    done = subprocess.run(launchable(["git", "-C", str(repo), *args]), capture_output=True, text=True, timeout=60)
    if done.returncode != 0:
        raise BuildError(f"git {args[0]} failed: {done.stderr.strip()}")
    return done.stdout.strip()


SOURCES = ("docs/guides", START_HERE, "docs/images", f"{NORTHBANK}/site", "tools/build_site.py", ".claude-plugin/plugin.json")


def landing(site: Site) -> str:
    groups = []
    for heading, group in GUIDES:
        cards = "".join(f'<li><a href="guides/{name}.html">{html.escape(site.pages[f"guides/{name}.html"].title)}</a>'
                        f"<span>{html.escape(text)}</span></li>" for name, text in group)
        groups.append(f'<div><h3>{heading}</h3><ul class="cards">{cards}</ul></div>')
    clone = f"git clone {GITHUB}.git"
    preview = "python ../shotos/install.py --runtime claude --scope project --dry-run"
    install = "python ../shotos/install.py --runtime claude --scope project"
    start = ('<a class="button ghost" href="start-here.html">Start here</a>'
             if "start-here.html" in site.rendered_sources().values()
             else '<a class="button ghost" href="guides/start-by-role.html">Start with your role</a>')
    return f"""<section class="hero"><div class="wrap">
<p class="eyebrow">Open source · MIT and CC BY 4.0</p>
<h1>Free AI workflows, from the first brief to a result someone can own.</h1>
<p class="lede">SHOTos is a set of skills, templates and rules for the AI assistant you already use. Use it to turn customer notes into a test plan, write a proposal, build a campaign preview or hand work to the next person. Start from your context, agree what good looks like, then check what comes back.</p>
<p class="actions"><a class="button" href="{site.release}" rel="noopener">Download SHOTos {site.version}</a>{start}</p>
</div></section>

<section class="wrap" aria-labelledby="install"><h2 id="install">Install</h2>
<p>The installer needs Python 3.9 or later. Clone SHOTos next to the project where you want to use it, then run the installer from your project folder. Preview first with <code>--dry-run</code>.</p>
<pre><code>{html.escape(clone)}</code></pre>
<pre><code>{html.escape(preview)}
{html.escape(install)}</code></pre>
<p>Use <code>--runtime agents</code> for Codex and other agents, and add <code>--pack &lt;name&gt;</code> for each pack you want. The installer always includes the core skills. No terminal? <a href="guides/chat-assistants.html">Use the skills in ChatGPT or Claude</a> by downloading the ZIPs from the <a href="{GITHUB}/releases/latest" rel="noopener">latest release</a>.</p>
</section>

<section class="wrap" aria-labelledby="rules"><h2 id="rules">The four rules inside every stage</h2>
<ol class="rules">
<li><strong>Stop at the boundaries.</strong> Get authority for actions that send, spend, publish, deploy or affect others.</li>
<li><strong>Agree acceptance first.</strong> Name the owner, expected result and checks.</li>
<li><strong>Read back the real result.</strong> Open the output, run the check or inspect the relevant system.</li>
<li><strong>Claim only what you can show.</strong> Link the evidence and label what still needs verification.</li>
</ol>
<figure><img src="images/six-stages.svg" alt="The six stages: Scope, Hypothesise, Operate, Track, Own, and Sustain and Scale." loading="lazy"></figure>
</section>

<section class="wrap" aria-labelledby="guides"><h2 id="guides">Guides</h2>
<div class="groups">{"".join(groups)}</div>
</section>

<section class="wrap" aria-labelledby="example"><h2 id="example">Worked example</h2>
<p><a href="examples/index.html">Northbank Community Football</a> is a fictional three-page club site and open-day campaign, taken from brief to a checked release with SHOTos. All club details are invented.</p>
</section>

<section class="wrap" aria-labelledby="licence"><h2 id="licence">Licence</h2>
<p>Code, including <code>tools/</code>, <code>hooks/</code> and <code>install.py</code>, is under the <a href="{site.blob}/LICENSE" rel="noopener">MIT licence</a>. Documentation, skills, templates and examples are under <a href="{site.blob}/LICENSE-docs.md" rel="noopener">CC BY 4.0</a>: share and adapt them for any purpose, with the credit set out in that file. The SHOT name and logo are not covered by either licence.</p>
</section>
"""


def example_page(site: Site) -> str:
    return f"""<div class="wrap prose">
<p class="eyebrow">Worked example · fictional</p>
<h1>Northbank Community Football</h1>
<p>A fictional three-page club website and open-day campaign, showing how SHOTos goes from a brief to a checked public release. All club details are invented. The pitch illustration is original SVG and the pages use local assets.</p>
<p class="actions"><a class="button" href="northbank/index.html">Open the example site</a><a class="button ghost" href="northbank/open-day.html">Open the campaign page</a></p>
<h2>Follow it through</h2>
<ol>
<li>Read the <a href="{site.blob}/packs/content/examples/build-small-website/input.md" rel="noopener">site brief</a>.</li>
<li>Open <a href="northbank/index.html">Home</a>, <a href="northbank/sessions.html">Sessions</a> and <a href="northbank/open-day.html">Open day</a>. The main campaign action opens an on-page itinerary.</li>
<li>Compare them with the <a href="{site.blob}/packs/content/examples/build-small-website/output.md" rel="noopener">site output example</a>.</li>
<li>Try the <a href="{site.blob}/{NORTHBANK}/campaign-review.md" rel="noopener">two-round campaign review</a> with its fictional records.</li>
</ol>
<p>The <a href="{site.blob}/packs/content/skills/build-small-website/README.md" rel="noopener">Build a Small Website</a> skill covers the site. <a href="{site.blob}/packs/content/skills/campaign-website/README.md" rel="noopener">Campaign Website</a> covers the event page.</p>
</div>
"""


def build(repo: Path = REPO, out: Path = OUT) -> Site:
    version = json.loads((repo / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))["version"]
    commit = git(repo, "rev-parse", "HEAD")
    clean = not git(repo, "status", "--porcelain", "--", *SOURCES)
    site = Site(repo, out, version, commit, clean)

    listed = set(site.guide_sources())
    present = {f"{GUIDES_DIR}/{p.name}" for p in (repo / GUIDES_DIR).glob("*.md")}
    if present != listed:
        missing, extra = sorted(present - listed), sorted(listed - present)
        raise BuildError(f"GUIDES in tools/build_site.py does not match docs/guides "
                         f"(unlisted: {', '.join(missing) or 'none'}; not found: {', '.join(extra) or 'none'})")

    for source, path in site.rendered_sources().items():
        page = Page(source, path, site.fix_link)
        body = markdown((repo / source).read_text(encoding="utf-8"), page)
        site.pages[path] = page
        section = "start" if source == START_HERE else "guides"
        edit = f'<p class="source"><a href="{site.blob}/{source}" rel="noopener">View this page on GitHub</a></p>'
        site.add(path, site.page(path, f"{page.title} · SHOTos", f'<article class="wrap prose">\n{body}\n{edit}\n'
                                 "</article>", f"SHOTos: {page.title}", section))

    index = Page("", "guides/index.html", site.fix_link)
    groups = "".join(f"<h2>{heading}</h2><ul class=\"cards\">" + "".join(
        f'<li><a href="{name}.html">{html.escape(site.pages[f"guides/{name}.html"].title)}</a>'
        f"<span>{html.escape(text)}</span></li>" for name, text in group) + "</ul>" for heading, group in GUIDES)
    site.pages[index.path] = index
    site.add(index.path, site.page(index.path, "Guides · SHOTos", f'<div class="wrap prose"><h1>Guides</h1>\n'
                                   f"<p>Choose the guide that fits the work in front of you.</p>{groups}</div>",
                                   "SHOTos guides by role, set-up and practice exercise.", "guides"))

    for path, body, title, description, section in (
            ("index.html", landing(site), "SHOTos · free AI workflows you can check",
             "Free, open-source AI workflows, from the first brief to a result someone can own.", ""),
            ("examples/index.html", example_page(site), "Northbank example · SHOTos",
             "A fictional club website and open-day campaign built with SHOTos.", "examples")):
        site.pages[path] = Page("", path, site.fix_link)
        site.add(path, site.page(path, title, body, description, section))
        for href in re.findall(r'href="([^"#:]+\.html)(?:#([^"]*))?"', body):
            site.links.append((path, posixpath.normpath(posixpath.join(posixpath.dirname(path), href[0])),
                               href[1], href[0]))
    site.add("404.html", not_found())

    for name in ("shotos-mark.svg", "six-stages.svg"):
        site.copies[f"images/{name}"] = f"docs/images/{name}"
    for file in sorted((repo / NORTHBANK / "site").rglob("*")):
        if file.is_file():
            site.copies["examples/northbank/" + file.relative_to(repo / NORTHBANK / "site").as_posix()] = \
                file.relative_to(repo).as_posix()
    for dest, source in site.copies.items():
        site.files[dest] = (repo / source).read_bytes()
    site.files["styles.css"] = STYLES.encode("utf-8")
    check_links(site)

    site.files["release.json"] = (json.dumps({
        "site": "SHOTos", "version": version, "commit": commit, "clean": clean,
        "files": {path: hashlib.sha256(data).hexdigest() for path, data in sorted(site.files.items())},
    }, indent=2) + "\n").encode("utf-8")
    write(site)
    return site


def check_links(site: Site):
    broken = []
    for here, dest, fragment, written in site.links:
        page = site.pages.get(dest)
        if dest not in site.files and dest not in site.copies:
            broken.append(f"{here}: {written} leads to {dest}, which is not in the site")
        elif fragment and page is not None and page.source and fragment not in page.ids:
            broken.append(f"{here}: {written} names #{fragment}, which {dest} does not have")
    if broken:
        raise BuildError("broken links:\n  " + "\n  ".join(broken))


def write(site: Site):
    out, repo = site.out.resolve(), site.repo.resolve()
    if out == repo or out in repo.parents:
        raise BuildError(f"{out} holds the repository, so it cannot be the output folder")
    if out.exists() and any(out.iterdir()) and not (out / "release.json").is_file():
        raise BuildError(f"{out} is not an earlier site build, so it will not be replaced")
    if out.exists():
        shutil.rmtree(out)
    for path, data in site.files.items():
        target = out / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)


def scan(site: Site, denylist: Path) -> list:
    """Each built file and file name checked against the denylist, reported without the term."""
    entries = leak_scan.load_denylist(denylist)
    hits = []
    for path, data in sorted(site.files.items()):
        shown = leak_scan.redact_path(path, entries)
        hits += [f"{shown} (file name): denylist line {entry.line}" for entry in entries if entry.found(path)]
        text = leak_scan.decode(data)
        if text is not None:
            hits += [f"{shown}:{line}: denylist line {entry}" for line, entry in leak_scan.text_hits(text, entries)]
    return hits


def not_found() -> str:
    return f"""<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found · SHOTos</title>
<style>body{{font:16px/1.6 Montserrat,Arial,sans-serif;color:#131023;max-width:36rem;margin:4rem auto;padding:0 1rem}}a{{color:#6B00DB}}</style>
</head><body><h1>Page not found</h1>
<p>This page is not part of the SHOTos site. Try the <a href="{GITHUB}" rel="noopener">SHOTos repository on GitHub</a>.</p>
</body></html>
"""


STYLES = """:root {
  --ink: #131023; --muted: #494456; --line: #d8d1e4; --tint: #f6f2fc;
  --purple: #6B00DB; --gold: #F7B613; --teal: #1ABC9C; --paper: #ffffff;
  --head: Poppins, Arial, sans-serif; --body: Montserrat, Arial, sans-serif;
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; background: var(--paper); color: var(--ink); font: 16px/1.65 var(--body); overflow-wrap: break-word; }
h1, h2, h3, h4 { font-family: var(--head); font-weight: 700; line-height: 1.25; margin: 1.6em 0 .5em; }
h1 { font-size: clamp(1.9rem, 5vw, 2.8rem); margin-top: .4em; }
h2 { font-size: 1.5rem; } h3 { font-size: 1.15rem; font-weight: 600; }
a { color: var(--purple); text-underline-offset: 2px; }
a:focus-visible, .button:focus-visible { outline: 3px solid var(--gold); outline-offset: 2px; }
img { max-width: 100%; height: auto; }
code { font: .9em/1.4 ui-monospace, Consolas, monospace; background: var(--tint); padding: .1em .3em; border-radius: 4px; }
pre { background: var(--ink); color: #fff; padding: 1rem; border-radius: 10px; overflow-x: auto; }
pre code { background: none; padding: 0; color: inherit; white-space: pre; }
blockquote { margin: 1rem 0; padding: .5rem 1rem; border-left: 4px solid var(--purple); background: var(--tint); }
blockquote p { margin: .4rem 0; }
.wrap { max-width: 68rem; margin: 0 auto; padding: 0 16px; }
.prose { max-width: 48rem; padding-bottom: 2rem; }
.skip { position: absolute; left: -999px; top: 0; }
.skip:focus { left: 8px; top: 8px; background: #fff; padding: .5rem 1rem; z-index: 2; }
.bar { border-bottom: 1px solid var(--line); }
.bar .wrap { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: .5rem 1rem; padding-top: .7rem; padding-bottom: .7rem; }
.brand { display: flex; align-items: center; gap: .5rem; font: 700 1.2rem var(--head); color: var(--ink); text-decoration: none; }
nav { display: flex; gap: 1rem; flex-wrap: wrap; }
nav a { color: var(--ink); text-decoration: none; font-weight: 700; padding: .25rem 0; }
nav a[aria-current] { color: var(--purple); box-shadow: inset 0 -3px 0 var(--purple); }
.hero { background: var(--tint); border-bottom: 1px solid var(--line); padding: 2.5rem 0 2.5rem; }
.hero h1 { max-width: 20ch; }
.eyebrow { font: 600 .8rem var(--head); letter-spacing: .08em; text-transform: uppercase; color: var(--muted); margin: 1.5rem 0 0; }
.lede { font-size: 1.1rem; max-width: 46rem; color: var(--muted); }
.actions { display: flex; flex-wrap: wrap; gap: .75rem; margin: 1.5rem 0 .5rem; }
.button { display: inline-block; background: var(--purple); color: #fff; font: 700 1rem var(--head); padding: .7rem 1.2rem; border-radius: 999px; text-decoration: none; border: 2px solid var(--purple); }
.button.ghost { background: #fff; color: var(--purple); }
section.wrap { padding-top: .5rem; }
.rules li { margin: .4rem 0; }
figure { margin: 1.5rem 0; } figure img { border-radius: 12px; }
.groups { display: grid; gap: 0 2rem; grid-template-columns: repeat(auto-fit, minmax(17rem, 1fr)); }
.cards { list-style: none; padding: 0; margin: 0 0 1rem; display: grid; gap: .75rem; }
.cards li { border: 1px solid var(--line); border-radius: 12px; padding: .8rem 1rem; }
.cards a { display: block; font: 600 1.02rem/1.35 var(--head); text-decoration: none; }
.cards span { display: block; color: var(--muted); font-size: .95rem; margin-top: .25rem; }
.table { overflow-x: auto; margin: 1rem 0; border: 1px solid var(--line); border-radius: 10px; }
table { border-collapse: collapse; width: 100%; min-width: 32rem; font-size: .95rem; }
th, td { text-align: left; vertical-align: top; padding: .55rem .75rem; border-bottom: 1px solid var(--line); }
th { background: var(--tint); font-family: var(--head); font-weight: 600; }
tr:last-child td { border-bottom: 0; }
details { border: 1px solid var(--line); border-radius: 10px; padding: .5rem 1rem; margin: 1rem 0; }
summary { cursor: pointer; font-weight: 700; }
.source { margin-top: 2.5rem; font-size: .95rem; }
footer { border-top: 1px solid var(--line); margin-top: 3rem; padding: 1.5rem 0 2rem; color: var(--muted); font-size: .9rem; }
footer p { margin: .4rem 0; }
"""


def serve(out: Path, port: int):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(out))
    with http.server.ThreadingHTTPServer(("127.0.0.1", port), handler) as server:
        print(f"Serving {out} at http://localhost:{port}/ (Ctrl+C to stop)")
        server.serve_forever()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=OUT, help=f"output folder (default: {OUT.relative_to(REPO)})")
    parser.add_argument("--denylist", help="denylist file (default: the SHOTOS_DENYLIST environment variable)")
    parser.add_argument("--serve", action="store_true", help="serve the built site on localhost after building")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args(argv)
    try:
        site = build(REPO, args.out)
    except BuildError as error:
        print(f"Site not built: {error}", file=sys.stderr)
        return 1
    print(f"Built {len(site.files)} files into {site.out} from {site.commit[:12]} (SHOTos {site.version}).")
    status = 0
    tagged = subprocess.run(launchable(["git", "-C", str(REPO), "rev-parse", "-q", "--verify",
                                        f"refs/tags/v{site.version}^{{commit}}"]),
                            capture_output=True, text=True).stdout.strip()
    if tagged != site.commit:
        print(f"HEAD is not the v{site.version} release commit. Links into the repository point at the "
              f"v{site.version} tag, so files added since then will not open until the next release.")
    if not site.clean:
        print("The site sources have uncommitted changes: preview only, not fit to publish.")
        status = 2
    denylist = leak_scan.denylist_path(args.denylist)
    if denylist is None:
        print("No denylist, so the output was not scanned: preview only, not fit to publish. "
              "Set SHOTOS_DENYLIST to the private denylist file.")
        status = 2
    else:
        try:
            hits = scan(site, denylist)
        except (OSError, ValueError) as error:
            print(f"Denylist scan could not run: {type(error).__name__}", file=sys.stderr)
            return 2
        if hits:
            print("Private terms found in the output:\n  " + "\n  ".join(hits), file=sys.stderr)
            return 1
        print(f"Denylist scan: no private terms in {len(site.files)} built files.")
    if args.serve:
        serve(site.out, args.port)
    return status


if __name__ == "__main__":
    sys.exit(main())
