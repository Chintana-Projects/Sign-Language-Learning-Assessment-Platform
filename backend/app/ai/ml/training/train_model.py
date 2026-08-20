from pathlib import Path
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# ==========================================================
# SignSync - Random Forest Training
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[5]
BACKEND_ROOT = PROJECT_ROOT / "backend"

DATASET_PATH = PROJECT_ROOT / "generated" / "asl_landmarks_normalized.csv"

MODEL_DIR = BACKEND_ROOT / "app" / "ai" / "ml" / "models"
MODEL_PATH = MODEL_DIR / "random_forest.pkl"
LABEL_PATH = MODEL_DIR / "label_names.pkl"

MODEL_DIR.mkdir(parents=True, exist_ok=True)


print("=" * 60)
print("        SignSync Random Forest Training")
print("=" * 60)

print("\nLoading dataset...")
print(DATASET_PATH)


# ----------------------------------------------------------
# Load dataset
# ----------------------------------------------------------

if not DATASET_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found:\n{DATASET_PATH}"
    )

df = pd.read_csv(DATASET_PATH)

print(f"\nTotal samples : {len(df)}")
print(f"Total columns : {len(df.columns)}")


# ----------------------------------------------------------
# Separate features and labels
# ----------------------------------------------------------

X = df.drop(columns=["label"])
y = df["label"]

print(f"Features      : {X.shape[1]}")
print(f"Classes       : {y.nunique()}")

print("\nClasses:")
print(sorted(y.unique()))


# ----------------------------------------------------------
# Train / test split
# ----------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples :", len(X_train))
print("Testing samples  :", len(X_test))


# ----------------------------------------------------------
# Create Random Forest
# ----------------------------------------------------------

print("\nTraining Random Forest...")

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

model.fit(X_train, y_train)


# ----------------------------------------------------------
# Evaluate
# ----------------------------------------------------------

print("\nEvaluating model...")

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\n" + "=" * 60)
print("              MODEL RESULTS")
print("=" * 60)

print(f"\nAccuracy : {accuracy:.4f}")

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)


# ----------------------------------------------------------
# Save model
# ----------------------------------------------------------

joblib.dump(model, MODEL_PATH)

label_names = sorted(y.unique())

joblib.dump(label_names, LABEL_PATH)


print("=" * 60)
print("Model training complete.")
print("=" * 60)

print("\nModel saved to:")
print(MODEL_PATH)

print("\nLabels saved to:")
print(LABEL_PATH)