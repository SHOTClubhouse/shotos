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
import subprocess
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
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
# The only raw HTML passed through: bare <details> and </details> lines, and a one-line <summary>
# whose text is rendered like any other text. Anything else, attributes included, is escaped.
RAW_HTML = re.compile(r"^\s*(<details>|<details open>|</details>|<summary>(?P<summary>[^<>]*)</summary>)\s*$")
SAFE_SCHEMES = {"http", "https", "mailto"}
SCHEME = re.compile(r"^([a-z][a-z0-9+.-]*):", re.I)
BUILD_MARKER = ".shotos-site-build"
# The only kinds of file the site copies from the repository, and the ones always scanned as text.
COPY_TYPES = {".html", ".css", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif"}
TEXT_TYPES = {".html", ".css", ".svg", ".json", ".txt", ".xml"}
MARKER_TEXT = "Built by tools/build_site.py. This folder is replaced on every build.\n"
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
        raw = RAW_HTML.match(line)
        if raw:
            summary = raw["summary"]
            out.append(raw[1] if summary is None else f"<summary>{inline(summary, page)}</summary>")
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
    tracked: dict = field(default_factory=dict)  # repository path -> Git file mode, from git ls-files
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
        if START_HERE in self.tracked:
            sources[START_HERE] = "start-here.html"
        return sources

    def is_tracked(self, path: str) -> bool:
        return path in self.tracked

    def is_tracked_dir(self, path: str) -> bool:
        return any(name.startswith(path.rstrip("/") + "/") for name in self.tracked)

    def fix_link(self, url: str, source: str, path: str) -> str:
        scheme = SCHEME.match(url)
        if scheme:
            if scheme[1].lower() not in SAFE_SCHEMES:
                raise BuildError(f"{source}: the link {url} uses {scheme[1]}:, which the site does not allow")
            return url
        if url.startswith(("/", "\\")):
            raise BuildError(f"{source}: the link {url} starts with a slash, which breaks under a sub-path")
        if url.startswith("#"):
            return url
        target, _, fragment = url.partition("#")
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source), target))
        if resolved.startswith("..") or not (self.is_tracked(resolved) or self.is_tracked_dir(resolved)):
            raise BuildError(f"{source}: the link {url} points to nothing tracked in the repository")
        guides = self.rendered_sources()
        if resolved in guides:
            dest = guides[resolved]
        elif resolved.startswith("docs/images/") and self.is_tracked(resolved):
            dest = "images/" + resolved[len("docs/images/"):]
            self.copies[dest] = resolved
        elif resolved in (NORTHBANK, f"{NORTHBANK}/README.md"):
            dest = "examples/index.html"
        elif resolved.startswith(f"{NORTHBANK}/site/") and self.is_tracked(resolved):
            dest = "examples/northbank/" + resolved[len(f"{NORTHBANK}/site/"):]
        else:
            kind = "blob" if self.is_tracked(resolved) else "tree"
            return f"{GITHUB}/{kind}/v{self.version}/{resolved}" + (f"#{fragment}" if fragment else "")
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


