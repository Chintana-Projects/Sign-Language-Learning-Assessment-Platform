from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


# ==========================================================
# SignSync - Stratified Dataset Split
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_CSV = (
    PROJECT_ROOT
    / "generated"
    / "asl_landmarks_normalized.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "generated"

TRAIN_CSV = OUTPUT_DIR / "train.csv"
VALIDATION_CSV = OUTPUT_DIR / "validation.csv"
TEST_CSV = OUTPUT_DIR / "test.csv"


# ==========================================================
# Configuration
# ==========================================================

TEST_SIZE = 0.15
VALIDATION_SIZE = 0.15
RANDOM_STATE = 42


# ==========================================================
# Check input
# ==========================================================

if not INPUT_CSV.exists():
    raise FileNotFoundError(
        f"Normalized dataset not found:\n{INPUT_CSV}"
    )


# ==========================================================
# Load dataset
# ==========================================================

print("=" * 60)
print("       SignSync Stratified Dataset Split")
print("=" * 60)

print("\nLoading dataset...")
print(INPUT_CSV)

df = pd.read_csv(INPUT_CSV)

print(f"\nTotal samples: {len(df)}")
print(f"Total columns: {len(df.columns)}")

if "label" not in df.columns:
    raise ValueError(
        "Dataset must contain a 'label' column."
    )


# ==========================================================
# Check classes
# ==========================================================

print(
    f"Number of classes: "
    f"{df['label'].nunique()}"
)

print("\nOriginal class distribution:")

print(
    df["label"]
    .value_counts()
    .sort_index()
)


# ==========================================================
# First split
#
# 70% Training
# 15% Validation
# 15% Test
# ==========================================================

# ==========================================================
# Stratified split
#
# Classes with enough samples are split normally.
# Extremely small classes cannot be stratified into all
# three datasets, so they are handled separately.
# ==========================================================

MIN_SAMPLES_FOR_STRATIFICATION = 4

normal_df = df[
    df["label"].map(df["label"].value_counts())
    >= MIN_SAMPLES_FOR_STRATIFICATION
].copy()

small_df = df[
    df["label"].map(df["label"].value_counts())
    < MIN_SAMPLES_FOR_STRATIFICATION
].copy()

print(
    f"\nNormal samples for stratified split: "
    f"{len(normal_df)}"
)

print(
    f"Small-class samples handled separately: "
    f"{len(small_df)}"
)

# ----------------------------------------------------------
# 70% train, 15% validation, 15% test
# ----------------------------------------------------------

train_df, temp_df = train_test_split(
    normal_df,
    test_size=TEST_SIZE + VALIDATION_SIZE,
    stratify=normal_df["label"],
    random_state=RANDOM_STATE
)

relative_test_size = (
    TEST_SIZE
    / (TEST_SIZE + VALIDATION_SIZE)
)

validation_df, test_df = train_test_split(
    temp_df,
    test_size=relative_test_size,
    stratify=temp_df["label"],
    random_state=RANDOM_STATE
)

# ----------------------------------------------------------
# Handle extremely small classes
# ----------------------------------------------------------

if len(small_df) > 0:

    print("\nSmall classes:")
    print(small_df["label"].value_counts())

    # These samples cannot be meaningfully represented
    # in all three splits. Keep them in training data so
    # no original sample is discarded.
    train_df = pd.concat(
        [train_df, small_df],
        ignore_index=True
    )

# ==========================================================
# Split temporary set into validation + test
# ==========================================================

relative_test_size = (
    TEST_SIZE
    / (TEST_SIZE + VALIDATION_SIZE)
)

validation_df, test_df = train_test_split(
    temp_df,
    test_size=relative_test_size,
    stratify=temp_df["label"],
    random_state=RANDOM_STATE
)


# ==========================================================
# Shuffle each final dataset
# ==========================================================

train_df = train_df.sample(
    frac=1,
    random_state=RANDOM_STATE
).reset_index(drop=True)

validation_df = validation_df.sample(
    frac=1,
    random_state=RANDOM_STATE
).reset_index(drop=True)

test_df = test_df.sample(
    frac=1,
    random_state=RANDOM_STATE
).reset_index(drop=True)


# ==========================================================
# Save
# ==========================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

train_df.to_csv(
    TRAIN_CSV,
    index=False
)

validation_df.to_csv(
    VALIDATION_CSV,
    index=False
)

test_df.to_csv(
    TEST_CSV,
    index=False
)


# ==========================================================
# Verification
# ==========================================================

print("\n" + "=" * 60)
print("Dataset Split Results")
print("=" * 60)

print(
    f"\nTraining samples   : {len(train_df)}"
)

print(
    f"Validation samples : {len(validation_df)}"
)

print(
    f"Test samples       : {len(test_df)}"
)

print(
    f"Total               : "
    f"{len(train_df) + len(validation_df) + len(test_df)}"
)


# ==========================================================
# Class distribution verification
# ==========================================================

print("\n" + "=" * 60)
print("Class Distribution Verification")
print("=" * 60)

distribution = pd.DataFrame({
    "Total": df["label"].value_counts(),
    "Train": train_df["label"].value_counts(),
    "Validation": validation_df["label"].value_counts(),
    "Test": test_df["label"].value_counts()
}).fillna(0).astype(int)

print("\n")
print(distribution.sort_index())


# ==========================================================
# Verify every class exists in every split
# ==========================================================

classes = set(df["label"])

train_classes = set(train_df["label"])
validation_classes = set(validation_df["label"])
test_classes = set(test_df["label"])


if (
    classes == train_classes
    and classes == validation_classes
    and classes == test_classes
):

    print(
        "\nSUCCESS: Every gesture class "
        "is represented in all three splits."
    )

else:

    print(
        "\nWARNING: Some classes are missing "
        "from one or more splits."
    )


print("\nFiles created:")

print(f"Train      : {TRAIN_CSV}")
print(f"Validation : {VALIDATION_CSV}")
print(f"Test       : {TEST_CSV}")

print("\nDataset splitting complete.")