import cv2
import requests

from app.ai.hand_tracking.hand_detector import HandDetector
from app.ai.gesture_recognition.landmark_converter import LandmarkConverter


API_URL = "http://127.0.0.1:8000"


def main():

    # --------------------------------------------------
    # Start practice session
    # --------------------------------------------------

    start_response = requests.post(
        f"{API_URL}/practice/start/1"
    )

    if start_response.status_code != 200:
        print("Failed to start practice session.")
        print(start_response.text)
        return

    start_data = start_response.json()

    session_id = start_data["session"]["session_id"]

    print("======================================")
    print("SignSync API Live Prediction Test")
    print("======================================")
    print(f"Session ID: {session_id}")
    print("Show your hand to the camera.")
    print("Press Q to quit.")
    print("======================================")

    # --------------------------------------------------
    # MediaPipe hand detector
    # --------------------------------------------------

    detector = HandDetector(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Unable to open webcam.")
        return

    frame_counter = 0

    try:

        while True:

            success, frame = cap.read()

            if not success:
                print("Failed to read webcam frame.")
                break

            frame, hand_count, landmark_data = detector.detect(frame)

            # --------------------------------------------------
            # No hand
            # --------------------------------------------------

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

            # --------------------------------------------------
            # Hand detected
            # --------------------------------------------------

            else:

                hand_landmarks = landmark_data[0]

                try:

                    landmarks = LandmarkConverter.to_model_format(
                        hand_landmarks
                    )

                    # Send every 5th frame to reduce API requests
                    frame_counter += 1

                    if frame_counter % 5 == 0:

                        response = requests.post(
                            f"{API_URL}/practice/{session_id}/attempt",
                            json={
                                "landmarks": landmarks
                            },
                            timeout=5
                        )

                        if response.status_code == 200:

                            data = response.json()

                            assessment = data["assessment"]

                            prediction = assessment["prediction"]
                            confidence = assessment["confidence"]

                            print(
                                f"API Prediction: {prediction} | "
                                f"Confidence: {confidence:.2f}"
                            )

                            text = (
                                f"{prediction} "
                                f"| Confidence: {confidence:.2f}"
                            )

                            cv2.putText(
                                frame,
                                text,
                                (20, 40),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.9,
                                (0, 255, 0),
                                2
                            )

                        else:

                            print(
                                "API error:",
                                response.status_code,
                                response.text
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
                "SignSync - API Live Prediction",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:

        cap.release()
        cv2.destroyAllWindows()

        # --------------------------------------------------
        # End practice session
        # --------------------------------------------------

        try:

            end_response = requests.post(
                f"{API_URL}/practice/{session_id}/end"
            )

            if end_response.status_code == 200:
                print("Practice session ended.")
            else:
                print(
                    "Failed to end session:",
                    end_response.text
                )

        except Exception as e:

            print("Could not end session:", e)


if __name__ == "__main__":
    main()