# The six stages, in the words of docs/framework.md and the README stage table.
STAGES = [
    ("Scope", "stage-01-scope.png", "A product owner spreads support notes across a desk to write a problem brief.",
     "Understand the situation before changing it. Most wasted effort starts with a solution chosen before anyone "
     "wrote down the problem.", "A problem brief and baseline"),
    ("Hypothesise", "stage-02-hypothesise.png", "A founder turns repeat calls into a one-week test.",
     "Turn the problem into bets you can test, and agree how you will know before you build anything.",
     "A hypothesis, experiment plan and acceptance checks"),
    ("Operate", "stage-03-operate.png", "A marketer turns approved copy and assets into a page preview.",
     "Deliver the smallest real piece into real use, working alongside the people who will own it.",
     "The actual result, checks and exceptions"),
    ("Track", "stage-04-track.png", "A student compares venue quotes and capacity to make a recommendation.",
     "Measure what changed against the baseline, then decide.",
     "Evidence and a decision: proceed to Own, pivot, stop or hold"),
    ("Own", "stage-05-own.png", "A commercial lead hands an accepted proposal to the delivery team.",
     "Make the team that will run the result self-sufficient before anyone copies it elsewhere.",
     "Evidence the team ran it independently and a named lead accepted it"),
    ("Sustain and Scale", "stage-06-sustain-scale.png",
     "A social creator turns an approved content week into a calendar to reuse.",
     "Take what worked to the next team, and keep improving.",
     "A supported rollout, local baselines and a review cadence"),
]
# The role cards, in the words of docs/guides/start-by-role.md, each linking to its section there.
ROLES = [
    ("Founder", "role-founder.png", "founder", "Turn customer notes into a clear problem and one small test."),
    ("Commercial lead", "role-commercial.png", "commercial-lead",
     "Qualify an opportunity, draft the offer and carry the accepted deal into delivery."),
    ("Product manager", "role-product.png", "product-manager",
     "Turn a feature request into examples the team can build and check."),
    ("Marketing manager", "role-marketing.png", "marketing-manager",
     "Give a B2B or direct-to-consumer campaign one action people can try."),
    ("Graduate", "role-graduate.png", "graduate",
     "Turn an assignment into a clear brief and a result your lead can review."),
    ("Social content creator", "role-creator.png", "social-content-creator",
     "Build a week of posts around real events, assets and audience needs."),
    ("The method", "role-method.png", "what-shotos-stands-for",
     "Scope, Hypothesise, Operate, Track, Own, and Sustain and Scale on one page."),
]
LANDING_IMAGES = ["shotos-mark.svg", "six-stages.svg", "stage-07-worked-outputs.png",
                  *(image for _, image, *_ in STAGES), *(image for _, image, *_ in ROLES)]


def picture(src: str, alt: str, lazy: bool = True) -> str:
    size = ' width="1270" height="760"' if src.endswith(".png") else ""
    load = ' loading="lazy"' if lazy else ""
    return f'<img src="{src}" alt="{html.escape(alt)}"{size}{load}>'


