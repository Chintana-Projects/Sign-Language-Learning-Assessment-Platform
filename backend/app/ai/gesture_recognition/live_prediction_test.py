import cv2

from app.ai.hand_tracking.hand_detector import HandDetector
from app.ai.hand_tracking.webcam import Webcam
from app.ai.gesture_recognition.landmark_converter import LandmarkConverter
from app.ai.ml.inference.predictor import Predictor


def main():

    detector = HandDetector(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    webcam = Webcam()
    predictor = Predictor()

    if not webcam.open():
        return

    print("======================================")
    print("SignSync Live Prediction Test")
    print("Show your hand to the camera.")
    print("Press Q to quit.")
    print("======================================")

    while True:

        success, frame = webcam.read()

        if not success:
            print("Failed to read webcam frame.")
            break

        frame, hand_count, landmark_data = detector.detect(frame)

        # --------------------------------------------------
        # No hand detected
        # --------------------------------------------------

        if hand_count == 0:

            cv2.putText(
                frame,
                "No hand detected",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

        # --------------------------------------------------
        # Hand detected
        # --------------------------------------------------

        else:

            # Use first detected hand
            hand_landmarks = landmark_data[0]

            try:

                # Convert MediaPipe output
                landmarks = LandmarkConverter.to_model_format(
                    hand_landmarks
                )

                # Predict
                result = predictor.predict(landmarks)

                prediction = result["prediction"]
                confidence = result["confidence"]

                text = (
                    f"Prediction: {prediction} "
                    f"| Confidence: {confidence:.2f}"
                )

                cv2.putText(
                    frame,
                    text,
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

                print(
                    f"Prediction: {prediction} | "
                    f"Confidence: {confidence:.2f}"
                )

            except Exception as e:

                print("Prediction error:", e)

                cv2.putText(
                    frame,
                    "Prediction error",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

        cv2.imshow(
            "SignSync - Live Prediction Test",
            frame
        )

        # Press Q to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    webcam.release()


if __name__ == "__main__":
    main()