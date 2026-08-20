from pathlib import Path
import time

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score


# ==========================================================
# SignSync - Experiment 001
# Task 3: Random Forest Hyperparameter Study
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = PROJECT_ROOT / "generated" / "landmarks.csv"

OUTPUT_PATH = (
    PROJECT_ROOT
    / "experiments"
    / "experiment_001"
    / "rf_hyperparameter_report.csv"
)


print("=" * 60)
print("SignSync Random Forest Hyperparameter Study")
print("=" * 60)

# ----------------------------------------------------------
# Load dataset
# ----------------------------------------------------------

df = pd.read_csv(DATASET_PATH)

print(f"\nSamples : {len(df)}")
print(f"Columns : {len(df.columns)}")

X = df.drop(columns=["label"])
y = df["label"]

# ----------------------------------------------------------
# SAME train/test split for every experiment
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
# Tree configurations
# ----------------------------------------------------------

tree_counts = [50, 100, 200]

results = []

# ----------------------------------------------------------
# Train models
# ----------------------------------------------------------

for n_trees in tree_counts:

    print("\n" + "-" * 50)
    print(f"Random Forest: {n_trees} Trees")
    print("-" * 50)

    model = RandomForestClassifier(
        n_estimators=n_trees,
        random_state=42,
        n_jobs=-1
    )

    start_time = time.perf_counter()

    model.fit(X_train, y_train)

    training_time = time.perf_counter() - start_time

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    print(f"Training Time : {training_time:.4f} seconds")
    print(f"Accuracy      : {accuracy:.4f}")
    print(f"F1 Score      : {f1:.4f}")

    results.append({
        "Trees": n_trees,
        "Training Time": round(training_time, 4),
        "Accuracy": round(accuracy, 4),
        "F1 Score": round(f1, 4)
    })


# ----------------------------------------------------------
# Save results
# ----------------------------------------------------------

results_df = pd.DataFrame(results)

results_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\n" + "=" * 60)
print("Hyperparameter study complete.")
print("=" * 60)

print("\nResults:")
print(results_df.to_string(index=False))

print("\nSaved to:")
print(OUTPUT_PATH)