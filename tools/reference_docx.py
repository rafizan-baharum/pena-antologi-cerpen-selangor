#!/usr/bin/env python3
"""Make a pandoc reference.docx that meets the PENA manuscript spec.

A4, Times New Roman 12 pt, double-spaced, black headings. Called by build.py.
"""
import re
import subprocess
import zipfile
from pathlib import Path

TNR = '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="Times New Roman" w:cs="Times New Roman" />'
SECT = ('<w:sectPr><w:footnotePr><w:numRestart w:val="eachSect" /></w:footnotePr>'
        '<w:pgSz w:w="11906" w:h="16838" />'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
        'w:header="709" w:footer="709" w:gutter="0" />'
        '<w:pgNumType w:start="1" /></w:sectPr>')


def _style(xml, sid, fn):
    pat = re.compile(rf'<w:style [^>]*w:styleId="{sid}".*?</w:style>', re.S)
    return pat.sub(lambda m: fn(m.group(0)), xml, count=1)


def _restyle(block, ppr, rpr):
    block = re.sub(r"<w:pPr>.*?</w:pPr>", "", block, flags=re.S)
    block = re.sub(r"<w:rPr>.*?</w:rPr>", "", block, flags=re.S)
    return block.replace("</w:style>", f"<w:pPr>{ppr}</w:pPr><w:rPr>{rpr}</w:rPr></w:style>")


def make(out: Path):
    raw = out.with_suffix(".raw.docx")
    with open(raw, "wb") as f:
        f.write(subprocess.run(["pandoc", "--print-default-data-file", "reference.docx"],
                               check=True, capture_output=True).stdout)
    zin = zipfile.ZipFile(raw)
    files = {n: zin.read(n) for n in zin.namelist()}
    s = files["word/styles.xml"].decode("utf-8")

    s = re.sub(r"<w:rPrDefault>.*?</w:rPrDefault>",
               f'<w:rPrDefault><w:rPr>{TNR}<w:sz w:val="24" /><w:szCs w:val="24" />'
               '<w:lang w:val="ms-MY" w:eastAsia="zh-CN" w:bidi="ar-SA" /></w:rPr></w:rPrDefault>',
               s, flags=re.S)
    s = re.sub(r"<w:pPrDefault>.*?</w:pPrDefault>",
               '<w:pPrDefault><w:pPr><w:spacing w:after="0" w:line="480" w:lineRule="auto" />'
               "</w:pPr></w:pPrDefault>", s, flags=re.S)

    body = '<w:spacing w:before="0" w:after="0" w:line="480" w:lineRule="auto" /><w:ind w:firstLine="720" />'
    flush = '<w:spacing w:before="0" w:after="0" w:line="480" w:lineRule="auto" />'
    s = _style(s, "BodyText", lambda b: _restyle(b, body, ""))
    s = _style(s, "FirstParagraph", lambda b: _restyle(b, "", ""))
    s = _style(s, "Compact", lambda b: _restyle(b, flush, ""))
    head = ('<w:keepNext /><w:keepLines /><w:spacing w:before="0" w:after="0" w:line="480" '
            'w:lineRule="auto" /><w:jc w:val="center" /><w:outlineLvl w:val="0" />')
    s = _style(s, "Heading1", lambda b: _restyle(
        b, head, f'{TNR}<w:b /><w:bCs /><w:color w:val="000000" /><w:sz w:val="28" /><w:szCs w:val="28" />'))
    ctr = '<w:spacing w:before="0" w:after="0" w:line="480" w:lineRule="auto" /><w:jc w:val="center" />'
    s = _style(s, "Title", lambda b: _restyle(
        b, ctr, f'{TNR}<w:b /><w:color w:val="000000" /><w:sz w:val="32" /><w:szCs w:val="32" />'))
    s = _style(s, "Author", lambda b: _restyle(
        b, ctr, f'{TNR}<w:color w:val="000000" /><w:sz w:val="24" /><w:szCs w:val="24" />'))
    s = _style(s, "TOCHeading", lambda b: _restyle(
        b, head.replace('<w:outlineLvl w:val="0" />', "<w:pageBreakBefore />"),
        f'{TNR}<w:b /><w:color w:val="000000" /><w:sz w:val="28" /><w:szCs w:val="28" />'))
    files["word/styles.xml"] = s.encode("utf-8")

    d = files["word/document.xml"].decode("utf-8")
    d = re.sub(r"<w:sectPr>.*?</w:sectPr>", SECT, d, flags=re.S)
    files["word/document.xml"] = d.encode("utf-8")

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for n, data in files.items():
            z.writestr(n, data)
    raw.unlink()
    return out