def landing(site: Site) -> str:
    groups = []
    for heading, group in GUIDES:
        cards = "".join(f'<li><a href="guides/{name}.html">{html.escape(site.pages[f"guides/{name}.html"].title)}</a>'
                        f"<span>{html.escape(text)}</span></li>" for name, text in group)
        groups.append(f'<div><h3>{heading}</h3><ul class="cards">{cards}</ul></div>')
    stages = "".join(
        f'<li class="stage"><figure>{picture(f"images/{image}", f"{name}: {alt}")}</figure>'
        f'<h3><span class="step">{n:02d}</span> {name}</h3><p>{html.escape(line)}</p>'
        f'<p class="hands"><strong>You hand forward:</strong> {html.escape(hands)}</p></li>'
        for n, (name, image, alt, line, hands) in enumerate(STAGES, 1))
    roles = "".join(
        f'<li class="role"><a href="guides/start-by-role.html#{anchor}">'
        f'{picture(f"images/{image}", f"{name} route. {text}")}'
        f'<span class="role-name">{name}</span><span class="role-text">{html.escape(text)}</span></a></li>'
        for name, image, anchor, text in ROLES)
    agreement = f"{site.blob}/templates/AGENTS.md"
    first_zip = f"{GITHUB}/releases/latest/download/capture-the-problem.zip"
    terminal = "\n".join([
        "# In the folder that holds your project, not inside it:",
        f"git clone {GITHUB}.git",
        "cd my-project",
        "python ../shotos/install.py --runtime claude --scope project --dry-run",
        "python ../shotos/install.py --runtime claude --scope project",
    ])
    start = ('<a class="button ghost" href="start-here.html">Start here</a>'
             if "start-here.html" in site.rendered_sources().values()
             else '<a class="button ghost" href="#roles">Start with your role</a>')
    return f"""<section class="hero"><div class="wrap split">
<div>
<p class="eyebrow">Free and open source · MIT and CC BY 4.0</p>
<h1>Free AI workflows, from the first brief to a result someone can own.</h1>
<p class="lede">SHOTos turns the AI assistant you already use into a small, careful team. It starts from your context, agrees what done looks like before it starts, checks the real result where it lives and tells you plainly what it could not check.</p>
<p class="actions"><a class="button" href="#set-up">Set up in five minutes</a>{start}</p>
<p class="small">Latest release: <a href="{site.release}" rel="noopener">SHOTos {site.version}</a> · <a href="{GITHUB}" rel="noopener">Source on GitHub</a></p>
</div>
<figure class="hero-art">{picture("images/stage-07-worked-outputs.png", "Two worked outputs made with SHOTos: a fictional campaign page, and the North Quay proposal with its delivery handoff record.", lazy=False)}</figure>
</div></section>

<section class="wrap" aria-labelledby="why"><h2 id="why">Why it exists</h2>
<p class="intro">Most AI help fails in the same few ways. None of them is fixed by a cleverer prompt. They are fixed by a process: say who the work is for and what would show it worked, test the idea small, check the real result and hand it to someone who can own it. Good teams already work this way. SHOTos writes that process down so an agent can follow it and a person can check it did.</p>
<div class="pairs">
<div class="pair"><p class="problem">the assistant guesses at facts it was never given.</p><p class="answer">it starts from your context: the task, its sources and the person who will review it.</p></div>
<div class="pair"><p class="problem">it does the task it imagined, not the one you meant.</p><p class="answer">it agrees what done looks like, including one check that should fail, before any work starts.</p></div>
<div class="pair"><p class="problem">it says "done" from memory of what it intended.</p><p class="answer">it reads back the real result where it lives: the file, the page or the record.</p></div>
<div class="pair"><p class="problem">it writes an invented number as confidently as a real one.</p><p class="answer">it claims only what it can show and marks everything else as not checked.</p></div>
</div>
</section>

<section class="wrap" aria-labelledby="how"><h2 id="how">How it works</h2>
<p class="intro">Two things hold SHOTos together: four rules inside every task, and six stages for work that matters. A small job uses one stage and one skill. A change that someone will rely on moves through all six, and each stage ends with a decision a person makes.</p>
<h3 id="rules">The four rules inside every task</h3>
<ol class="rules">
<li><strong>Stop at the boundaries.</strong> Nothing is sent, spent, published or deleted without your yes.</li>
<li><strong>Agree acceptance first.</strong> Name the owner, the expected result and the checks.</li>
<li><strong>Read back the real result.</strong> Open the output, run the check or look at the system it changed.</li>
<li><strong>Claim only what you can show.</strong> Link the evidence and label what still needs checking.</li>
</ol>
<p>The rules live in one short file, the <a href="{agreement}" rel="noopener">working agreement</a>. A project install loads it in every session. In a chat app, paste it into the project instructions or attach it to the chat.</p>
<figure class="overview">{picture("images/six-stages.svg", "The six stages from Scope to Sustain and Scale. After Track, work proceeds to Own, returns to Hypothesise to try a new idea, waits for facts or stops. Scaling starts the next team at Scope.")}</figure>
</section>

<section class="wrap" aria-labelledby="stages"><h2 id="stages">The six stages, one job at a time</h2>
<p class="intro">Each stage has skills that do its job and a clear thing to hand to the next. Every example below is fictional, so you can try it without real records.</p>
<ol class="stage-grid">{stages}</ol>
<p><a href="{site.blob}/docs/framework.md" rel="noopener">Read the six stages in detail</a> · <a href="examples/index.html">Open the Northbank worked example</a></p>
</section>

<section class="wrap" aria-labelledby="roles"><h2 id="roles">Start with your role</h2>
<p class="intro">Pick the card closest to the work in front of you. Each one opens a short route: the first skill to try, the result to expect and how to check it helped. Leading a team or a business? Start with the <a href="guides/start-by-role.html#business-leader">business leader route</a> or the <a href="guides/small-business.html">small business guide</a>.</p>
<ul class="role-grid">{roles}</ul>
</section>

<section class="wrap" aria-labelledby="set-up"><h2 id="set-up">Set up in five minutes</h2>
<p class="intro">The same skills work in three ways. Pick the one that matches how you work today. Whichever you choose, check the first result before you rely on it.</p>
<div class="routes">
<div class="route"><h3>A. One skill in your chat app</h3><p>Best for trying SHOTos on one real task.</p>
<ol>
<li>Download a skill ZIP from the <a href="{GITHUB}/releases/latest" rel="noopener">latest release</a>. <a href="{first_zip}" rel="noopener">Capture the Problem</a> is a good first one.</li>
<li>Upload it as a skill without unzipping it. In Claude, open <strong>Customize → Skills</strong>. In ChatGPT, use <strong>Skills → Create → Upload from your computer</strong> where your workspace allows it.</li>
<li>A single skill ZIP does not carry the <a href="{agreement}" rel="noopener">working agreement</a>. Attach it to a fresh chat, ask the assistant to read it first, then ask for the skill by name.</li>
</ol>
<p><a href="guides/chat-assistants.html">Step-by-step guide</a></p></div>
<div class="route"><h3>B. A chat project</h3><p>Best for a team that works in Claude or ChatGPT every day.</p>
<ol>
<li>Create a project and paste the <a href="{agreement}" rel="noopener">working agreement</a> into its instructions.</li>
<li>Add the skill files you use most to the project's files.</li>
<li>Ask for a skill by name in any chat inside the project.</li>
</ol>
<p><a href="guides/chat-assistants.html#chatgpt-projects-or-a-claude-chat-using-files">Step-by-step guide</a></p></div>
<div class="route wide"><h3>C. A terminal</h3><p>Best if you already use Claude Code, Codex or another coding agent. The installer needs Python 3.9 or later. Open a terminal in the folder that holds your project, clone SHOTos beside it, move into your project and run the installer. Replace <code>my-project</code> with your project's folder name, and preview first with <code>--dry-run</code>.</p>
<pre><code>{html.escape(terminal)}</code></pre>
<p>Use <code>--runtime agents</code> for Codex and other agents, and add <code>--pack &lt;name&gt;</code> for each pack you want. The installer always includes the core skills and the working agreement. Then open a fresh session in the project and ask for a skill by name. <a href="guides/codex-claude-code.html">Step-by-step guide</a></p></div>
</div>
</section>

<section class="wrap" aria-labelledby="guides"><h2 id="guides">All guides</h2>
<div class="groups">{"".join(groups)}</div>
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
    if not isinstance(version, str) or not re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", version):
        raise BuildError(f"plugin.json has {version!r}, which is not a release version such as 1.17.0")
    commit = git(repo, "rev-parse", "HEAD")
    clean = not git(repo, "status", "--porcelain", "--", *SOURCES)
    site = Site(repo, out, version, commit, clean, tracked=tracked_files(repo))

    listed = set(site.guide_sources())
    present = {path for path in site.tracked if posixpath.dirname(path) == GUIDES_DIR and path.endswith(".md")}
    if present != listed:
        missing, extra = sorted(present - listed), sorted(listed - present)
        raise BuildError(f"GUIDES in tools/build_site.py does not match docs/guides "
                         f"(unlisted: {', '.join(missing) or 'none'}; not found: {', '.join(extra) or 'none'})")

    for source, path in site.rendered_sources().items():
        page = Page(source, path, site.fix_link)
        body = markdown(read_tracked(site, source).decode("utf-8"), page)
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
    site.add("404.html", not_found())

    for name in LANDING_IMAGES:
        site.copies[f"images/{name}"] = f"docs/images/{name}"
    prefix = f"{NORTHBANK}/site/"
    for path in sorted(site.tracked):
        if path.startswith(prefix):
            site.copies["examples/northbank/" + path[len(prefix):]] = path
    copy_files(site)
    site.files["styles.css"] = STYLES.encode("utf-8")
    check_links(site)

    site.files["release.json"] = (json.dumps({
        "site": "SHOTos", "version": version, "commit": commit, "clean": clean,
        "files": {path: hashlib.sha256(data).hexdigest() for path, data in sorted(site.files.items())},
    }, indent=2) + "\n").encode("utf-8")
    write(site)
    return site


def read_tracked(site: Site, source: str) -> bytes:
    """A source file's bytes. Only tracked, regular files: never an ignored file, a symlink or a path outside."""
    if site.tracked.get(source) not in ("100644", "100755"):
        raise BuildError(f"{source} is not a tracked regular file, so it cannot be used in the site")
    file = (site.repo / source).resolve()
    if site.repo.resolve() not in file.parents or not file.is_file():
        raise BuildError(f"{source} does not resolve to a file inside the repository")
    return file.read_bytes()


