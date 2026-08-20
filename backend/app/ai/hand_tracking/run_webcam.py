import cv2
from webcam import Webcam


def main():

    webcam = Webcam()

    if not webcam.open():
        return

    print("Press 'Q' to quit.")

    while True:

        success, frame = webcam.read()

        if not success:
            print("Failed to capture frame.")
            break

        cv2.imshow("SignSync Webcam", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    webcam.release()


if __name__ == "__main__":
    main()