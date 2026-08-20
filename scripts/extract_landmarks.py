from pathlib import Path
import csv
import cv2
import mediapipe as mp

# ==========================================================
# SignSync - Landmark Extraction Utility
# Task 1 + Task 2
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = PROJECT_ROOT / "datasets" / "merged_dataset"
OUTPUT_DIR = PROJECT_ROOT / "generated"

OUTPUT_CSV = OUTPUT_DIR / "asl_landmarks.csv"
FAILED_LOG = OUTPUT_DIR / "failed_landmark_images.txt"

OUTPUT_DIR.mkdir(exist_ok=True)

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}

# ==========================================================
# MediaPipe Hands
# ==========================================================

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5
)

# ==========================================================
# CSV Header
# ==========================================================

header = []

for i in range(21):
    header.extend([
        f"x{i}",
        f"y{i}",
        f"z{i}"
    ])

header.append("label")

# ==========================================================
# Counters
# ==========================================================

total_images = 0
successful_extractions = 0
failed_detections = 0

failed_images = []

# ==========================================================
# Start Extraction
# ==========================================================

print("=" * 60)
print("        SignSync Landmark Extraction")
print("=" * 60)

with open(OUTPUT_CSV, "w", newline="") as csv_file:

    writer = csv.writer(csv_file)

    # Write CSV header
    writer.writerow(header)

    # ------------------------------------------------------
    # Process every class
    # ------------------------------------------------------

    for class_folder in sorted(DATASET_PATH.iterdir()):

        if not class_folder.is_dir():
            continue

        label = class_folder.name

        print(f"Processing {label}...")

        # --------------------------------------------------
        # Process every image
        # --------------------------------------------------

        for image_path in sorted(class_folder.iterdir()):

            if not image_path.is_file():
                continue

            if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
                continue

            total_images += 1

            # ------------------------------------------------
            # Read image
            # ------------------------------------------------

            image = cv2.imread(str(image_path))

            if image is None:

                failed_detections += 1

                failed_images.append(
                    f"{label}/{image_path.name} - Image could not be read"
                )

                continue

            # ------------------------------------------------
            # Convert BGR to RGB
            # ------------------------------------------------

            rgb = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2RGB
            )

            # ------------------------------------------------
            # Detect hand
            # ------------------------------------------------

            results = hands.process(rgb)

            # ------------------------------------------------
            # Handle failed detection
            # ------------------------------------------------

            if not results.multi_hand_landmarks:

                failed_detections += 1

                failed_images.append(
                    f"{label}/{image_path.name} - No hand detected"
                )

                continue

            # ------------------------------------------------
            # Extract first detected hand
            # ------------------------------------------------

            landmarks = results.multi_hand_landmarks[0]

            feature_vector = []

            for landmark in landmarks.landmark:

                feature_vector.extend([
                    landmark.x,
                    landmark.y,
                    landmark.z
                ])

            # ------------------------------------------------
            # Add class label
            # ------------------------------------------------

            feature_vector.append(label)

            # ------------------------------------------------
            # Save sample
            # ------------------------------------------------

            writer.writerow(feature_vector)

            successful_extractions += 1


# ==========================================================
# Close MediaPipe
# ==========================================================

hands.close()

# ==========================================================
# Save Failed Image Log
# ==========================================================

with open(FAILED_LOG, "w") as log_file:

    for failed_image in failed_images:
        log_file.write(failed_image + "\n")

# ==========================================================
# Final Summary
# ==========================================================

print()
print("=" * 60)
print("        Landmark Extraction Summary")
print("=" * 60)

print(f"Total Images Processed      : {total_images}")
print(f"Successful Extractions      : {successful_extractions}")
print(f"Failed Landmark Detections  : {failed_detections}")

print("=" * 60)

print()
print("CSV saved to:")
print(OUTPUT_CSV)

print()
print("Failed image log saved to:")
print(FAILED_LOG)

print()
print("Extraction Complete.")