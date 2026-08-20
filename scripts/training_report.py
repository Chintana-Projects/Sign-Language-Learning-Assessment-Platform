from pathlib import Path
import json
import pandas as pd


# ==========================================================
# SignSync - Training Dataset Report
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

GENERATED_DIR = PROJECT_ROOT / "generated"

LANDMARKS_CSV = GENERATED_DIR / "asl_landmarks_normalized.csv"
TRAIN_CSV = GENERATED_DIR / "train.csv"
VALIDATION_CSV = GENERATED_DIR / "validation.csv"
TEST_CSV = GENERATED_DIR / "test.csv"

REPORT_FILE = GENERATED_DIR / "training_report.json"


# ==========================================================
# Check files
# ==========================================================

required_files = [
    LANDMARKS_CSV,
    TRAIN_CSV,
    VALIDATION_CSV,
    TEST_CSV
]

for file in required_files:
    if not file.exists():
        raise FileNotFoundError(
            f"Required file not found:\n{file}"
        )


# ==========================================================
# Load datasets
# ==========================================================

print("=" * 60)
print("       SignSync Training Dataset Report")
print("=" * 60)

print("\nLoading datasets...")

full_df = pd.read_csv(LANDMARKS_CSV)
train_df = pd.read_csv(TRAIN_CSV)
validation_df = pd.read_csv(VALIDATION_CSV)
test_df = pd.read_csv(TEST_CSV)


# ==========================================================
# Identify features
# ==========================================================

if "label" not in full_df.columns:
    raise ValueError(
        "The dataset must contain a 'label' column."
    )

feature_columns = [
    column
    for column in full_df.columns
    if column != "label"
]

number_of_features = len(feature_columns)

number_of_classes = full_df["label"].nunique()

samples_per_class = (
    full_df["label"]
    .value_counts()
    .sort_index()
    .to_dict()
)


# ==========================================================
# Failed extraction count
# ==========================================================

failed_log = GENERATED_DIR / "failed_landmark_images.txt"

if failed_log.exists():

    with open(
        failed_log,
        "r",
        encoding="utf-8"
    ) as file:

        failed_extraction_count = sum(
            1 for line in file
            if line.strip()
        )

else:

    failed_extraction_count = 0


# ==========================================================
# Build report
# ==========================================================

report = {

    "total_samples": int(len(full_df)),

    "number_of_gesture_classes":
        int(number_of_classes),

    "samples_per_class":
        {
            str(label): int(count)
            for label, count
            in samples_per_class.items()
        },

    "number_of_features":
        int(number_of_features),

    "training_set_size":
        int(len(train_df)),

    "validation_set_size":
        int(len(validation_df)),

    "test_set_size":
        int(len(test_df)),

    "failed_landmark_extraction_count":
        int(failed_extraction_count)
}


# ==========================================================
# Save report
# ==========================================================

with open(
    REPORT_FILE,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        report,
        file,
        indent=4
    )


# ==========================================================
# Display summary
# ==========================================================

print("\n" + "=" * 60)
print("Training Dataset Summary")
print("=" * 60)

print(
    f"\nTotal samples       : "
    f"{report['total_samples']}"
)

print(
    f"Gesture classes     : "
    f"{report['number_of_gesture_classes']}"
)

print(
    f"Features            : "
    f"{report['number_of_features']}"
)

print(
    f"Training samples    : "
    f"{report['training_set_size']}"
)

print(
    f"Validation samples  : "
    f"{report['validation_set_size']}"
)

print(
    f"Test samples        : "
    f"{report['test_set_size']}"
)

print(
    f"Failed extractions  : "
    f"{report['failed_landmark_extraction_count']}"
)

print("\nReport saved to:")
print(REPORT_FILE)

print("\nTraining report generation complete.")