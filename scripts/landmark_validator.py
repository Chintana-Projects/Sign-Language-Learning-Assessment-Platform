from pathlib import Path
import json
import cv2
import mediapipe as mp


# ==========================================================
# SignSync - Landmark Validation
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = (
    PROJECT_ROOT
    / "datasets"
    / "merged_dataset"
)

GENERATED_DIR = (
    PROJECT_ROOT
    / "generated"
)

REPORT_PATH = (
    GENERATED_DIR
    / "dataset_report.json"
)

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp"
}


def validate_landmarks():

    GENERATED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # ------------------------------------------------------
    # Validate dataset
    # ------------------------------------------------------

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset folder not found:\n{DATASET_PATH}"
        )

    class_folders = sorted(
        [
            folder
            for folder in DATASET_PATH.iterdir()
            if folder.is_dir()
        ]
    )

    if not class_folders:
        raise RuntimeError(
            "No gesture class folders found in merged_dataset."
        )

    total_images = 0
    successful_detections = 0
    no_hand_detected = 0
    corrupted_images = 0

    mp_hands = mp.solutions.hands

    hands = mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=1,
        min_detection_confidence=0.5
    )

    try:

        for class_folder in class_folders:

            for image_path in sorted(class_folder.glob("*")):

                if not image_path.is_file():
                    continue

                if (
                    image_path.suffix.lower()
                    not in IMAGE_EXTENSIONS
                ):
                    continue

                total_images += 1

                image = cv2.imread(
                    str(image_path)
                )

                # --------------------------------------
                # Corrupted / unreadable image
                # --------------------------------------

                if image is None:

                    corrupted_images += 1
                    continue

                # --------------------------------------
                # Convert to RGB
                # --------------------------------------

                rgb = cv2.cvtColor(
                    image,
                    cv2.COLOR_BGR2RGB
                )

                # --------------------------------------
                # MediaPipe Detection
                # --------------------------------------

                results = hands.process(rgb)

                # --------------------------------------
                # No hand detected
                # --------------------------------------

                if not results.multi_hand_landmarks:

                    no_hand_detected += 1
                    continue

                # --------------------------------------
                # Validate landmark count
                # --------------------------------------

                landmarks = results.multi_hand_landmarks[0]

                if len(landmarks.landmark) == 21:

                    successful_detections += 1

                else:

                    no_hand_detected += 1

    finally:

        hands.close()

    # ------------------------------------------------------
    # Calculate success percentage
    # ------------------------------------------------------

    success_percentage = (
        (successful_detections / total_images) * 100
        if total_images > 0
        else 0
    )

    # ------------------------------------------------------
    # Create report
    # ------------------------------------------------------

    report = {

        "dataset_path": str(DATASET_PATH),

        "number_of_classes": len(class_folders),

        "total_images_processed": total_images,

        "successful_landmark_detections":
            successful_detections,

        "no_hand_detected":
            no_hand_detected,

        "corrupted_or_unreadable_images":
            corrupted_images,

        "success_percentage":
            round(success_percentage, 2)

    }

    with open(
        REPORT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4
        )

    return report


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("        SignSync Landmark Validation")
    print("=" * 60)

    report = validate_landmarks()

    print()
    print(f"Dataset Path           : {report['dataset_path']}")
    print(f"Gesture Classes        : {report['number_of_classes']}")
    print(f"Total Images           : {report['total_images_processed']}")
    print(f"Successful Detections  : {report['successful_landmark_detections']}")
    print(f"No Hand Detected       : {report['no_hand_detected']}")
    print(f"Corrupted Images       : {report['corrupted_or_unreadable_images']}")
    print(f"Success Percentage     : {report['success_percentage']}%")

    print()
    print(f"Report saved to:\n{REPORT_PATH}")

    print("\nValidation Complete.")