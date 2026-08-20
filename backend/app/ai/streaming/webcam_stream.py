import cv2
import time


class WebcamStream:
    """
    SignSync Webcam Stream

    Responsible for:
    - Continuous webcam capture
    - Frame delivery
    - Camera release
    """


    def __init__(
        self,
        camera_id=0,
        width=640,
        height=480
    ):

        self.camera_id = camera_id

        self.camera = cv2.VideoCapture(
            camera_id
        )

        if not self.camera.isOpened():
            raise RuntimeError(
                "Unable to open webcam."
            )


        self.camera.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            width
        )

        self.camera.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            height
        )


        self.running = False



    # ==========================================
    # Start Camera
    # ==========================================

    def start(self):

        self.running = True



    # ==========================================
    # Read Frame
    # ==========================================

    def read(self):

        if not self.running:
            self.start()


        success, frame = self.camera.read()


        if not success:

            return None


        return frame



    # ==========================================
    # Generator Stream
    # ==========================================

    def stream(self):

        self.start()


        while self.running:


            frame = self.read()


            if frame is None:
                continue


            yield frame



    # ==========================================
    # Stop Camera
    # ==========================================

    def stop(self):

        self.running = False


        if self.camera:

            self.camera.release()



    # ==========================================
    # Context Manager Support
    # ==========================================

    def __enter__(self):

        self.start()

        return self



    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):

        self.stop()