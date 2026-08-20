from pathlib import Path
import csv

# ==========================================================
# SignSync Dataset Explorer
# Explores the merged dataset and exports statistics
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "datasets" / "merged_dataset"
CSV_PATH = Path(__file__).resolve().parent / "dataset_statistics.csv"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}

print("=" * 60)
print("           SignSync Dataset Explorer")
print("=" * 60)

# ----------------------------------------------------------
# Check dataset
# ----------------------------------------------------------

if not DATASET_PATH.exists():
    print("Merged dataset not found.")
    exit()

# ----------------------------------------------------------
# Find all class folders
# ----------------------------------------------------------

class_folders = sorted(
    [folder for folder in DATASET_PATH.iterdir() if folder.is_dir()],
    key=lambda folder: folder.name
)

total_images = 0
class_statistics = []

print("\nClasses Found:\n")

for folder in class_folders:

    image_count = sum(
        1
        for file in folder.iterdir()
        if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS
    )

    total_images += image_count

    class_statistics.append((folder.name, image_count))

    print(f"{folder.name:<10} : {image_count}")

# ----------------------------------------------------------
# Largest and Smallest Classes
# ----------------------------------------------------------

largest_class = max(class_statistics, key=lambda x: x[1])
smallest_class = min(class_statistics, key=lambda x: x[1])

print("\n" + "=" * 60)
print(f"Total Classes   : {len(class_folders)}")
print(f"Total Images    : {total_images}")
print(f"Largest Class   : {largest_class[0]} ({largest_class[1]} images)")
print(f"Smallest Class  : {smallest_class[0]} ({smallest_class[1]} images)")
print("=" * 60)

# ----------------------------------------------------------
# Export to CSV
# ----------------------------------------------------------

with open(CSV_PATH, "w", newline="") as csv_file:

    writer = csv.writer(csv_file)

    writer.writerow(["Class", "Number of Images"])

    for class_name, count in class_statistics:
        writer.writerow([class_name, count])

    writer.writerow([])
    writer.writerow(["Total Classes", len(class_folders)])
    writer.writerow(["Total Images", total_images])
    writer.writerow(["Largest Class", largest_class[0], largest_class[1]])
    writer.writerow(["Smallest Class", smallest_class[0], smallest_class[1]])

print(f"\nCSV report saved successfully:")
print(CSV_PATH)