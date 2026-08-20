class PersonalizedFeedback:


    def generate(
        self,
        current_attempt,
        previous_attempts
    ):


        feedback = []

        recommendations = []


        current_letter = current_attempt.get(
            "expected",
            "UNKNOWN"
        )


        current_confidence = current_attempt.get(
            "confidence",
            0
        )


        # -----------------------------------------
        # Normalize Confidence
        # -----------------------------------------

        if current_confidence > 1:

            current_confidence = current_confidence / 100



        # -----------------------------------------
        # First Attempt
        # -----------------------------------------

        if not previous_attempts:


            feedback.append(

                "This is your first attempt. Focus on correct hand positioning."

            )


            recommendations.append(

                "Practice slowly and hold the gesture until recognition is stable."

            )


            return {

                "feedback": feedback,

                "recommendations": recommendations

            }



        # -----------------------------------------
        # Previous Mistakes
        # -----------------------------------------

        mistakes = [

            attempt

            for attempt in previous_attempts

            if not attempt.get(
                "correct",
                False
            )

        ]



        letter_mistakes = [

            attempt

            for attempt in mistakes

            if attempt.get(
                "expected"
            )
            ==
            current_letter

        ]



        # -----------------------------------------
        # Repeated Mistake Detection
        # -----------------------------------------

        if len(letter_mistakes) >= 3:


            feedback.append(

                f"You are repeatedly making mistakes in {current_letter}."

            )


            recommendations.append(

                f"Revise {current_letter} and compare finger positions carefully."

            )


        elif len(letter_mistakes) > 0:


            feedback.append(

                f"You have attempted {current_letter} before. Continue improving."

            )



        else:


            feedback.append(

                f"Your performance on {current_letter} is improving."

            )




        # -----------------------------------------
        # Confidence Analysis
        # -----------------------------------------

        if current_confidence < 0.5:


            feedback.append(

                "Recognition confidence is low."

            )


            recommendations.append(

                "Keep your hand steady and make the sign clearer."

            )



        elif current_confidence >= 0.9:


            feedback.append(

                "Your gesture confidence is excellent."

            )


            recommendations.append(

                "Maintain this consistency."

            )



        else:


            recommendations.append(

                "Try holding the gesture slightly longer."

            )



        # -----------------------------------------
        # Accuracy History
        # -----------------------------------------

        total = len(previous_attempts)


        correct = sum(

            1

            for attempt in previous_attempts

            if attempt.get(
                "correct",
                False
            )

        )


        accuracy = (

            correct / total

        ) * 100



        if accuracy < 50:


            recommendations.append(

                "Spend more time revising basic alphabets."

            )


        elif accuracy > 80:


            feedback.append(

                "Your overall learning progress is strong."

            )



        return {


            "feedback": feedback,


            "recommendations": recommendations

        }