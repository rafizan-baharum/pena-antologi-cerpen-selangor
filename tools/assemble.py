#!/usr/bin/env python3
"""Assemble the readable manuscript: stories/*.md -> MANUSCRIPT.md

Order and story loading live in manuscript.py. For epub/tex/pdf/docx use build.py.
"""
import manuscript as m

OUT = m.REPO / "MANUSCRIPT.md"

items = m.stories()
toc = "\n".join(f"{i:02d}. {t}" for i, (t, _, _) in enumerate(items, 1))

title_block = f"# {m.TITLE}\n"
if m.SUBTITLE:
    title_block += f"## {m.SUBTITLE}\n"
title_block += f"\n**{m.AUTHOR}**"

blocks = [title_block, m.imprint_md(items)]
if m.EPIGRAPH:
    blocks.append(f"*{m.EPIGRAPH}*")
blocks.append(f"## Kandungan\n\n{toc}")

parts = ["\n\n---\n\n".join(blocks)]
for title, text, _ in items:
    parts.append(f"# {title}\n\n{text}")

OUT.write_text("\n\n---\n\n".join(parts).rstrip() + "\n", encoding="utf-8")

print(f"tulis {OUT.relative_to(m.REPO)}")
print(f"{len(items)} cerpen / {m.total_words(items):,} kata badan teks")
