# MANUSCRIPT_ORDER.md
## Susunan Kumcer Muktamad

*Sumber kebenaran tunggal untuk urutan. Semua fail dalam `stories/`. Kekalkan selaras dengan `ORDER` dalam `tools/manuscript.py`.*

**15 unit / 25,961 patah perkataan**

**Tajuk:** Secebis Hari di Selangor · **Pengarang:** RB Arbi

| # | Tajuk | Fail | Kata |
|---|---|---|---|
| 1 | Kisah-kisah Dongeng Tok Nek | `01-kisah-kisah-dongeng-tok-nek.md` | 2,420 |
| 2 | Sekejap Singgah | `02-sekejap-singgah.md` | 2,022 |
| 3 | Titik Panas | `03-titik-panas.md` | 1,557 |
| 4 | Mak Su Datang Hari Ini | `04-mak-su-datang-hari-ini.md` | 1,996 |
| 5 | Sinekdoke | `05-sinekdoke.md` | 1,990 |
| 6 | Gelas Kaca untuk Ibu | `06-gelas-kaca-untuk-ibu.md` | 1,620 |
| 7 | Antara Buku dan Buku Lima | `07-antara-buku-dan-buku-lima.md` | 1,247 |
| 8 | Ikan Halus Sungai Bernam | `08-ikan-halus-sungai-bernam.md` | 2,121 |
| 9 | Raja Puisi | `09-raja-puisi.md` | 1,512 |
| 10 | Siakap Tasik Biru | `10-siakap-tasik-biru.md` | 2,196 |
| 11 | Lagu Terakhir Nami | `11-lagu-terakhir-nami.md` | 2,535 |
| 12 | Anak Sulung Tidak Menangis di Tepi Kubur | `12-anak-sulung-tidak-menangis-di-tepi-kubur.md` | 1,076 |
| 13 | Hanya Dua Puluh Minit Dari Kota | `13-hanya-dua-puluh-minit.md` | 1,119 |
| 14 | Di Bawah Payung Rahmah Ini | `14-di-bawah-payung-rahmah-ini.md` | 1,681 |
| 15 | Syif Terakhir | `15-syif-terakhir.md` | 869 |

## Logik Susunan

Tok Nek membuka (cerita disimpan, antologi disebut) dan Syif Terakhir menutup (satu lagi perjalanan, hidup diteruskan). Di antara: berat dan ringan berselang. Selepas cerpen yang menekan (Titik Panas, Mak Su) datang yang lebih ringan atau ironis (Sinekdoke); dua cerpen spekulatif (Gelas Kaca 2075, Siakap 2526) dipisahkan supaya tidak menjadi blok. Suara bentuk-pelik (Raja Puisi sebagai surat, Nami panjang) di tengah. Kehilangan memuncak secara berperingkat: Anak Sulung (sunyi, tertahan), Hanya Dua Puluh Minit (jeritan terus kepada kota), Di Bawah Payung Rahmah Ini (kematian yang melahirkan). Rahmat yang dinamakan di hujung cerpen ke-14 menyediakan pintu untuk Shahir menekan *Terima*.

## Output Dijana

`python3 tools/assemble.py && python3 tools/build.py` → `MANUSCRIPT.md`, `build/KUMCER.*`.
