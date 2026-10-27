# SUBMISSION.md
## Syarat Penghantaran

*Isi sebelum menulis. Semua yang kosong ialah soalan terbuka — jangan teka.*

| Perkara | Nilai |
|---|---|
| Penerima / penerbit / penganjur | Persatuan Penulis Nasional Malaysia (PENA) |
| Jenis penghantaran | _antologi penuh / cerpen individu / kertas cadangan_. Borang minta *Monograph* (satu/ramai pengarang untuk keseluruhan buku) atau *Edited Volume* (setiap bab pengarang berbeza) — pilih bila penulis antologi diputuskan |
| Tarikh tutup | _TBD_ |
| Bilangan cerpen | _TBD_ |
| Had kata setiap cerpen | _TBD_ |
| Jumlah kata keseluruhan | _TBD_ |
| Tema / syarat kandungan | _TBD_ |
| Format fail (docx / pdf / epub) | Microsoft Word (softcopy), atau hardcopy A4. Lihat spesifikasi di bawah |
| Penulisan: satu penulis atau ramai | _TBD_ |
| Nama pena / pengarang / penyunting | _TBD_ |
| Dokumen sokongan (sinopsis, bio, borang) | _TBD_ |
| Rujukan / pautan makluman | _TBD_ |

## Senarai Semak Sebelum Hantar

- [ ] Syarat di atas diisi dan dipadankan dengan manuskrip
- [ ] `TITLE`, `AUTHOR` dalam `tools/manuscript.py` disahkan
- [ ] Semua cerpen lulus pass `AI_NONO.md` dan voice pass
- [ ] Jumlah kata dalam had (`python3 tools/assemble.py`)
- [ ] Imprint / penafian fiksyen disemak
- [ ] Build format yang diminta; buka dan semak hasil
- [ ] Sinopsis dan bio penulis siap
- [ ] Halaman hadapan: nama, gelaran, jawatan, alamat penuh, nombor telefon, butir penulis — isi `AUTHOR_DETAILS` dalam `tools/manuscript.py`
- [x] Fail Word, A4, langkau dua baris, Times New Roman 12 pt (`tools/reference_docx.py`; build docx)
- [ ] Bahasa Melayu sahaja; tatabahasa Dewan
- [ ] Semua cerpen asli dan belum pernah diterbitkan (media cetak, elektronik, lain-lain)
- [x] Sekurang-kurangnya 38 muka surat (syarat ISBN) — ~24k kata dua baris ≈ 85+ muka
- [ ] Surat izin terbit sedia untuk dihantar ke PENA
- [ ] Bibliografi di akhir manuskrip (jika ada)
- [ ] Tiada elemen bertentangan dengan dasar Kerajaan Malaysia

---

## Borang Penghantaran PENA

Maklumat diperlukan dalam borang dalam talian (boleh simpan dan sambung kemudian; semak dan betulkan sebelum hantar):

- **Title** (wajib)
- **Submission Type** (wajib): Monograph atau Edited Volume. Edited Volume = setiap pengarang dikaitkan dengan bab sendiri; butiran bab diisi kemudian dalam proses
- **Submission Requirements** (wajib): perakuan terhadap panduan di bawah
- Muat naik fail, kenal pasti pengarang bersama, abstrak

Beri sebanyak mungkin butiran supaya editor dapat menilai karya.

## Panduan Penulisan Manuskrip (PENA)

- Bahasa Melayu sahaja.
- Karya asli boleh dihantar softcopy atau hardcopy untuk penilaian. Surat izin terbit perlu dihantar ke PENA.
- Nama, gelaran, jawatan, alamat penuh, nombor telefon dan butir penulis pada salah satu halaman hadapan manuskrip.
- Kertas putih A4 sahaja, langkau dua baris, Times New Roman atau Arial saiz 12.
- Tidak boleh hantar manuskrip yang ditulis oleh penulis lain, atau yang telah diterbitkan dalam media cetak, media elektronik atau bentuk terbitan lain.
- Lampirkan bibliografi di akhir manuskrip (jika ada).

## Panduan Gaya Penerbitan (PENA)

- **Nada:** profesional, berilmiah, jelas.
- **Khalayak sasaran:** sasterawan, cendekiawan, ahli akademik, profesional dalam bidang berkaitan.
- **Perisian:** Microsoft Word.
- **Format:** langkau dua baris, 12 pt, Times New Roman atau Arial diutamakan.
- **Petikan dan rujukan:** Gaya Dewan Edisi Keempat.
- **Bahasa:** Tatabahasa Dewan.

## Standard Penerbitan

- **ISBN / e-ISBN** + kod bar daripada Perpustakaan Negara Malaysia. Minimum **38 muka surat** untuk dapat ISBN.
- **ISSN / e-ISSN**: untuk penerbitan berkala sahaja (tidak terpakai untuk antologi ini).
- **Data CIP** (Cataloguing in Publication) daripada Perpustakaan Negara Malaysia untuk semua buku.
- Pengindeksan jurnal (MyJurnal, Google Scholar, MyCite, Scopus): tidak terpakai untuk antologi.

## Penilaian

- Jawatankuasa penilai ialah pakar dalam bidang yang dinilai.
- Jawatankuasa Pemilihan Judul Buku PENA-MALAYSIA MADANI berhak menolak manuskrip yang dipercayai bertentangan dengan dasar Kerajaan Malaysia atau boleh menjejaskan nama baik PENA.

## Penetapan Nama (kulit buku, Perjanjian Penerbitan, CIP)

| Peranan | Maksud |
|---|---|
| Penulis / Pengarang | Menulis sepenuhnya isi kandungan |
| Editor | Awasi pra-penerbitan: tatabahasa, pematuhan gaya |
| Penterjemah | Alih bahasa, kekalkan makna asal |
| Penyusun | Kumpul dan susun isi kandungan menjadi manuskrip lengkap |
| Pengarang bersama | Dua atau lebih penyumbang signifikan; kongsi hak cipta |
| Ilustrator | Rekaan visual: lukisan, gambar rajah |

Antologi ini kemungkinan perlukan peranan **Penyusun** (atau Editor) di samping Penulis. Putuskan sebelum isi `AUTHOR` dalam `tools/manuscript.py`.
