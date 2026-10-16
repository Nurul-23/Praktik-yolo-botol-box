import cv2
from pathlib import Path

# Lokasi dataset asli
ROOT = Path(__file__).parent / "dataset_raw"

# Lokasi penyimpanan hasil anotasi
OUTPUT = Path(__file__).parent / "dataset_yolo"

KELAS = {
    0: "botol",
    1: "box",
}

EKSTENSI = {".jpg", ".jpeg", ".png"}

for nama_kelas in KELAS.values():
    (OUTPUT / "images").mkdir(parents=True, exist_ok=True)
    (OUTPUT / "labels").mkdir(parents=True, exist_ok=True)

(OUTPUT / "classes.txt").write_text(
    "\n".join(KELAS.values()) + "\n",
    encoding="utf-8",
)

# Variabel anotasi
gambar = None
kotak = []
titik_awal = None
sedang_menggambar = False


def mouse(event, x, y, flags, param):
    global titik_awal, sedang_menggambar, gambar

    if event == cv2.EVENT_LBUTTONDOWN:
        titik_awal = (x, y)
        sedang_menggambar = True

    elif event == cv2.EVENT_MOUSEMOVE and sedang_menggambar:
        tampilan = gambar.copy()

        for x1, y1, x2, y2 in kotak:
            cv2.rectangle(tampilan, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.rectangle(tampilan, titik_awal, (x, y), (0, 255, 255), 2)
        cv2.imshow("Anotasi YOLO", tampilan)

    elif event == cv2.EVENT_LBUTTONUP:
        sedang_menggambar = False

        x1 = min(titik_awal[0], x)
        y1 = min(titik_awal[1], y)
        x2 = max(titik_awal[0], x)
        y2 = max(titik_awal[1], y)

        if x2 > x1 and y2 > y1:
            kotak.append((x1, y1, x2, y2))

        tampilkan()


def tampilkan():
    global gambar

    tampilan = gambar.copy()

    for x1, y1, x2, y2 in kotak:
        cv2.rectangle(tampilan, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow("Anotasi YOLO", tampilan)


def simpan_label(img_path, img, daftar_kotak, class_id):
    tinggi, lebar = img.shape[:2]
    baris = []

    for x1, y1, x2, y2 in daftar_kotak:
        cx = ((x1 + x2) / 2) / lebar
        cy = ((y1 + y2) / 2) / tinggi
        bw = (x2 - x1) / lebar
        bh = (y2 - y1) / tinggi

        baris.append(
            f"{class_id} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}"
        )

    tujuan_gambar = OUTPUT / "images" / img_path.name
    tujuan_label = OUTPUT / "labels" / f"{img_path.stem}.txt"

    cv2.imwrite(str(tujuan_gambar), img)
    tujuan_label.write_text("\n".join(baris) + ("\n" if baris else ""),
                            encoding="utf-8")


def main():
    global gambar, kotak

    cv2.namedWindow("Anotasi YOLO", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Anotasi YOLO", 1000, 700)
    cv2.setMouseCallback("Anotasi YOLO", mouse)

    for class_id, nama_kelas in KELAS.items():
        folder = ROOT / nama_kelas

        if not folder.exists():
            print(f"Folder tidak ditemukan: {folder}")
            continue

        daftar_gambar = sorted(
            p for p in folder.iterdir()
            if p.suffix.lower() in EKSTENSI
        )

        for nomor, img_path in enumerate(daftar_gambar, start=1):
            gambar = cv2.imread(str(img_path))

            if gambar is None:
                print(f"Gagal membuka: {img_path.name}")
                continue

            kotak = []
            tampilkan()

            print(f"\nKelas: {nama_kelas}")
            print(f"Gambar {nomor}/{len(daftar_gambar)}: {img_path.name}")
            print("Tarik mouse untuk membuat kotak.")
            print("S = simpan | U = hapus kotak terakhir | N = lewati")

            while True:
                tombol = cv2.waitKey(0) & 0xFF

                if tombol == ord("s"):
                    if not kotak:
                        print("Belum ada kotak. Buat kotak sebelum menyimpan.")
                        continue

                    simpan_label(img_path, gambar, kotak, class_id)
                    print(f"Tersimpan: {img_path.name}")
                    break

                elif tombol == ord("u"):
                    if kotak:
                        kotak.pop()
                        tampilkan()

                elif tombol == ord("n"):
                    print("Gambar dilewati.")
                    break

                elif tombol == 27:
                    cv2.destroyAllWindows()
                    print("Anotasi dihentikan.")
                    return

    cv2.destroyAllWindows()
    print("\nAnotasi selesai.")
    print(f"Hasil disimpan di: {OUTPUT}")


if __name__ == "__main__":
    main()