import cv2
import time

from app.ai.hand_tracking.webcam import Webcam
from app.ai.hand_tracking.hand_detector import HandDetector
from app.ai.utils.json_saver import JSONSaver


def main():

    webcam = Webcam()

    if not webcam.open():
        return

    detector = HandDetector()
    saver = JSONSaver()

    previous_time = time.time()

    print("======================================")
    print("        SignSync Hand Tracking")
    print("======================================")
    print("Press S -> Save Landmark JSON")
    print("Press Q -> Quit")
    print("======================================")

    while True:

        success, frame = webcam.read()

        if not success:
            break

        frame, hand_count, landmark_data = detector.detect(frame)

        # ---------------- FPS ----------------

        current_time = time.time()

        fps = 1 / (current_time - previous_time)

        previous_time = current_time

        cv2.putText(
            frame,
            f"FPS : {int(fps)}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )

        # ------------ Hand Count ------------

        if hand_count > 0:

            cv2.putText(
                frame,
                f"Hands : {hand_count}",
                (10, 65),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 0, 0),
                2,
            )

            # Print landmarks

            for hand_index, hand in enumerate(landmark_data):

                print(f"\nHand {hand_index + 1}")

                for landmark_index, landmark in enumerate(hand):

                    print(
                        f"Landmark {landmark_index:2} : "
                        f"{landmark['x']:.5f} "
                        f"{landmark['y']:.5f} "
                        f"{landmark['z']:.5f}"
                    )

        else:

            cv2.putText(
                frame,
                "No Hand Detected",
                (10, 65),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2,
            )

        cv2.imshow("SignSync Hand Tracking", frame)

        key = cv2.waitKey(1) & 0xFF

        # Save JSON

        if key == ord("s"):

            if hand_count > 0:

                saver.save(landmark_data)

            else:

                print("\nNo hand detected. Nothing saved.")

        # Quit

        if key == ord("q"):
            break

    webcam.release()


if __name__ == "__main__":
    main()