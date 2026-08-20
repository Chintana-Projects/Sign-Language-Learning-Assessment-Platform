import time


from app.ai.hand_tracking.hand_detector import HandDetector

from app.ai.gesture_recognition.landmark_converter import LandmarkConverter

from app.ai.ml.inference.predictor import Predictor

from app.ai.temporal.temporal_buffer import TemporalBuffer

from app.ai.temporal.stable_detector import StableGestureDetector

from app.ai.utils.fps_counter import FPSCounter

from app.ai.utils.frame_validator import FrameValidator





class GesturePipeline:
    """
    SignSync Real-Time Gesture Processing Pipeline


    Flow:

    Webcam Frame
          |
          ↓
    Hand Detection
          |
          ↓
    Frame Validation
          |
          ↓
    Landmark Conversion
          |
          ↓
    Temporal Buffer
          |
          ↓
    ML Prediction
          |
          ↓
    Stable Gesture Detection
          |
          ↓
    Response


    """



    def __init__(self):


        # Detection

        self.detector = HandDetector(
            max_num_hands=1
        )



        # Validation

        self.validator = FrameValidator(
            max_hands=1
        )



        # ML

        self.predictor = Predictor()



        # Temporal memory

        self.buffer = TemporalBuffer(
            max_frames=30
        )



        # Stability

        self.stable_detector = StableGestureDetector(
            required_stable_frames=5,
            confidence_threshold=0.60
        )



        # Performance

        self.fps_counter = FPSCounter()



    # ==================================================
    # Process One Frame
    # ==================================================

    def process_frame(self, frame):


        start_time = time.perf_counter()



        self.fps_counter.update()



        # ------------------------------------
        # Detect hand
        # ------------------------------------

        detection = self.detector.detect(
            frame
        )




        # ------------------------------------
        # Validate frame
        # ------------------------------------

        validation = self.validator.validate(
            detection
        )



        if not validation["valid"]:


            return {

                "prediction": None,

                "confidence":0,

                "stable":False,

                "message":
                validation["reason"],

                "fps":
                self.fps_counter.get_fps(),

                "latency":

                round(
                    time.perf_counter()
                    -
                    start_time,
                    4
                )

            }





        # ------------------------------------
        # Convert landmarks
        # ------------------------------------

        landmarks = detection["landmarks"][0]



        try:


            model_landmarks = LandmarkConverter.to_model_format(
                landmarks
            )


        except Exception as e:


            return {

                "prediction":None,

                "stable":False,

                "message":
                str(e)

            }





        # ------------------------------------
        # Temporal Buffer
        # ------------------------------------

        self.buffer.add_frame(
            model_landmarks
        )





        # ------------------------------------
        # Prediction
        # ------------------------------------

        result = self.predictor.predict(
            model_landmarks
        )



        prediction = result["prediction"]

        confidence = result["confidence"]






        # ------------------------------------
        # Stable Detection
        # ------------------------------------

        stable_result = self.stable_detector.update(

            prediction,

            confidence

        )





        latency = round(

            time.perf_counter()
            -
            start_time,

            4

        )





        return {


            "prediction":

            stable_result["prediction"],



            "raw_prediction":

            prediction,



            "confidence":

            confidence,



            "stable":

            stable_result["stable"],



            "stable_frames":

            stable_result["stable_frames"],



            "fps":

            self.fps_counter.get_fps(),



            "latency":

            latency,



            "message":

            "Stable Gesture"

            if stable_result["stable"]

            else

            "Waiting for stability"


        }