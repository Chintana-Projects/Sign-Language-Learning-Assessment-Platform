from pathlib import Path
import csv

# ==========================================================
# SignSync - Dataset Builder
# Task 2: Build Landmark Dataset
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_CSV = PROJECT_ROOT / "generated" / "asl_landmarks.csv"
OUTPUT_CSV = PROJECT_ROOT / "generated" / "landmarks.csv"


def build_dataset():

    if not INPUT_CSV.exists():
        raise FileNotFoundError(
            f"Landmark extraction file not found:\n{INPUT_CSV}"
        )

    # ------------------------------------------------------
    # Create required column names
    # ------------------------------------------------------

    header = []

    for i in range(21):
        header.extend([
            f"x{i}",
            f"y{i}",
            f"z{i}"
        ])

    header.append("label")

    # ------------------------------------------------------
    # Read extracted landmarks
    # ------------------------------------------------------

    rows = []

    with open(
        INPUT_CSV,
        "r",
        newline="",
        encoding="utf-8"
    ) as input_file:

        reader = csv.reader(input_file)

        # Skip existing header
        next(reader, None)

        for row in reader:

            if len(row) != 64:
                continue

            rows.append(row)

    # ------------------------------------------------------
    # Write final dataset
    # ------------------------------------------------------

    with open(
        OUTPUT_CSV,
        "w",
        newline="",
        encoding="utf-8"
    ) as output_file:

        writer = csv.writer(output_file)

        writer.writerow(header)

        writer.writerows(rows)

    return {
        "rows": len(rows),
        "columns": len(header),
        "output_file": str(OUTPUT_CSV)
    }


if __name__ == "__main__":

    print("=" * 60)
    print("SignSync Dataset Builder")
    print("=" * 60)

    result = build_dataset()

    print()
    print(f"Samples : {result['rows']}")
    print(f"Columns : {result['columns']}")
    print(f"Saved   : {result['output_file']}")
    print()
    print("Dataset building complete.")