import cv2
import time

from app.ai.hand_tracking.hand_detector import HandDetector
from app.ai.gesture_recognition.landmark_converter import LandmarkConverter
from app.ai.ml.inference.predictor import Predictor
from app.ai.temporal.temporal_buffer import TemporalBuffer
from app.ai.temporal.stable_detector import StableGestureDetector
from app.ai.utils.fps_counter import FPSCounter


class WebcamPipelineTest:


    def __init__(self):

        print("Initializing SignSync Real-Time Pipeline...")


        self.hand_detector = HandDetector(
            max_num_hands=1
        )


        self.converter = LandmarkConverter()


        self.predictor = Predictor()


        self.buffer = TemporalBuffer(
            max_frames=30
        )


        self.stable_detector = StableGestureDetector(
            required_stable_frames=5,
            confidence_threshold=0.60
        )


        self.fps = FPSCounter()


        print("Pipeline Ready")



    def run(self):

        camera = cv2.VideoCapture(0)


        if not camera.isOpened():

            print("Camera not detected")

            return



        print("\nStarting Webcam Test")
        print("Press Q to exit\n")



        while True:


            start_time = time.perf_counter()



            success, frame = camera.read()


            if not success:

                continue



            self.fps.update()



            # ----------------------------------
            # Hand Detection
            # ----------------------------------

            detection = self.hand_detector.detect(
                frame
            )



            prediction = None
            confidence = 0



            # ----------------------------------
            # Validate Hand
            # ----------------------------------

            if detection["hand_count"] == 1:



                landmarks = detection["landmarks"][0]



                # Store temporal data

                self.buffer.add_frame(
                    landmarks
                )



                # ----------------------------------
                # Prediction
                # ----------------------------------

                result = self.predictor.predict(
                    landmarks
                )



                prediction = result["prediction"]

                confidence = result["confidence"]



                # ----------------------------------
                # Stability Check
                # ----------------------------------

                stable = self.stable_detector.update(
                    prediction,
                    confidence
                )



                display_prediction = (
                    stable["prediction"]
                    if stable["stable"]
                    else "Waiting..."
                )



                cv2.putText(
                    frame,
                    f"Gesture: {display_prediction}",
                    (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2
                )


                cv2.putText(
                    frame,
                    f"Confidence: {confidence:.2f}",
                    (20,80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255,255,255),
                    2
                )


                cv2.putText(
                    frame,
                    f"Stable Frames: {stable['stable_frames']}",
                    (20,120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255,255,255),
                    2
                )



            else:


                cv2.putText(
                    frame,
                    "No Hand / Invalid Input",
                    (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,0,255),
                    2
                )



            # ----------------------------------
            # Performance
            # ----------------------------------

            latency = (
                time.perf_counter()
                -
                start_time
            ) * 1000



            cv2.putText(
                frame,
                f"FPS: {self.fps.get_fps():.2f}",
                (20,170),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,255),
                2
            )


            cv2.putText(
                frame,
                f"Latency: {latency:.2f} ms",
                (20,210),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,255),
                2
            )



            cv2.imshow(
                "SignSync Real-Time Pipeline Test",
                frame
            )



            key = cv2.waitKey(1)


            if key == ord('q'):

                break



        camera.release()

        cv2.destroyAllWindows()





if __name__ == "__main__":


    pipeline = WebcamPipelineTest()

    pipeline.run()