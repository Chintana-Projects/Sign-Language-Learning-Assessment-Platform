from pathlib import Path
import time
import os
import joblib
import tracemalloc
import warnings
import pandas as pd
import numpy as np

warnings.filterwarnings(
    "ignore",
    message="`sklearn.utils.parallel.delayed` should be used"
)
# ==========================================================
# SignSync - Experiment 001
# Task 5: Inference Benchmark
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = PROJECT_ROOT / "generated" / "landmarks.csv"

MODEL_PATH = (
    PROJECT_ROOT
    / "backend"
    / "app"
    / "ai"
    / "ml"
    / "models"
    / "random_forest.pkl"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "experiments"
    / "experiment_001"
    / "benchmark_report.md"
)

NUM_PREDICTIONS = 100


print("=" * 60)
print("SignSync Inference Benchmark")
print("=" * 60)


# ----------------------------------------------------------
# Check model
# ----------------------------------------------------------

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model not found: {MODEL_PATH}"
    )


# ----------------------------------------------------------
# Model file size
# ----------------------------------------------------------

model_size_bytes = MODEL_PATH.stat().st_size

model_size_mb = (
    model_size_bytes / (1024 * 1024)
)

print(
    f"\nModel size: "
    f"{model_size_mb:.2f} MB"
)


# ----------------------------------------------------------
# Load model
# ----------------------------------------------------------

print("\nLoading model...")

model = joblib.load(MODEL_PATH)

print("Model loaded.")


# ----------------------------------------------------------
# Load dataset
# ----------------------------------------------------------

print("\nLoading test data...")

df = pd.read_csv(DATASET_PATH)

X = df.drop(columns=["label"])

# Make sure we have enough samples
if len(X) < NUM_PREDICTIONS:

    NUM_PREDICTIONS = len(X)


X_test = X[:NUM_PREDICTIONS]


print(
    f"Predictions to benchmark: "
    f"{NUM_PREDICTIONS}"
)


# ----------------------------------------------------------
# Warm-up
# ----------------------------------------------------------

print("\nWarming up model...")

for i in range(min(10, len(X_test))):

    model.predict(
        X_test[i].reshape(1, -1)
    )


# ----------------------------------------------------------
# Memory measurement
# ----------------------------------------------------------

tracemalloc.start()


# ----------------------------------------------------------
# Inference benchmark
# ----------------------------------------------------------

print("\nRunning benchmark...")

start_time = time.perf_counter()

for sample in X_test:

    model.predict(
        sample.reshape(1, -1)
    )

end_time = time.perf_counter()


current_memory, peak_memory = (
    tracemalloc.get_traced_memory()
)

tracemalloc.stop()


# ----------------------------------------------------------
# Metrics
# ----------------------------------------------------------

total_time = (
    end_time - start_time
)

average_time = (
    total_time
    / NUM_PREDICTIONS
)

average_time_ms = (
    average_time * 1000
)

throughput = (
    NUM_PREDICTIONS
    / total_time
)

peak_memory_mb = (
    peak_memory
    / (1024 * 1024)
)


# ----------------------------------------------------------
# Print results
# ----------------------------------------------------------

print("\n" + "=" * 60)
print("Benchmark Results")
print("=" * 60)

print(
    f"Total inference time : "
    f"{total_time:.4f} seconds"
)

print(
    f"Average inference   : "
    f"{average_time_ms:.4f} ms"
)

print(
    f"Throughput          : "
    f"{throughput:.2f} predictions/sec"
)

print(
    f"Peak memory         : "
    f"{peak_memory_mb:.2f} MB"
)

print(
    f"Model size          : "
    f"{model_size_mb:.2f} MB"
)


# ----------------------------------------------------------
# Determine real-time suitability
# ----------------------------------------------------------

if average_time_ms < 50:

    suitability = "YES"

    reason = (
        "The average inference time is below 50 ms, "
        "which provides sufficient speed for real-time "
        "webcam-based gesture recognition."
    )

elif average_time_ms < 100:

    suitability = "LIKELY"

    reason = (
        "The model is reasonably fast for real-time "
        "recognition, although additional camera and "
        "MediaPipe processing overhead should be considered."
    )

else:

    suitability = "NO"

    reason = (
        "The inference time is relatively high and may "
        "introduce noticeable latency in real-time recognition."
    )


# ----------------------------------------------------------
# Generate report
# ----------------------------------------------------------

with open(
    OUTPUT_PATH,
    "w",
    encoding="utf-8"
) as file:

    file.write("# SignSync Inference Benchmark\n\n")

    file.write("## Model\n\n")

    file.write(
        "`backend/app/ai/ml/models/random_forest.pkl`\n\n"
    )

    file.write("## Dataset\n\n")

    file.write(
        "`generated/landmarks.csv`\n\n"
    )

    file.write("## Benchmark Configuration\n\n")

    file.write(
        f"- Predictions measured: {NUM_PREDICTIONS}\n"
        "- Warm-up predictions: 10\n"
        "- Measurement: single-sample prediction\n\n"
    )

    file.write("## Results\n\n")

    file.write("| Metric | Result |\n")
    file.write("|---|---:|\n")

    file.write(
        f"| Average inference time | "
        f"{average_time_ms:.4f} ms |\n"
    )

    file.write(
        f"| Throughput | "
        f"{throughput:.2f} predictions/sec |\n"
    )

    file.write(
        f"| Peak memory | "
        f"{peak_memory_mb:.2f} MB |\n"
    )

    file.write(
        f"| Model file size | "
        f"{model_size_mb:.2f} MB |\n"
    )

    file.write("\n")

    file.write("## Real-Time Suitability\n\n")

    file.write(
        f"**Suitable for real-time recognition: "
        f"{suitability}**\n\n"
    )

    file.write(reason)

    file.write("\n\n")

    file.write("## Conclusion\n\n")

    file.write(
        "The benchmark measures model inference independently "
        "of webcam capture and MediaPipe landmark extraction. "
        "Therefore, the final end-to-end latency of SignSync "
        "will also depend on camera capture, MediaPipe processing, "
        "feature preparation, and frontend/backend communication.\n"
    )


print("\nReport saved to:")
print(OUTPUT_PATH)

print("\nBenchmark complete.")