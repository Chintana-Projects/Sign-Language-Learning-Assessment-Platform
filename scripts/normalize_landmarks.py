from pathlib import Path
import csv

# ==========================================================
# SignSync - Landmark Normalization
# Task 4: Optional / Recommended
#
# Reads:
#   generated/asl_landmarks.csv
#
# Creates:
#   generated/asl_landmarks_normalized.csv
#
# The original CSV is NOT modified.
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_CSV = PROJECT_ROOT / "generated" / "asl_landmarks.csv"
OUTPUT_CSV = PROJECT_ROOT / "generated" / "asl_landmarks_normalized.csv"

# ----------------------------------------------------------
# Check input file
# ----------------------------------------------------------

if not INPUT_CSV.exists():
    print("=" * 60)
    print("SignSync Landmark Normalization")
    print("=" * 60)
    print("\nERROR: Input landmark CSV was not found.")
    print(f"Expected:\n{INPUT_CSV}")
    print("\nRun extract_landmarks.py first.")
    exit()

# ----------------------------------------------------------
# Create header
# ----------------------------------------------------------

header = []

for i in range(21):
    header.extend([
        f"x{i}",
        f"y{i}",
        f"z{i}"
    ])

header.append("label")

# ----------------------------------------------------------
# Counters
# ----------------------------------------------------------

total_samples = 0
normalized_samples = 0
skipped_samples = 0

# ----------------------------------------------------------
# Start normalization
# ----------------------------------------------------------

print("=" * 60)
print("        SignSync Landmark Normalization")
print("=" * 60)

print(f"\nInput CSV:")
print(INPUT_CSV)

print("\nProcessing...")

with open(INPUT_CSV, "r", newline="", encoding="utf-8") as input_file, \
     open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as output_file:

    reader = csv.DictReader(input_file)
    writer = csv.writer(output_file)

    writer.writerow(header)

    for row in reader:

        total_samples += 1

        try:
            # --------------------------------------------------
            # Read the 21 landmarks
            # --------------------------------------------------

            landmarks = []

            for i in range(21):

                x = float(row[f"x{i}"])
                y = float(row[f"y{i}"])
                z = float(row[f"z{i}"])

                landmarks.append([x, y, z])

            label = row["label"]

            # --------------------------------------------------
            # Use Landmark 0 (wrist) as reference point.
            #
            # This makes the coordinates relative to the wrist
            # instead of the original image position.
            # --------------------------------------------------

            wrist_x = landmarks[0][0]
            wrist_y = landmarks[0][1]
            wrist_z = landmarks[0][2]

            normalized = []

            for x, y, z in landmarks:

                normalized_x = x - wrist_x
                normalized_y = y - wrist_y
                normalized_z = z - wrist_z

                normalized.extend([
                    normalized_x,
                    normalized_y,
                    normalized_z
                ])

            # --------------------------------------------------
            # Add label
            # --------------------------------------------------

            normalized.append(label)

            writer.writerow(normalized)

            normalized_samples += 1

        except (ValueError, KeyError, TypeError):
            skipped_samples += 1
            continue

# ----------------------------------------------------------
# Summary
# ----------------------------------------------------------

print("\n" + "=" * 60)
print("        Normalization Complete")
print("=" * 60)

print(f"\nTotal Samples      : {total_samples}")
print(f"Normalized Samples : {normalized_samples}")
print(f"Skipped Samples    : {skipped_samples}")

print("\nNormalized CSV saved to:")
print(OUTPUT_CSV)

print("\nOriginal CSV was NOT modified.")
print("=" * 60)