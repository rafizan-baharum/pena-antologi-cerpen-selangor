#!/usr/bin/env python3
"""Shared manuscript model for the Selangor cerpen anthology.

Single source of truth for anthology order and for turning the per-story
files in stories/ into assembled bodies. Both assemble.py and build.py
import from here, so the order lives in exactly one place.

Keep ORDER in sync with MANUSCRIPT_ORDER.md.
"""
import re
import pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent
SRC = REPO / "stories"
FRONT = REPO / "front-matter"

# TODO: confirm before submission.
TITLE = "SECEBIS HARI DI SELANGOR"
SUBTITLE = ""
AUTHOR = "RB Arbi"
LANG = "ms"
EMAIL = "ra.harum76@gmail.com"
YEAR = 2026

# Canonical anthology order, one slug per story. Story files are
# stories/NN-<slug>.md. See MANUSCRIPT_ORDER.md.
ORDER = [
    "kisah-kisah-dongeng-tok-nek",
    "mak-su-datang-hari-ini",
    "titik-panas",
    "antara-buku-dan-buku-lima",
    "gelas-kaca-untuk-ibu",
    "sekejap-singgah",
    "ikan-halus-sungai-bernam",
    "hanya-dua-puluh-minit",
    "siakap-tasik-biru",
    "raja-puisi-tiga-jam",
    "sinekdoke",
    "anak-sulung-tidak-menangis-di-tepi-kubur",
    "lagu-terakhir-nami",
]

# Optional front matter. Leave empty to omit.
EPIGRAPH = ""
DEDICATION = ""

COVER = ""  # filename inside front-matter/, e.g. "cover_front.png"; "" = no cover

# Imprint / copyright page.
IMPRINT = [
    ("title", TITLE),
    ("rule", None),
    ("line", f"© {YEAR} {AUTHOR}"),
    (
        "para",
        "Hak cipta terpelihara. Tiada mana-mana bahagian daripada karya ini "
        "boleh diterbitkan semula, disimpan dalam sistem dapatan semula, atau "
        "dipindahkan dalam apa-apa bentuk tanpa kebenaran bertulis daripada "
        "penulis.",
    ),
    (
        "para",
        "Karya ini adalah fiksyen. Semua watak dan peristiwa adalah rekaan. "
        "Sebarang persamaan dengan individu atau peristiwa sebenar adalah "
        "tidak disengajakan.",
    ),
    ("rule", None),
    ("line", "Antologi cerpen · Bahasa Malaysia"),
    ("line", "{n} cerpen · {words} patah perkataan"),
    ("line", "Manuskrip. Tidak untuk edaran."),
    ("rule", None),
    ("line", AUTHOR),
    ("line", EMAIL),
]

_FOOTER = re.compile(r"^\*.*patah perkataan\*$")


def story_path(slug):
    """Resolve a slug to its numbered file, e.g. "intro" -> 01-intro.md.

    The NN- prefix is a convenience so files sort in reading order in an
    editor; ORDER is the source of truth. A disagreeing prefix is an error to
    fix, not a reordering to honour.
    """
    pattern = re.compile(rf"^(\d+)-{re.escape(slug)}\.md$")
    hits = sorted(f for f in SRC.iterdir() if pattern.match(f.name))
    if not hits:
        raise FileNotFoundError(f"{slug}: no NN-{slug}.md in {SRC}")
    if len(hits) > 1:
        raise ValueError(f"{slug}: {len(hits)} numbered copies: "
                         + ", ".join(f.name for f in hits))
    path = hits[0]
    want = ORDER.index(slug) + 1
    got = int(pattern.match(path.name).group(1))
    if got != want:
        raise ValueError(
            f"{path.name}: prefix {got:02d} but ORDER position is {want:02d}. "
            "Rename the file, or fix ORDER and MANUSCRIPT_ORDER.md."
        )
    return path


def load(slug):
    """Return (title, body, wordcount) with H1 and stale wordcount footer gone."""
    lines = story_path(slug).read_text(encoding="utf-8").split("\n")

    if not lines[0].startswith("# "):
        raise ValueError(f"{slug}: missing H1 title")
    title = lines[0][2:].strip()
    lines = lines[1:]

    def rstrip_blank():
        while lines and not lines[-1].strip():
            lines.pop()

    # Drop only the LAST "---" + "*Title — N patah perkataan*" pair; interior
    # "---" are scene breaks.
    rstrip_blank()
    if lines and _FOOTER.match(lines[-1].strip()):
        lines.pop()
        rstrip_blank()
        if lines and lines[-1].strip() == "---":
            lines.pop()
    rstrip_blank()

    body = "\n".join(lines).strip("\n")
    return title, body, len(body.split())


