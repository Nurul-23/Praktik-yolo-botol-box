from pathlib import Path
from collections import Counter

import cv2

ROOT = Path("dataset_yolo")
IMAGE_DIR = ROOT / "images"
LABEL_DIR = ROOT / "labels"

classes = [
    name.strip()
    for name in (ROOT / "classes.txt").read_text().splitlines()
    if name.strip()
]

extensions = {".jpg", ".jpeg", ".png"}
images = sorted(
    p for p in IMAGE_DIR.iterdir()
    if p.suffix.lower() in extensions
)

errors = []
class_counts = Counter()

for image_path in images:
    label_path = LABEL_DIR / f"{image_path.stem}.txt"

    if not label_path.exists():
        errors.append(f"{image_path.name}: file label tidak ditemukan")
        continue

    image = cv2.imread(str(image_path))

    if image is None:
        errors.append(f"{image_path.name}: gambar tidak dapat dibaca")
        continue

    height, width = image.shape[:2]

    lines = [
        line.strip()
        for line in label_path.read_text().splitlines()
        if line.strip()
    ]

    if not lines:
        errors.append(f"{label_path.name}: label kosong")
        continue

    for line_number, line in enumerate(lines, start=1):
        values = line.split()

        if len(values) != 5:
            errors.append(
                f"{label_path.name}, baris {line_number}: "
                "harus terdiri dari 5 nilai"
            )
            continue

        try:
            class_id = int(values[0])
            cx, cy, bw, bh = map(float, values[1:])
        except ValueError:
            errors.append(
                f"{label_path.name}, baris {line_number}: "
                "format angka tidak valid"
            )
            continue

        if not 0 <= class_id < len(classes):
            errors.append(
                f"{label_path.name}: class_id {class_id} tidak valid"
            )
            continue

        if not all(0 <= v <= 1 for v in (cx, cy, bw, bh)):
            errors.append(
                f"{label_path.name}: koordinat di luar rentang 0-1"
            )
            continue

        if bw <= 0 or bh <= 0:
            errors.append(
                f"{label_path.name}: lebar atau tinggi kotak tidak valid"
            )
            continue

        if (
            cx - bw / 2 < 0
            or cx + bw / 2 > 1
            or cy - bh / 2 < 0
            or cy + bh / 2 > 1
        ):
            errors.append(
                f"{label_path.name}: bounding box melewati batas gambar"
            )
            continue

        class_counts[classes[class_id]] += 1

print(f"Jumlah gambar: {len(images)}")
print(f"Jumlah kelas: {len(classes)}")
print(f"Nama kelas: {classes}")

print("\nJumlah objek berdasarkan kelas:")
for name in classes:
    print(f"- {name}: {class_counts[name]}")

print(f"\nJumlah masalah anotasi: {len(errors)}")

for error in errors[:30]:
    print("-", error)

if len(errors) > 30:
    print(f"... dan {len(errors) - 30} masalah lainnya")

if not errors:
    print("\nPemeriksaan format anotasi berhasil!")