def copy_files(site: Site):
    """Copy each planned file: tracked regular pages, stylesheets and images only."""
    for dest, source in site.copies.items():
        if kind(source) not in COPY_TYPES or kind(dest) not in COPY_TYPES:
            raise BuildError(f"{source} is not a page, stylesheet or image, so it cannot be copied into the site")
        site.files[dest] = read_tracked(site, source)


def tracked_files(repo: Path) -> dict:
    """Repository path -> Git file mode for every tracked file (120000 is a symlink)."""
    tracked = {}
    for row in filter(None, git(repo, "ls-files", "-s", "-z").split("\0")):
        meta, path = row.split("\t", 1)
        tracked[path] = meta.split()[0]
    return tracked


# Tags whose edges separate text on screen, so "a<br>b" and "<p>a</p><p>b</p>" read as two words.
BREAK_TAGS = {"address", "article", "aside", "blockquote", "br", "caption", "dd", "details", "div", "dl", "dt",
              "figcaption", "figure", "footer", "h1", "h2", "h3", "h4", "h5", "h6", "header", "hr", "li", "main",
              "nav", "ol", "p", "pre", "section", "summary", "table", "td", "th", "tr", "ul", "img", "text",
              "tspan", "title", "desc"}
ACTIVE_TAGS = {"script", "iframe", "frame", "frameset", "object", "embed", "applet", "base", "foreignobject"}
URL_ATTRIBUTES = {"href", "src", "action", "formaction", "poster", "data", "cite", "background", "xlink:href"}
CSS_URL = re.compile(r"""url\(\s*['"]?([^'")]+)['"]?\s*\)|@import\s+['"]([^'"]+)['"]""", re.I)


