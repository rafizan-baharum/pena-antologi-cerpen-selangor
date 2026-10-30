#!/usr/bin/env python3
"""Build distributable formats into build/.

    python3 tools/build.py             # everything
    python3 tools/build.py epub tex    # only these

Targets: epub, tex, pdf, docx, html
"""
import subprocess
import sys
import shutil
import manuscript as m
import reference_docx

BUILD = m.REPO / "build"
STEM = "KUMCER"
HEADER = m.REPO / "tools" / "latex-header.tex"
COVER = (m.FRONT / m.COVER) if m.COVER else None

PAGEBREAK = '```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```'


def cover_header():
    """Generated header defining \\anthcover when a cover image is set."""
    p = BUILD / ".cover.tex"
    text = f"\\newcommand{{\\anthcover}}{{{COVER.as_posix()}}}\n" if COVER else ""
    p.write_text(text, encoding="utf-8")
    return p


def source(separators, fmt="md"):
    items = m.stories()
    return m.metadata_yaml(items) + "\n" + m.body(items, separators=separators, fmt=fmt)


# A5 trim, book class, Malay strings via latex-header.tex. No --toc: the
# contents page is placed by manuscript._front_latex().
TEXOPTS = [
    "-s", "--top-level-division=chapter",
    "-V", "documentclass=book",
    "-V", "classoption=openany", "-V", "classoption=oneside",
    "-V", "papersize=a5",
    "-V", "fontsize=11pt", "-V", "geometry:margin=2cm",
    "-V", "linkcolor=black", "-V", "lang=ms",
]


def run(args, label):
    try:
        subprocess.run(args, check=True, cwd=m.REPO, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"  ✗ {label}\n{(e.stderr or e.stdout or '').strip()[:900]}")
        return False
    out = BUILD / args[args.index("-o") + 1].split("/")[-1]
    size = out.stat().st_size / 1024
    unit = f"{size/1024:.1f} MB" if size > 1024 else f"{size:.0f} KB"
    print(f"  ✓ {label:<6} {out.name:<28} {unit}")
    return True


def write_tmp(name, text):
    p = BUILD / f".{name}.md"
    p.write_text(text, encoding="utf-8")
    return p


RES = ["--resource-path", f"{m.REPO}:{m.FRONT}"]


def build_epub():
    src = write_tmp("epub", source(separators=False))
    cover = [f"--epub-cover-image={COVER}"] if COVER else []
    return run(
        ["pandoc", str(src), *RES, "--from", "markdown", "--toc", "--toc-depth=1",
         *cover, "--epub-title-page=true", "-o", f"build/{STEM}.epub"],
        "epub",
    )


def _tex_args(src):
    return ["pandoc", str(src), *RES, "--from", "markdown+raw_attribute", *TEXOPTS,
            f"--include-in-header={cover_header()}",
            f"--include-in-header={HEADER}"]


def build_tex():
    src = write_tmp("tex", source(separators=False, fmt="latex"))
    return run([*_tex_args(src), "-o", f"build/{STEM}.tex"], "tex")


def build_pdf():
    src = write_tmp("pdf", source(separators=False, fmt="latex"))
    engine = shutil.which("tectonic") or shutil.which("xelatex")
    if not engine:
        print("  ✗ pdf    tiada LaTeX engine (pasang tectonic)")
        return False
    return run([*_tex_args(src), f"--pdf-engine={engine}", "-o", f"build/{STEM}.pdf"], "pdf")


def build_html():
    src = write_tmp("html", source(separators=True))
    return run(
        ["pandoc", str(src), *RES, "--from", "markdown", "-s", "--toc",
         "--toc-depth=1", "--embed-resources", "--metadata", "title-prefix=",
         "-o", f"build/{STEM}.html"],
        "html",
    )


def build_docx():
    # The docx writer does not start Heading 1 on a new page by itself.
    text = source(separators=False).replace("\n\n# ", f"\n\n{PAGEBREAK}\n\n# ")
    front, missing = m.front_page_md()
    if missing:
        print(f"  ! muka depan PENA tiada: {', '.join(missing)} (isi AUTHOR_DETAILS)")
    # Pandoc puts title, authors, then the contents list at the top. Author
    # details ride along as extra `author` lines (centred, 12 pt) so the front
    # page precedes the contents; TOC Heading starts a new page.
    rows = [l for l in front.split("\n\n") if l]
    authors = "".join(f'  - "{r}"\n' for r in rows)
    text = text.replace(f'author: "{m.AUTHOR}"\n',
                        f'author:\n  - "{m.AUTHOR}"\n{authors}toc-title: "Kandungan"\n', 1)
    src = write_tmp("docx", text)
    ref = reference_docx.make(BUILD / ".reference.docx")
    ok = run(
        ["pandoc", str(src), *RES, "--from", "markdown+raw_attribute",
         "--reference-doc", str(ref), "--toc", "--toc-depth=1",
         "-o", f"build/{STEM}.docx"],
        "docx",
    )
    ref.unlink(missing_ok=True)
    return ok


TARGETS = {
    "epub": build_epub,
    "tex": build_tex,
    "pdf": build_pdf,
    "docx": build_docx,
    "html": build_html,
}

if __name__ == "__main__":
    want = sys.argv[1:] or list(TARGETS)
    bad = [t for t in want if t not in TARGETS]
    if bad:
        sys.exit(f"target tidak dikenali: {', '.join(bad)}\nada: {', '.join(TARGETS)}")

    BUILD.mkdir(exist_ok=True)
    items = m.stories()
    print(f"{len(items)} cerpen / {m.total_words(items):,} kata → build/\n")

    ok = sum(TARGETS[t]() for t in want)
    for pattern in (".*.md", ".cover.tex"):
        for tmp in BUILD.glob(pattern):
            tmp.unlink()
    print(f"\n{ok}/{len(want)} berjaya")
    sys.exit(0 if ok == len(want) else 1)
