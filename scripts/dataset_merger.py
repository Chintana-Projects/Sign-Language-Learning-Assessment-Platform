import shutil
from pathlib import Path

# ==========================================================
# SignSync Dataset Merger
# Merges:
#   datasets/asl_alphabet_train
#   datasets/custom_webcam
# into:
#   datasets/merged_dataset
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ASL_DATASET = PROJECT_ROOT / "datasets" / "asl_alphabet_train"
WEBCAM_DATASET = PROJECT_ROOT / "datasets" / "custom_webcam"
MERGED_DATASET = PROJECT_ROOT / "datasets" / "merged_dataset"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}

print("=" * 60)
print("          SignSync Dataset Merger")
print("=" * 60)

# ----------------------------------------------------------
# Check datasets
# ----------------------------------------------------------

if not ASL_DATASET.exists():
    print("ERROR: ASL training dataset not found.")
    exit()

if not WEBCAM_DATASET.exists():
    print("ERROR: Custom webcam dataset not found.")
    exit()

# ----------------------------------------------------------
# Create merged dataset
# ----------------------------------------------------------

MERGED_DATASET.mkdir(exist_ok=True)

total_asl = 0
total_webcam = 0
total_merged = 0

# Read all class folders from ASL dataset
classes = sorted(
    [folder.name for folder in ASL_DATASET.iterdir() if folder.is_dir()]
)

for class_name in classes:

    print(f"\nProcessing Class: {class_name}")

    merged_class = MERGED_DATASET / class_name
    merged_class.mkdir(parents=True, exist_ok=True)

    asl_count = 0
    webcam_count = 0

    # ======================================================
    # Copy ASL Images
    # ======================================================

    asl_folder = ASL_DATASET / class_name

    if asl_folder.exists():

        for image in sorted(asl_folder.iterdir()):

            if image.suffix.lower() not in IMAGE_EXTENSIONS:
                continue

            asl_count += 1

            new_name = f"asl_{class_name}_{asl_count:06d}{image.suffix.lower()}"

            shutil.copy2(
                image,
                merged_class / new_name
            )

    # ======================================================
    # Copy Webcam Images (Only A-Z exist)
    # ======================================================

    webcam_folder = WEBCAM_DATASET / class_name

    if webcam_folder.exists():

        for image in sorted(webcam_folder.iterdir()):

            if image.suffix.lower() not in IMAGE_EXTENSIONS:
                continue

            webcam_count += 1

            new_name = f"webcam_{class_name}_{webcam_count:06d}{image.suffix.lower()}"

            shutil.copy2(
                image,
                merged_class / new_name
            )

    merged_count = asl_count + webcam_count

    total_asl += asl_count
    total_webcam += webcam_count
    total_merged += merged_count

    print(f"ASL Images      : {asl_count}")
    print(f"Webcam Images   : {webcam_count}")
    print(f"Merged Images   : {merged_count}")

# ==========================================================
# Summary
# ==========================================================

print("\n" + "=" * 60)
print("Merge Completed Successfully")
print("=" * 60)

print(f"Total ASL Images      : {total_asl}")
print(f"Total Webcam Images   : {total_webcam}")
print(f"Total Merged Images   : {total_merged}")

print("\nMerged dataset saved to:")
print(MERGED_DATASET)