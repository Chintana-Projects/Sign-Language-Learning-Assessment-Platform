from pathlib import Path

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score


# ==========================================================
# SignSync - Experiment 001
# Task 4: Error Analysis
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = PROJECT_ROOT / "generated" / "landmarks.csv"

OUTPUT_DIR = PROJECT_ROOT / "experiments" / "experiment_001"

MATRIX_PATH = OUTPUT_DIR / "confusion_matrix.csv"
REPORT_PATH = OUTPUT_DIR / "error_analysis.md"


print("=" * 60)
print("SignSync Gesture Error Analysis")
print("=" * 60)


# ----------------------------------------------------------
# Load dataset
# ----------------------------------------------------------

df = pd.read_csv(DATASET_PATH)

X = df.drop(columns=["label"])
y = df["label"]


# ----------------------------------------------------------
# Same split used in previous experiments
# ----------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ----------------------------------------------------------
# Train separate Random Forest
# ----------------------------------------------------------

print("\nTraining Random Forest...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)


# ----------------------------------------------------------
# Predictions
# ----------------------------------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(f"Accuracy: {accuracy:.4f}")


# ----------------------------------------------------------
# Confusion Matrix
# ----------------------------------------------------------

labels = sorted(y.unique())

cm = confusion_matrix(
    y_test,
    predictions,
    labels=labels
)

cm_df = pd.DataFrame(
    cm,
    index=labels,
    columns=labels
)

cm_df.to_csv(MATRIX_PATH)

print("\nConfusion matrix saved:")
print(MATRIX_PATH)


# ----------------------------------------------------------
# Find top 5 confused pairs
# ----------------------------------------------------------

confusions = []

for i in range(len(labels)):

    for j in range(len(labels)):

        if i == j:
            continue

        count = cm[i][j]

        if count > 0:

            confusions.append({
                "actual": labels[i],
                "predicted": labels[j],
                "count": int(count)
            })


confusions.sort(
    key=lambda x: x["count"],
    reverse=True
)

top5 = confusions[:5]


# ----------------------------------------------------------
# Generate Markdown report
# ----------------------------------------------------------

with open(
    REPORT_PATH,
    "w",
    encoding="utf-8"
) as file:

    file.write("# SignSync Error Analysis\n\n")

    file.write("## Model\n\n")
    file.write("Random Forest with 100 trees.\n\n")

    file.write("## Dataset\n\n")
    file.write("`generated/landmarks.csv`\n\n")

    file.write("## Test Accuracy\n\n")
    file.write(f"{accuracy:.4f}\n\n")

    file.write("## Top 5 Most Confused Gestures\n\n")

    file.write(
        "| Rank | Actual | Predicted | Errors |\n"
    )

    file.write(
        "|---:|---|---|---:|\n"
    )

    for rank, item in enumerate(top5, start=1):

        file.write(
            f"| {rank} | "
            f"{item['actual']} | "
            f"{item['predicted']} | "
            f"{item['count']} |\n"
        )

    file.write("\n")

    file.write("## Possible Causes\n\n")

    file.write(
        "The most common sources of gesture confusion may include:\n\n"
    )

    file.write(
        "- Similar finger positions between gestures.\n"
        "- Occlusion of fingers or parts of the hand.\n"
        "- Poor-quality or inconsistent training images.\n"
        "- Incorrect or ambiguous dataset labels.\n"
        "- Similar landmark configurations between different signs.\n"
        "- Variations in hand orientation or camera position.\n"
        "- Background and lighting conditions affecting landmark detection.\n\n"
    )

    file.write("## Recommendations\n\n")

    file.write(
        "The confused gesture pairs should be investigated individually. "
        "Additional training samples can be collected for visually similar "
        "gestures, particularly samples covering different hand orientations, "
        "distances, lighting conditions, and backgrounds.\n"
    )


print("\nTop 5 confused gestures:")

for rank, item in enumerate(top5, start=1):

    print(
        f"{rank}. "
        f"{item['actual']} -> "
        f"{item['predicted']} : "
        f"{item['count']} errors"
    )


print("\nReport saved:")
print(REPORT_PATH)

print("\nError analysis complete.")