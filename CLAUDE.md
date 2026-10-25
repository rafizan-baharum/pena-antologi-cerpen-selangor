# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Pena Antologi Cerpen Selangor

Projek antologi cerpen Bahasa Malaysia untuk **penghantaran (submission)** — Selangor. Struktur dan aliran kerja sama seperti `../pena-jpfn`, tetapi ini antologi: cerpen yang berdiri sendiri, dihimpun di bawah satu tema/penerbit/pertandingan, bukan satu dunia bersiri.

**Language:** Bahasa Malaysia
**Status:** Scaffold. Belum ada cerpen. Butiran penghantaran belum diisi — rujuk `SUBMISSION.md`.

Rujukan korpus dan juri: `../selangor-kini-cerpen` (analisis cerpen Selangor Kini / Hadiah Sastera Selangor).

---

## Project Documents

| Fail | Fungsi |
|---|---|
| `SUBMISSION.md` | **Syarat penghantaran** — penerima, tarikh tutup, had kata, format, borang. Isi dahulu |
| `MANUSCRIPT_ORDER.md` | Susunan antologi muktamad — sumber kebenaran tunggal. Menang atas dokumen lain |
| `WRITING_PLAN.md` | Status setiap cerpen, fasa kerja, isu terbuka, inventori kata |
| `STYLE_GUIDE.md` | Panduan bahasa, suara, format cerpen |
| `AI_NONO.md` | Tanda-tanda tulisan AI untuk dihapus (contoh dipinjam dari JPFN) |
| `MANUSCRIPT.md` | **OUTPUT** — jangan edit; jana semula |

Dokumen tambahan (tema, bible, ledger) ditambah bila perlu; jangan cipta sebelum ada keperluan.

---

## Struktur Fail

```
stories/          # MANUSKRIP AKTIF — semua kerja di sini. NN-slug.md
front-matter/     # Imej kulit dan aset lain (cover_front.png, dll)
notes/            # Nota kerja, riset, draf kasar — tidak masuk manuskrip
tools/            # assemble.py, build.py, manuscript.py, latex-header.tex
build/            # OUTPUT (gitignored)
```

Format setiap fail cerpen: baris pertama `# Tajuk`, kemudian badan. Footer `*Tajuk — N patah perkataan*` (jika ada) dibuang automatik semasa assemble.

Awalan `NN-` = susunan antologi. Susunan sebenar ialah `ORDER` dalam `tools/manuscript.py`; awalan yang tidak sepadan, atau fail dalam `stories/` yang tiada dalam `ORDER`, menyebabkan build gagal dengan sengaja.

---

## Tambah Cerpen Baru

1. Cipta `stories/NN-slug.md` (`# Tajuk` di baris 1)
2. Tambah `"slug"` dalam `ORDER` di `tools/manuscript.py` pada kedudukan NN
3. Kemas kini `MANUSCRIPT_ORDER.md` dan `WRITING_PLAN.md`
4. `python3 tools/assemble.py` untuk semak

---

## Jana Semula Manuskrip

```bash
python3 tools/assemble.py              # → MANUSCRIPT.md (sumber boleh baca)
python3 tools/build.py                 # → build/ (semua format)
python3 tools/build.py epub pdf        # → hanya target tertentu
```

**Keperluan:** `pandoc` (semua format) + `tectonic` atau `xelatex` (PDF sahaja).

Output: `build/ANTOLOGI.{epub,tex,pdf,docx,html}`. PDF: A5, kelas `book` + `openany` + `oneside`; halaman i tajuk, ii imprint, kandungan, cerpen pertama pada halaman arab 1.

**Metadata dalam `tools/manuscript.py` yang perlu disahkan:** `TITLE`, `AUTHOR`, `EPIGRAPH`, `COVER`, teks `IMPRINT`. `TITLE`/`AUTHOR` kini placeholder.

`build/` dan `MANUSCRIPT.md` ialah output — edit `stories/` dan jana semula.

---

## Sifat Kerja

Kerja dokumen-level: menulis, mengedit, menyusun fail cerpen. Tiada dependencies selain skrip assembly.
