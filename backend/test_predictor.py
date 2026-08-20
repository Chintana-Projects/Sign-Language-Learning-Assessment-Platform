import csv

from app.ai.ml.inference.predictor import Predictor


# ==========================================================
# SignSync - Predictor Test
# ==========================================================

CSV_PATH = "../generated/asl_landmarks.csv"


print("=" * 60)
print("        SignSync Predictor Test")
print("=" * 60)


# ----------------------------------------------------------
# Load predictor
# ----------------------------------------------------------

predictor = Predictor()

print("\nPredictor loaded successfully.")


# ----------------------------------------------------------
# Read first sample from CSV
# ----------------------------------------------------------

with open(
    CSV_PATH,
    "r",
    newline="",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)

    row = next(reader)


# ----------------------------------------------------------
# Extract 21 landmarks
# ----------------------------------------------------------

landmarks = []

for i in range(21):

    landmarks.append([
        float(row[f"x{i}"]),
        float(row[f"y{i}"]),
        float(row[f"z{i}"])
    ])


# ----------------------------------------------------------
# Actual label
# ----------------------------------------------------------

actual_label = row["label"]


# ----------------------------------------------------------
# Predict
# ----------------------------------------------------------

result = predictor.predict(landmarks)


# ----------------------------------------------------------
# Display result
# ----------------------------------------------------------

print("\nActual label     :", actual_label)
print("Predicted label  :", result["prediction"])
print("Confidence       :", result["confidence"])
print("Processing time  :", result["processing_time"])

print("\n" + "=" * 60)