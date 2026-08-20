import json
import time
from pathlib import Path

import cv2

from app.ai.hand_tracking.hand_detector import HandDetector
from app.ai.gesture_recognition.landmark_converter import LandmarkConverter
from app.ai.ml.inference.predictor import Predictor


# ======================================================
# Paths
# ======================================================

BACKEND_ROOT = Path(__file__).resolve().parents[4]


TEST_DATASET = (
    BACKEND_ROOT.parent
    /
    "datasets"
    /
    "asl_alphabet_test"
)


REPORT_PATH = (
    BACKEND_ROOT.parent
    /
    "alphabet_test_report.json"
)


# ======================================================
# Alphabet Test
# ======================================================

def main():

    print("\nStarting Alphabet Test...\n")


    detector = HandDetector()

    predictor = Predictor()


    results = []

    correct_count = 0

    total_count = 0

    confidence_scores = []



    for image_path in sorted(TEST_DATASET.glob("*_test.jpg")):


        expected = (
            image_path.stem
            .replace("_test", "")
            .upper()
        )


        print(
            f"Testing {expected}..."
        )


        image = cv2.imread(
            str(image_path)
        )


        if image is None:

            print(
                "Image loading failed"
            )

            continue



        # ---------------------------------
        # MediaPipe Detection
        # ---------------------------------

        frame, hand_count, landmark_data = (
            detector.detect(image)
        )



        if hand_count == 0:


            predicted = "NOTHING"

            confidence = 0


        else:


            hand_landmarks = (
                landmark_data[0]
            )


            landmarks = (
                LandmarkConverter
                .to_model_format(
                    hand_landmarks
                )
            )


            output = (
                predictor.predict(
                    landmarks
                )
            )


            predicted = (
                output["prediction"]
            )


            confidence = (
                output["confidence"]
            )



        if confidence > 1:

            confidence /= 100



        confidence_scores.append(
            confidence
        )



        correct = (
            expected.upper()
            ==
            predicted.upper()
        )


        if correct:

            correct_count += 1



        total_count += 1



        results.append({

            "expected":
                expected,


            "predicted":
                predicted,


            "correct":
                correct,


            "confidence":
                round(
                    confidence * 100,
                    2
                )

        })



    # ==================================================
    # Final Report
    # ==================================================

    accuracy = (

        correct_count / total_count * 100

        if total_count > 0

        else 0

    )


    avg_confidence = (

        sum(confidence_scores)
        /
        len(confidence_scores)
        *
        100

        if confidence_scores

        else 0

    )



    report = {


        "total_samples":
            total_count,


        "correct_predictions":
            correct_count,


        "accuracy":
            round(
                accuracy,
                2
            ),


        "average_confidence":
            round(
                avg_confidence,
                2
            ),


        "results":
            results

    }



    with open(
        REPORT_PATH,
        "w"
    ) as f:

        json.dump(
            report,
            f,
            indent=4
        )



    print("\n==============================")

    print(
        "Alphabet Test Completed"
    )

    print("==============================")

    print(
        f"Accuracy: {accuracy:.2f}%"
    )

    print(
        f"Average Confidence: {avg_confidence:.2f}%"
    )

    print(
        f"Report saved: {REPORT_PATH}"
    )



if __name__ == "__main__":

    main()