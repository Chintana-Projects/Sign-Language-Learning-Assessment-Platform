import cv2


class Webcam:

    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None

    def open(self):
        self.cap = cv2.VideoCapture(self.camera_index)

        if not self.cap.isOpened():
            print("Error: Unable to open webcam.")
            return False

        return True

    def read(self):
        if self.cap is None:
            return False, None

        return self.cap.read()

    def release(self):
        if self.cap is not None:
            self.cap.release()

        cv2.destroyAllWindows()