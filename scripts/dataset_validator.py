import os
import cv2
import shutil
from pathlib import Path

# =====================================================
# CONFIGURATION
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_DIR = PROJECT_ROOT / "datasets" / "custom_webcam"

REJECTED_DIR = PROJECT_ROOT / "datasets" / "rejected"

VALID_EXTENSIONS = (".jpg", ".jpeg", ".png")

EXPECTED_WIDTH = 224
EXPECTED_HEIGHT = 224

BLUR_THRESHOLD = 120

# =====================================================
# CREATE REJECTED FOLDER
# =====================================================

REJECTED_DIR.mkdir(parents=True, exist_ok=True)

# =====================================================
# STATISTICS
# =====================================================

overall_total = 0
overall_valid = 0
overall_blurry = 0
overall_corrupted = 0
overall_wrong_size = 0

print("\n" + "=" * 65)
print("         SignSync Dataset Validation Report")
print("=" * 65)

# =====================================================
# PROCESS EACH LETTER
# =====================================================

for class_folder in sorted(DATASET_DIR.iterdir()):

    if not class_folder.is_dir():
        continue

    class_name = class_folder.name

    rejected_class = REJECTED_DIR / class_name
    rejected_class.mkdir(parents=True, exist_ok=True)

    total = 0
    valid = 0
    blurry = 0
    corrupted = 0
    wrong_size = 0

    for image_path in class_folder.iterdir():

        if image_path.suffix.lower() not in VALID_EXTENSIONS:
            continue

        total += 1

        image = cv2.imread(str(image_path))

        # -----------------------------
        # Corrupted image
        # -----------------------------
        if image is None:

            corrupted += 1

            shutil.move(
                str(image_path),
                str(rejected_class / image_path.name)
            )

            continue

        h, w = image.shape[:2]

        # -----------------------------
        # Wrong size
        # -----------------------------
        if w != EXPECTED_WIDTH or h != EXPECTED_HEIGHT:

            wrong_size += 1

            shutil.move(
                str(image_path),
                str(rejected_class / image_path.name)
            )

            continue

        # -----------------------------
        # Blur Detection
        # -----------------------------
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

        if blur_score < BLUR_THRESHOLD:

            blurry += 1

            shutil.move(
                str(image_path),
                str(rejected_class / image_path.name)
            )

            continue

        valid += 1

    overall_total += total
    overall_valid += valid
    overall_blurry += blurry
    overall_corrupted += corrupted
    overall_wrong_size += wrong_size

    print(f"\nLetter : {class_name}")
    print("-" * 35)
    print(f"Total Images      : {total}")
    print(f"Valid Images      : {valid}")
    print(f"Blurry Images     : {blurry}")
    print(f"Corrupted Images  : {corrupted}")
    print(f"Wrong Size Images : {wrong_size}")

print("\n" + "=" * 65)
print("OVERALL DATASET")
print("=" * 65)

print(f"Total Images      : {overall_total}")
print(f"Valid Images      : {overall_valid}")
print(f"Blurry Images     : {overall_blurry}")
print(f"Corrupted Images  : {overall_corrupted}")
print(f"Wrong Size Images : {overall_wrong_size}")

accuracy = (overall_valid / overall_total * 100) if overall_total else 0

print(f"\nDataset Quality : {accuracy:.2f}%")

print("\nValidation Complete.")