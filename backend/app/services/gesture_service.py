from app.ai.ml.inference.predictor import Predictor
import time


class GestureService:


    def __init__(self):

        self.predictor = Predictor()



    # =================================================
    # Gesture Prediction
    # =================================================

    def predict(
        self,
        landmarks
    ):


        start_time = time.time()



        # ---------------------------------
        # No hand detected
        # ---------------------------------

        if not landmarks:

            return {

                "prediction": "UNKNOWN",

                "confidence": 0,

                "processing_time": 0,

                "valid": False,

                "reason": "No hand detected"

            }




        # ---------------------------------
        # Landmark count validation
        # ---------------------------------

        if len(landmarks) != 21:


            return {

                "prediction": "UNKNOWN",

                "confidence": 0,

                "processing_time":0,

                "valid":False,

                "reason":
                    "Invalid landmark count"

            }




        # ---------------------------------
        # Landmark format validation
        # ---------------------------------

        for point in landmarks:


            if (
                not isinstance(point,list)
                or
                len(point)!=3
            ):


                return {

                    "prediction":"UNKNOWN",

                    "confidence":0,

                    "processing_time":0,

                    "valid":False,

                    "reason":
                    "Invalid landmark format"

                }




        try:


            # ---------------------------------
            # ML Prediction
            # ---------------------------------

            result = self.predictor.predict(
                landmarks
            )



            if result is None:


                return {

                    "prediction":"UNKNOWN",

                    "confidence":0,

                    "processing_time":
                    round(
                        time.time()-start_time,
                        4
                    ),

                    "valid":False,

                    "reason":
                    "Empty model response"

                }



            prediction = result.get(
                "prediction"
            )



            confidence = result.get(
                "confidence",
                0
            )



            # ---------------------------------
            # Normalize confidence
            # ---------------------------------

            confidence = float(
                confidence
            )


            if confidence > 1:

                confidence /= 100




            # ---------------------------------
            # Normalize prediction
            # ---------------------------------

            if prediction is None:

                prediction = "UNKNOWN"


            prediction = str(
                prediction
            ).strip().upper()



            # ---------------------------------
            # Confidence filtering
            # ---------------------------------

            # keep low confidence prediction
            # for debugging

            if prediction == "":

                prediction="UNKNOWN"




            processing_time = round(

                time.time()-start_time,

                4

            )
            print(
    "GESTURE SERVICE OUTPUT:",
    prediction,
    confidence
)



            return {


                "prediction":

                    prediction,


                "confidence":

                    round(
                        confidence,
                        3
                    ),


                "processing_time":

                    processing_time,


                "valid":

                    True

            }





        except Exception as error:


            print(
                "Gesture prediction error:",
                error
            )



            return {


                "prediction":

                    "UNKNOWN",


                "confidence":

                    0,


                "processing_time":

                    round(
                        time.time()-start_time,
                        4
                    ),


                "valid":

                    False,


                "reason":

                    str(error)

            }