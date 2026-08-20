import cv2
import requests

from app.ai.hand_tracking.hand_detector import HandDetector
from app.ai.hand_tracking.webcam import Webcam
from app.ai.gesture_recognition.landmark_converter import LandmarkConverter


API_URL = "http://127.0.0.1:8000"

# ---------------------------------------------------------
# Start a practice session
# ---------------------------------------------------------

response = requests.post(
    f"{API_URL}/practice/start/1"
)

response.raise_for_status()

session_data = response.json()

session_id = session_data["session"]["session_id"]

print("======================================")
print("SignSync API Live Prediction Test")
print("======================================")
print(f"Session ID: {session_id}")
print("Show your hand to the camera.")
print("Press Q to quit.")
print("======================================")


# ---------------------------------------------------------
# MediaPipe
# ---------------------------------------------------------

detector = HandDetector(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

webcam = Webcam()

if not webcam.open():
    print("Unable to open webcam.")
    raise SystemExit


# ---------------------------------------------------------
# Main loop
# ---------------------------------------------------------

try:

    while True:

        success, frame = webcam.read()

        if not success:
            print("Failed to read webcam frame.")
            break

        frame, hand_count, landmark_data = detector.detect(frame)

        # -------------------------------------------------
        # No hand
        # -------------------------------------------------

        if hand_count == 0:

            cv2.putText(
                frame,
                "No hand detected",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

        # -------------------------------------------------
        # Hand detected
        # -------------------------------------------------

        else:

            try:

                # Get first hand
                hand_landmarks = landmark_data[0]

                # Convert MediaPipe dictionaries
                # into [x, y, z] format
                landmarks = (
                    LandmarkConverter.to_model_format(
                        hand_landmarks
                    )
                )

                # -------------------------------------------------
                # Send REAL MediaPipe landmarks to FastAPI
                # -------------------------------------------------

                api_response = requests.post(
                    f"{API_URL}/practice/{session_id}/attempt",
                    json={
                        "landmarks": landmarks
                    },
                    timeout=5
                )

                api_response.raise_for_status()

                result = api_response.json()

                assessment = result["assessment"]

                prediction = assessment["prediction"]
                confidence = assessment["confidence"]

                # -------------------------------------------------
                # Display prediction
                # -------------------------------------------------

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

                print("API prediction error:", e)

                cv2.putText(
                    frame,
                    "API prediction error",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

        cv2.imshow(
            "SignSync - API Live Prediction",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:

    # ---------------------------------------------------------
    # End practice session
    # ---------------------------------------------------------

    try:

        end_response = requests.post(
            f"{API_URL}/practice/{session_id}/end",
            timeout=5
        )

        if end_response.ok:

            print("\nPractice session ended.")

            print(
                end_response.json()
            )

    except Exception as e:

        print(
            "Could not end practice session:",
            e
        )

    webcam.release()