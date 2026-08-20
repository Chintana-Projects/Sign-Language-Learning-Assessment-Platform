from pathlib import Path
import time

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


# ==========================================================
# SignSync - Experiment 001
# Task 2: Classifier Comparison
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = PROJECT_ROOT / "generated" / "landmarks.csv"

OUTPUT_PATH = (
    PROJECT_ROOT
    / "experiments"
    / "experiment_001"
    / "comparison_report.csv"
)


print("=" * 60)
print("SignSync Classifier Comparison")
print("=" * 60)

# ----------------------------------------------------------
# Load dataset
# ----------------------------------------------------------

print("\nLoading dataset...")

df = pd.read_csv(DATASET_PATH)

print(f"Samples : {len(df)}")
print(f"Columns : {len(df.columns)}")

# ----------------------------------------------------------
# Separate features and labels
# ----------------------------------------------------------

X = df.drop(columns=["label"])
y = df["label"]

# ----------------------------------------------------------
# Same train/test split for every model
# ----------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"Training samples : {len(X_train)}")
print(f"Testing samples  : {len(X_test)}")

# ----------------------------------------------------------
# Models
# ----------------------------------------------------------

models = {

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    ),

    "Decision Tree": DecisionTreeClassifier(
        random_state=42
    ),

    "Support Vector Machine": SVC(
        kernel="rbf",
        random_state=42
    )
}

results = []

# ----------------------------------------------------------
# Train and evaluate
# ----------------------------------------------------------

for name, model in models.items():

    print("\n" + "-" * 50)
    print(f"Training: {name}")
    print("-" * 50)

    start_time = time.perf_counter()

    model.fit(X_train, y_train)

    training_time = time.perf_counter() - start_time

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    print(f"Training Time : {training_time:.4f} seconds")
    print(f"Accuracy      : {accuracy:.4f}")
    print(f"Precision     : {precision:.4f}")
    print(f"Recall        : {recall:.4f}")
    print(f"F1 Score      : {f1:.4f}")

    results.append({
        "Algorithm": name,
        "Training Time": round(training_time, 4),
        "Accuracy": round(accuracy, 4),
        "Precision": round(precision, 4),
        "Recall": round(recall, 4),
        "F1 Score": round(f1, 4)
    })

# ----------------------------------------------------------
# Save comparison report
# ----------------------------------------------------------

results_df = pd.DataFrame(results)

results_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\n" + "=" * 60)
print("Comparison complete.")
print("=" * 60)

print("\nReport:")
print(results_df.to_string(index=False))

print("\nSaved to:")
print(OUTPUT_PATH)