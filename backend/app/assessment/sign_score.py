class SignScoreCalculator:
    """
    Calculates overall gesture performance score.

    Score Components:

    Gesture Accuracy  -> 40%
    Confidence        -> 30%
    Stability         -> 20%
    Timing            -> 10%

    Total Score       -> 100%
    """



    def __init__(self):

        self.ACCURACY_WEIGHT = 40

        self.CONFIDENCE_WEIGHT = 30

        self.STABILITY_WEIGHT = 20

        self.TIMING_WEIGHT = 10




    # =====================================================
    # Calculate Sign Score
    # =====================================================

    def calculate(
            self,
            correct,
            confidence,
            stability,
            time_taken
    ):


        # =================================================
        # Normalize Confidence
        # =================================================

        try:

            confidence = float(
                confidence or 0
            )

        except:

            confidence = 0



        if confidence > 1:

            confidence = confidence / 100



        confidence = max(
            0,
            min(
                confidence,
                1
            )
        )





        # =================================================
        # Normalize Stability
        # =================================================

        try:

            stability = float(
                stability or 0
            )

        except:

            stability = 0




        stability = max(
            0,
            min(
                stability,
                100
            )
        )






        # =================================================
        # Normalize Time
        # =================================================

        try:

            time_taken = float(
                time_taken or 0
            )

        except:

            time_taken = 0







        # =================================================
        # Accuracy Score
        # =================================================

        accuracy_score = (

            self.ACCURACY_WEIGHT

            if correct

            else 0

        )







        # =================================================
        # Confidence Score
        # =================================================

        confidence_score = (

            confidence *

            self.CONFIDENCE_WEIGHT

        )







        # =================================================
        # Stability Score
        # =================================================

        stability_score = (

            stability / 100

        ) * self.STABILITY_WEIGHT







        # =================================================
        # Timing Score
        # =================================================

        timing_score = self.calculate_timing_score(
            time_taken
        )







        # =================================================
        # Final Score
        # =================================================

        total_score = (

            accuracy_score

            +

            confidence_score

            +

            stability_score

            +

            timing_score

        )




        total_score = round(

            max(
                min(
                    total_score,
                    100
                ),
                0
            ),

            2

        )






        return {


            "overall_score":

                total_score,



            "grade":

                self.get_grade(
                    total_score
                ),



            "components": {


                "accuracy":

                    round(

                        (
                            accuracy_score
                            /
                            self.ACCURACY_WEIGHT
                        )

                        *

                        100,

                        2

                    ),




                "confidence":

                    round(

                        confidence * 100,

                        2

                    ),




                "stability":

                    round(

                        stability,

                        2

                    ),





                "gesture_accuracy_score":

                    round(

                        accuracy_score,

                        2

                    ),




                "confidence_score":

                    round(

                        confidence_score,

                        2

                    ),




                "stability_score":

                    round(

                        stability_score,

                        2

                    ),




                "timing_score":

                    round(

                        timing_score,

                        2

                    ),




                "time_taken":

                    round(

                        time_taken,

                        2

                    )

            }


        }







    # =====================================================
    # Timing Score
    # =====================================================

    def calculate_timing_score(
            self,
            time_taken
    ):


        if time_taken <= 0:

            return 0





        # Excellent speed

        if time_taken <= 2:


            return self.TIMING_WEIGHT






        # Reduce after 2 seconds

        score = (

            self.TIMING_WEIGHT

            -

            (

                ((time_taken - 2) / 8)

                *

                self.TIMING_WEIGHT

            )

        )




        return round(

            max(
                score,
                0
            ),

            2

        )







    # =====================================================
    # Grade Calculation
    # =====================================================

    def get_grade(
            self,
            score
    ):



        if score >= 90:

            return "Excellent"



        elif score >= 75:

            return "Good"



        elif score >= 50:

            return "Average"



        else:

            return "Needs Improvement"