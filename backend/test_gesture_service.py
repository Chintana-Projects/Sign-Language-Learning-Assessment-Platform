import cv2

from app.ai.hand_tracking.hand_detector import HandDetector
from app.services.gesture_service import GestureService
from app.ai.gesture_recognition.prediction_smoother import PredictionSmoother


print("=" * 60)
print("        SignSync Real Gesture Test")
print("=" * 60)


# ----------------------------------------------------------
# Initialize components
# ----------------------------------------------------------

detector = HandDetector(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

gesture_service = GestureService()

smoother = PredictionSmoother(
    window_size=15,
    confidence_threshold=0.40
)

camera = cv2.VideoCapture(0)


if not camera.isOpened():
    print("ERROR: Could not open webcam.")
    exit()


print("\nWebcam started.")
print("Show an ASL letter to the camera.")
print("Press Q to quit.")


# ----------------------------------------------------------
# Webcam loop
# ----------------------------------------------------------

while True:

    success, frame = camera.read()

    if not success:
        print("Failed to read webcam frame.")
        break


    # ------------------------------------------------------
    # Detect hand and extract landmarks
    # ------------------------------------------------------

    frame, hand_count, landmark_data = detector.detect(frame)


    # ------------------------------------------------------
    # Hand detected
    # ------------------------------------------------------

    if hand_count > 0:

        # First detected hand
        landmarks = landmark_data[0]


        # --------------------------------------------------
        # Convert landmark dictionary format
        #
        # From:
        # {"x": ..., "y": ..., "z": ...}
        #
        # To:
        # [[x,y,z], [x,y,z], ...]
        # --------------------------------------------------

        landmark_list = []

        for landmark in landmarks:

            landmark_list.append([
                landmark["x"],
                landmark["y"],
                landmark["z"]
            ])


        # --------------------------------------------------
        # Predict gesture
        # --------------------------------------------------

        try:

            result = gesture_service.predict(landmark_list)

            raw_prediction = result["prediction"]
            raw_confidence = result["confidence"]


            # ------------------------------------------------
            # Apply prediction smoothing
            # ------------------------------------------------

            stable_result = smoother.add_prediction(
                raw_prediction,
                raw_confidence
            )


            # ------------------------------------------------
            # Use stable prediction if available
            # ------------------------------------------------

            if stable_result is not None:

                prediction = stable_result["prediction"]
                confidence = stable_result["confidence"]

                votes = stable_result["votes"]
                window_size = stable_result["window_size"]

            else:

                prediction = "Uncertain"
                confidence = 0.0
                votes = 0
                window_size = 0


            # ------------------------------------------------
            # Console output
            # ------------------------------------------------

            print(
                f"Raw: {raw_prediction} ({raw_confidence:.3f}) | "
                f"Stable: {prediction} ({confidence:.3f}) | "
                f"Votes: {votes}/{window_size}"
            )


            # ------------------------------------------------
            # Display stable prediction
            # ------------------------------------------------

            cv2.putText(
                frame,
                f"Prediction: {prediction}",
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )


            # ------------------------------------------------
            # Display confidence
            # ------------------------------------------------

            cv2.putText(
                frame,
                f"Confidence: {confidence:.2f}",
                (10, 140),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )


            # ------------------------------------------------
            # Display smoothing votes
            # ------------------------------------------------

            cv2.putText(
                frame,
                f"Votes: {votes}/{window_size}",
                (10, 175),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )


        except Exception as error:

            print("Prediction error:", error)


    # ------------------------------------------------------
    # No hand detected
    # ------------------------------------------------------

    else:

        # Clear old prediction history
        smoother.reset()


        cv2.putText(
            frame,
            "No Hand Detected",
            (10, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )


    # ------------------------------------------------------
    # Display webcam
    # ------------------------------------------------------

    cv2.imshow(
        "SignSync Real Gesture Recognition",
        frame
    )


    # ------------------------------------------------------
    # Keyboard input
    # ------------------------------------------------------

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


# ----------------------------------------------------------
# Cleanup
# ----------------------------------------------------------

camera.release()

cv2.destroyAllWindows()


print("\nWebcam stopped.")
print("=" * 60)