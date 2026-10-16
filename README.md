# Praktik Terpadu RET503 — Data dan YOLO

## Identitas
- Nama: Nurul Aisyah
- NIM: 4222401011
- Dataset: Deteksi objek botol dan box
- Model: YOLOv8n
- Perangkat: CPU AMD Ryzen 5 PRO 2500U

## 1. Dataset
Dataset terdiri dari dua kelas:
- botol
- box

Total data: 100 gambar.
Pembagian dataset:
- Train: 70 gambar
- Validation: 20 gambar
- Test: 10 gambar

Anotasi diperiksa menggunakan skrip pemeriksaan anotasi dari dosen.

## 2. Eksperimen
Pelatihan dilakukan menggunakan 5 epoch untuk percobaan awal.

| Eksperimen | Konfigurasi | mAP50 | mAP50-95 |
|---|---|---:|---:|
| E1 Pretrained | Model pralatih | 0.882 | 0.539 |
| E2 Scratch | Pelatihan dari awal | 0.008 | 0.001 |
| E3 Tuning | imgsz=640 | 0.744 | 0.445 |

## 3. Model Terbaik
E1 Pretrained terpilih berdasarkan nilai mAP50-95 validasi tertinggi, yaitu 0.539.

Lokasi model:
`hasil_praktik/E1_pretrained/weights/best.pt`

## 4. Hasil Pengujian (Test)
- mAP50: 0.937 (93.7%)
- mAP50-95: 0.573 (57.3%)

Pengujian dilakukan pada 10 gambar test. Karena jumlah data test masih terbatas, hasil ini merupakan evaluasi awal dan belum mewakili seluruh kondisi penggunaan.

## 5. Kesimpulan
Pada percobaan awal, E1 Pretrained memberikan hasil validasi terbaik dibandingkan E2 Scratch dan E3 Tuning. Hasil ini menunjukkan bahwa penggunaan model pralatih membantu pelatihan pada dataset kecil.

## 6. Berkas Hasil
- `hasil_praktik_4222401011.txt`
- `hasil_praktik_4222401011.csv`
- `hasil_praktik/E1_pretrained/results.png`
- `hasil_praktik/E3_tuning/results.png`
- `hasil_praktik/E1_pretrained/weights/best.pt`