IMAGE_SET = re.compile(r"(?:-webkit-)?image-set\(((?:[^()]|\([^()]*\))*)\)", re.I)


def css_refs(text: str) -> list:
    refs = [m[1] or m[2] for m in CSS_URL.finditer(text)]
    for match in IMAGE_SET.finditer(text):  # image-set("a.png" 1x, "b.png" 2x) takes bare strings too
        refs += re.findall(r"""['"]([^'"]+)['"]""", CSS_URL.sub(" ", match[1]))
    return refs


class References(HTMLParser):
    """Every URL in one HTML page (URL attributes, srcset and inline CSS) and its ids."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs, self.ids, self.in_style, self.active, self.text = [], set(), False, [], []

    def handle_starttag(self, tag, attrs):
        self.in_style = tag == "style"
        if tag in BREAK_TAGS:
            self.text.append("\n")  # a browser separates the text on either side
        if tag in ACTIVE_TAGS:
            self.active.append(f"<{tag}>")
        for name, value in attrs:
            if name.startswith("on") or name == "srcdoc":
                self.active.append(f"{name} on <{tag}>")
            if tag == "meta" and name == "http-equiv" and (value or "").lower() == "refresh":
                self.active.append("<meta http-equiv=refresh>")
            if value is None:
                continue
            if name == "style" and "\\" in value:
                self.active.append(f"a CSS escape in a style attribute on <{tag}>")
            if name == "id" and value:
                self.ids.add(value)
            elif name in URL_ATTRIBUTES:
                self.refs.append(value)
            elif name in ("srcset", "imagesrcset"):
                self.refs += [part.split()[0] for part in value.split(",") if part.strip()]
            elif name == "style" or "url(" in value.lower() or "image-set(" in value.lower():
                self.refs += css_refs(value)  # style, and SVG paint such as fill="url(#gradient)"

    handle_startendtag = handle_starttag

    def handle_endtag(self, tag):
        if tag == "style":
            self.in_style = False
        if tag in BREAK_TAGS:
            self.text.append("\n")

    def handle_data(self, data):
        if not self.in_style:
            self.text.append(data)  # entities already decoded: convert_charrefs is on
        if self.in_style:
            if "\\" in data:
                self.active.append("a CSS escape in a <style> block")
            self.refs += css_refs(data)


def kind(path: str) -> str:
    return posixpath.splitext(path)[1].lower()


def check_links(site: Site):
    """Every URL in every built HTML, SVG and CSS file, copied pages included, and no active content.

    The site is static: scripts, frames, event handlers, srcdoc, meta refresh and CSS escapes are
    refused outright rather than interpreted, so nothing the checks cannot read reaches the host.
    """
    pages, broken = {}, []
    for path, data in site.files.items():
        if kind(path) in (".html", ".svg"):
            parser = References()
            parser.feed(data.decode("utf-8", errors="replace"))
            parser.close()
            pages[path] = parser
            broken += [f"{path}: {item} is active content, which the site does not allow" for item in parser.active]
    for path, data in sorted(site.files.items()):
        if path in pages:
            refs = pages[path].refs
        elif kind(path) == ".css":
            text = data.decode("utf-8", errors="replace")
            if "\\" in text:
                broken.append(f"{path}: CSS escapes are not allowed, because the link check cannot read them")
            refs = css_refs(text)
        else:
            continue
        for ref in refs:
            scheme = SCHEME.match(ref)
            if scheme:
                if scheme[1].lower() not in SAFE_SCHEMES:
                    broken.append(f"{path}: {ref} uses {scheme[1]}:, which the site does not allow")
                continue
            if ref.startswith(("/", "\\")):
                broken.append(f"{path}: {ref} starts with a slash, which breaks under a sub-path")
                continue
            target, _, fragment = ref.partition("#")
            target = target.partition("?")[0]
            dest = posixpath.normpath(posixpath.join(posixpath.dirname(path), target)) if target else path
            if dest == "." or target.endswith("/"):
                dest = posixpath.join("" if dest == "." else dest, "index.html")
            if dest.startswith("..") or dest not in site.files:
                broken.append(f"{path}: {ref} leads to {dest}, which is not in the site")
            elif fragment and dest in pages and fragment not in pages[dest].ids:
                broken.append(f"{path}: {ref} names #{fragment}, which {dest} does not have")
    if broken:
        raise BuildError("broken links:\n  " + "\n  ".join(broken))


def write(site: Site):
    out, repo = site.out.resolve(), site.repo.resolve()
    if site.out.is_symlink():
        raise BuildError(f"{site.out} is a symbolic link, so it cannot be the output folder")
    if out == repo or out in repo.parents:
        raise BuildError(f"{out} holds the repository, so it cannot be the output folder")
    if out.exists():
        remove_previous_build(out)
    for path, data in site.files.items():
        target = out / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    listing = "".join(f"{hashlib.sha256(data).hexdigest()} {path}\n" for path, data in sorted(site.files.items()))
    (out / BUILD_MARKER).write_text(MARKER_TEXT + listing, encoding="utf-8", newline="\n")


def remove_previous_build(out: Path):
    """Delete an earlier build only when every file in the folder is one it wrote, unchanged."""
    present = {p.relative_to(out).as_posix(): p for p in out.rglob("*") if p.is_file() or p.is_symlink()}
    if not present:
        return
    marker = out / BUILD_MARKER
    text = marker.read_text(encoding="utf-8", errors="replace") if marker.is_file() else ""
    if not text.startswith(MARKER_TEXT):
        raise BuildError(f"{out} is not an earlier site build, so it will not be replaced")
    listed = {}
    for line in text[len(MARKER_TEXT):].splitlines():
        digest, _, path = line.partition(" ")
        listed[path] = digest
    for path, file in present.items():
        if path == BUILD_MARKER:
            continue
        if file.is_symlink() or path not in listed or hashlib.sha256(file.read_bytes()).hexdigest() != listed[path]:
            raise BuildError(f"{out} holds {path}, which the last build did not write, so nothing was replaced")
    for file in present.values():
        file.unlink()
    for folder in sorted((p for p in out.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
        folder.rmdir()


def scan(site: Site, denylist: Path) -> list:
    """Each built file and file name checked against the denylist, reported without the term."""
    entries = leak_scan.load_denylist(denylist)
    # The same entries with runs of whitespace collapsed, to compare with text a browser collapses too.
    collapsed = [leak_scan.Entry(entry.line, entry.kind, re.sub(r"\s+", " ", entry.text)) for entry in entries]
    hits = []
    for path, data in sorted(site.files.items()):
        shown = leak_scan.redact_path(path, entries)
        hits += [f"{shown} (file name): denylist line {entry.line}" for entry in entries if entry.found(path)]
        text = (data.decode("utf-8", errors="replace")
                if posixpath.splitext(path)[1].lower() in TEXT_TYPES else leak_scan.decode(data))
        if text is None:
            continue
        found = set(leak_scan.text_hits(text, entries))
        if kind(path) in (".html", ".svg"):
            # Also what a browser shows: entities decoded, tags removed, and whitespace collapsed on both sides.
            parser = References()
            parser.feed(text)
            parser.close()
            visible = "".join(parser.text)
            found |= {(line, entry) for line, entry in leak_scan.text_hits(html.unescape(text), entries)}
            seen = {entry for _, entry in found}
            extra = leak_scan.text_hits(visible, entries) + \
                leak_scan.text_hits(re.sub(r"\s+", " ", visible), collapsed)
            found |= {(0, entry) for _, entry in extra if entry not in seen}
        hits += [f"{shown}:{line or 'text'}: denylist line {entry}" for line, entry in sorted(found)]
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
.small { font-size: .9rem; color: var(--muted); }
.intro { max-width: 48rem; font-size: 1.05rem; }
section.wrap > h2 { font-size: clamp(1.5rem, 4vw, 2rem); margin-top: 2.2em; }
.split { display: grid; gap: 1.5rem; align-items: center; }
.hero-art { margin: 0; }
.hero-art img, .stage img, .role img { display: block; width: 100%; height: auto; border-radius: 12px; border: 1px solid var(--line); background: #fff; }
.pairs { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr)); margin: 1.5rem 0; }
.pair { border: 1px solid var(--line); border-radius: 12px; padding: 1rem 1.1rem; }
.pair p { margin: 0; }
.problem { color: var(--muted); font-size: .95rem; }
.problem::before { content: "Without a process, "; font-weight: 700; color: var(--ink); }
.answer { margin-top: .6rem !important; font-weight: 700; }
.answer::before { content: "With SHOTos, "; color: var(--purple); }
.overview { max-width: 60rem; }
.stage-grid, .role-grid { list-style: none; padding: 0; margin: 1.5rem 0; display: grid; gap: 1.5rem; grid-template-columns: repeat(auto-fit, minmax(19rem, 1fr)); }
.role-grid { grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr)); gap: 1.1rem; }
.stage figure { margin: 0 0 .75rem; }
.stage h3 { margin: .25rem 0 .4rem; }
.stage p { margin: .3rem 0; }
.step { font: 700 .85rem var(--head); color: var(--purple); letter-spacing: .06em; margin-right: .25rem; }
.hands { font-size: .95rem; color: var(--muted); }
.role a { display: block; text-decoration: none; color: var(--ink); border: 1px solid var(--line); border-radius: 14px; padding: .6rem .6rem 1rem; height: 100%; }
.role a:hover { border-color: var(--purple); }
.role img { border: 0; }
.role-name { display: block; font: 700 1.1rem var(--head); color: var(--purple); margin: .75rem .4rem .25rem; }
.role-text { display: block; margin: 0 .4rem; color: var(--muted); font-size: .95rem; }
.routes { display: grid; gap: 1.25rem; grid-template-columns: 1fr; margin: 1.5rem 0; }
.route { border: 1px solid var(--line); border-radius: 12px; padding: .25rem 1.1rem 1rem; min-width: 0; }
.route h3 { margin-top: .9rem; }
.route ol { padding-left: 1.2rem; }
.route li { margin: .35rem 0; }
.route.wide { grid-column: 1 / -1; }
@media (min-width: 900px) {
  .split { grid-template-columns: 1fr 1.05fr; gap: 2.5rem; }
  .routes { grid-template-columns: 1fr 1fr; }
}
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