def check_orphans():
    """Story files on disk that ORDER does not list."""
    listed = {f"-{s}.md" for s in ORDER}
    return sorted(
        f.name for f in SRC.glob("*.md")
        if not any(f.name.endswith(s) for s in listed)
    )


def stories():
    orphans = check_orphans()
    if orphans:
        raise ValueError("not in ORDER: " + ", ".join(orphans))
    return [load(s) for s in ORDER]


def total_words(items=None):
    return sum(w for _, _, w in (items or stories()))


def imprint_lines(items):
    out = []
    for kind, text in IMPRINT:
        if text is not None:
            text = text.format(n=len(items), words=f"{total_words(items):,}")
        out.append((kind, text))
    return out


def imprint_md(items):
    out = []
    for kind, text in imprint_lines(items):
        if kind == "rule":
            out.append("<br>")
        elif kind == "title":
            out.append(f"**{text}**")
        else:
            out.append(text)
    return "\n\n".join(out)


def imprint_latex(items):
    """Imprint as raw LaTeX: page ii, no running head, small type."""
    rows = []
    for kind, text in imprint_lines(items):
        if kind == "rule":
            rows.append("\\medskip")
        elif kind == "title":
            rows.append(f"{{\\bfseries {text}}}\\par")
        elif kind == "para":
            rows.append(f"\\par {text}\\par")
        else:
            rows.append(f"{text}\\par")
    return (
        "\\thispagestyle{plain}\n"
        "\\begingroup\\footnotesize\\raggedright\n"
        "\\vspace*{\\fill}\n" + "\n".join(rows) + "\n"
        "\\vspace*{\\fill}\n"
        "\\par\\endgroup"
    )


def _epigraph_latex():
    if not EPIGRAPH:
        return None
    return (
        "\\clearpage\n\\thispagestyle{empty}\n\\vspace*{\\fill}\n"
        f"\\begin{{center}}\n\\emph{{{EPIGRAPH}}}\n\\end{{center}}\n"
        "\\vspace*{\\fill}"
    )


def _front_latex(items):
    """Front matter as raw LaTeX: imprint, epigraph, contents, then mainmatter.

    Hand-rolled because pandoc's book template fires \\mainmatter right after
    \\maketitle; we need the imprint on page ii and \\tableofcontents placed
    ourselves (no --toc), then arabic numbering restarting at 1.
    """
    pages = [imprint_latex(items)]
    epi = _epigraph_latex()
    if epi:
        pages.append(epi)
    pages.append("\\clearpage\n\\tableofcontents")
    return (
        "```{=latex}\n"
        "\\pagenumbering{roman}\\setcounter{page}{2}\n\n"
        + "\n\n".join(pages)
        + "\n\n\\clearpage\n\\mainmatter\n```"
    )


def body(items, separators=True, fmt="md"):
    """Assemble front matter + stories.

    separators=True puts a rule between units (readable .md). False for
    epub/docx, where the chapter break already starts a new page.
    """
    if fmt == "latex":
        front = _front_latex(items)
    else:
        joiner = "\n\n---\n\n" if separators else "\n\n"
        parts = [imprint_md(items)]
        if EPIGRAPH:
            parts.append(f"*{EPIGRAPH}*")
        front = joiner.join(parts)

    chunks = [front]
    for title, text, _ in items:
        head = "\n---\n\n" if separators else "\n"
        chunks.append(f"{head}# {title}\n\n{text}\n")
    return "\n".join(chunks).rstrip() + "\n"


def metadata_yaml(items):
    sub = f'subtitle: "{SUBTITLE}"\n' if SUBTITLE else ""
    return (
        "---\n"
        f'title: "{TITLE}"\n'
        f"{sub}"
        f'author: "{AUTHOR}"\n'
        f"lang: {LANG}\n"
        f'description: "Antologi {len(items)} cerpen."\n'
        "---\n"
    )
