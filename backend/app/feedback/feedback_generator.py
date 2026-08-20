from app.feedback.feedback_rules import FeedbackRules


class FeedbackGenerator:
    """
    SignSync Feedback Generator

    Responsibilities:
    -----------------
    1. Compare expected and predicted gesture
    2. Generate correction feedback
    3. Provide structured response
    4. Support future rule expansion
    """


    def __init__(self):

        self.rules = FeedbackRules()



    # =====================================================
    # Generate Feedback
    # =====================================================

    def generate(
            self,
            expected,
            predicted,
            confidence,
            landmark_analysis=None
    ):


        expected = expected.upper()

        predicted = predicted.upper()



        # -------------------------------------------------
        # Correct Gesture
        # -------------------------------------------------

        if expected == predicted:


            if confidence >= 0.95:

                feedback_type = "excellent"
                title = "Excellent!"


                messages = [

                    "Perfect sign detected.",

                    "Maintain the same hand posture."

                ]


            elif confidence >= 0.85:


                feedback_type = "good"
                title = "Very Good!"


                messages = [

                    "Correct gesture detected.",

                    "Try holding the gesture steadily."

                ]


            else:


                feedback_type = "correct"
                title = "Correct"


                messages = [

                    "Gesture is correct.",

                    "Practice to improve confidence."

                ]


            return {


                "expected":
                    expected,


                "predicted":
                    predicted,


                "correct":
                    True,


                "confidence":
                    confidence,


                "feedback_type":
                    feedback_type,


                "feedback_title":
                    title,


                "feedback_messages":
                    messages,


                "mistakes":
                    [],


                "improvement_tips":
                    [],


                "landmark_analysis":
                    landmark_analysis or {}

            }





        # -------------------------------------------------
        # Incorrect Gesture
        # -------------------------------------------------


        correction_messages = self.rules.get_feedback(

            expected,

            predicted

        )



        mistakes = []

        improvement_tips = []



        # Add landmark based corrections

        if landmark_analysis:


            deviations = landmark_analysis.get(

                "deviations",

                []

            )


            messages = landmark_analysis.get(

                "messages",

                []

            )



            mistakes.extend(
                deviations
            )


            improvement_tips.extend(
                messages
            )



        # Combine rule feedback

        improvement_tips.extend(

            correction_messages

        )



        return {


            "expected":
                expected,


            "predicted":
                predicted,


            "correct":
                False,


            "confidence":
                confidence,


            "feedback_type":
                "incorrect",


            "feedback_title":
                "Needs Improvement",


            "feedback_messages":

                [

                    f"Expected sign {expected}, but detected {predicted}."

                ]

                +

                improvement_tips,



            "mistakes":
                list(
                    dict.fromkeys(
                        mistakes
                    )
                ),



            "improvement_tips":

                list(
                    dict.fromkeys(
                        improvement_tips
                    )
                ),



            "landmark_analysis":

                landmark_analysis or {}

        }