from pathlib import Path
import csv
import json
from collections import Counter

# ==========================================================
# SignSync - Landmark Dataset Statistics
# Task 3
#
# Reads the already-generated landmark CSV.
# Does NOT run MediaPipe again.
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_CSV = PROJECT_ROOT / "generated" / "asl_landmarks.csv"
OUTPUT_DIR = PROJECT_ROOT / "generated"

REPORT_JSON = OUTPUT_DIR / "landmark_statistics.json"
REPORT_TXT = OUTPUT_DIR / "landmark_statistics.txt"

# ----------------------------------------------------------
# Check input file
# ----------------------------------------------------------

if not INPUT_CSV.exists():
    print("=" * 60)
    print("SignSync Landmark Statistics")
    print("=" * 60)
    print("\nERROR: Landmark CSV not found.")
    print(f"Expected file:\n{INPUT_CSV}")
    print("\nRun extract_landmarks.py first.")
    exit()

# ----------------------------------------------------------
# Read CSV
# ----------------------------------------------------------

total_successful_samples = 0
class_counts = Counter()

with open(INPUT_CSV, "r", newline="", encoding="utf-8") as csv_file:

    reader = csv.DictReader(csv_file)

    for row in reader:

        label = row.get("label")

        if label:
            total_successful_samples += 1
            class_counts[label] += 1

# ----------------------------------------------------------
# Number of classes
# ----------------------------------------------------------

number_of_classes = len(class_counts)

# ----------------------------------------------------------
# Find largest and smallest classes
# ----------------------------------------------------------

largest_count = max(class_counts.values()) if class_counts else 0
smallest_count = min(class_counts.values()) if class_counts else 0

largest_classes = sorted(
    label for label, count in class_counts.items()
    if count == largest_count
)

smallest_classes = sorted(
    label for label, count in class_counts.items()
    if count == smallest_count
)

# ----------------------------------------------------------
# Print report
# ----------------------------------------------------------

print("=" * 60)
print("        SignSync Landmark Dataset Statistics")
print("=" * 60)

print(f"\nTotal Successful Samples : {total_successful_samples}")
print(f"Number of Classes       : {number_of_classes}")

print("\nSamples Per Class")
print("-" * 40)

for label in sorted(class_counts):
    print(f"{label:<12}: {class_counts[label]}")

print("\n" + "-" * 40)

print(
    f"Largest Class           : "
    f"{', '.join(largest_classes)} ({largest_count} samples)"
)

print(
    f"Smallest Class          : "
    f"{', '.join(smallest_classes)} ({smallest_count} samples)"
)

# ----------------------------------------------------------
# Create statistics dictionary
# ----------------------------------------------------------

statistics = {
    "total_successful_samples": total_successful_samples,
    "number_of_classes": number_of_classes,
    "samples_per_class": dict(
        sorted(class_counts.items())
    ),
    "largest_class": {
        "classes": largest_classes,
        "count": largest_count
    },
    "smallest_class": {
        "classes": smallest_classes,
        "count": smallest_count
    }
}

# ----------------------------------------------------------
# Save JSON report
# ----------------------------------------------------------

with open(REPORT_JSON, "w", encoding="utf-8") as json_file:

    json.dump(
        statistics,
        json_file,
        indent=4
    )

# ----------------------------------------------------------
# Save TXT report
# ----------------------------------------------------------

with open(REPORT_TXT, "w", encoding="utf-8") as txt_file:

    txt_file.write("SignSync Landmark Dataset Statistics\n")
    txt_file.write("=" * 50 + "\n\n")

    txt_file.write(
        f"Total Successful Samples : {total_successful_samples}\n"
    )

    txt_file.write(
        f"Number of Classes       : {number_of_classes}\n\n"
    )

    txt_file.write("Samples Per Class\n")
    txt_file.write("-" * 40 + "\n")

    for label in sorted(class_counts):
        txt_file.write(
            f"{label:<12}: {class_counts[label]}\n"
        )

    txt_file.write("\n")

    txt_file.write(
        f"Largest Class : "
        f"{', '.join(largest_classes)} "
        f"({largest_count} samples)\n"
    )

    txt_file.write(
        f"Smallest Class : "
        f"{', '.join(smallest_classes)} "
        f"({smallest_count} samples)\n"
    )

# ----------------------------------------------------------
# Completion
# ----------------------------------------------------------

print("\n" + "=" * 60)
print("Statistics Generated Successfully")
print("=" * 60)

print(f"\nJSON report:")
print(REPORT_JSON)

print(f"\nText report:")
print(REPORT_TXT)