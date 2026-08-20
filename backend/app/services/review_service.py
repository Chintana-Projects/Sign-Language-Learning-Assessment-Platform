from collections import Counter



class ReviewService:
    """
    Generates complete practice review after session ends.

    Provides:
    - Accuracy
    - Confidence trend
    - Gesture feedback
    - Motion metrics
    - Sign score analysis
    - Recommendations
    """



    @staticmethod
    def generate_review(session_data: dict):


        history = session_data.get(
            "history",
            []
        )



        total_attempts = len(history)



        correct_attempts = 0

        incorrect_attempts = 0



        correct_gestures = []

        incorrect_gestures = []



        confidence_trend = []

        gesture_feedback = []

        common_mistakes = []

        recommendation_counter = Counter()



        motion_history = []

        sign_scores = []



        temporal_frames = 0







        # =====================================
        # PROCESS HISTORY
        # =====================================

        for attempt in history:



            expected = attempt.get(
                "expected",
                ""
            )


            predicted = attempt.get(
                "predicted",
                "Unknown"
            )


            correct = attempt.get(
                "correct",
                False
            )



            confidence = float(
                attempt.get(
                    "confidence",
                    0
                )
            )



            # normalize confidence

            if confidence > 1:

                confidence = confidence / 100



            confidence_percent = round(
                confidence * 100,
                2
            )





            confidence_trend.append({

                "attempt":
                    len(confidence_trend)+1,


                "gesture":
                    expected,


                "confidence":
                    confidence_percent

            })









            # -----------------------------
            # Accuracy
            # -----------------------------


            if correct:


                correct_attempts += 1


                correct_gestures.append(
                    expected
                )


            else:


                incorrect_attempts += 1


                incorrect_gestures.append(
                    expected
                )


                recommendation_counter[expected]+=1










            # -----------------------------
            # Feedback
            # -----------------------------


            feedback = attempt.get(
                "feedback",
                {}
            )



            common_mistakes.extend(

                feedback.get(
                    "mistakes",
                    []
                )

            )





            gesture_feedback.append({

                "expected":
                    expected,


                "predicted":
                    predicted,


                "correct":
                    correct,


                "confidence":
                    confidence_percent,


                "feedback":
                    feedback.get(
                        "feedback_messages",
                        []
                    )

            })









            # -----------------------------
            # Motion Metrics
            # -----------------------------


            motion = attempt.get(
                "motion_metrics",
                {}
            )



            if motion:


                motion_history.append(
                    motion
                )



                temporal_frames += motion.get(
                    "frames_analyzed",
                    0
                )









            # -----------------------------
            # Sign Score
            # -----------------------------


            score = attempt.get(
                "sign_score",
                0
            )



            if isinstance(score,dict):


                score_value = score.get(
                    "overall_score",
                    0
                )


            else:


                score_value = score




            sign_scores.append(

                float(score_value)

            )











        # =====================================
        # ACCURACY
        # =====================================


        accuracy = 0



        if total_attempts:


            accuracy = round(

                (

                    correct_attempts /

                    total_attempts

                )

                *

                100,

                2

            )









        # =====================================
        # MOTION SUMMARY
        # =====================================


        motion_summary = {


            "gesture_stability":0,


            "average_confidence":0,


            "invalid_frames":0,


            "time_taken":0,


            "frames_analyzed":0

        }






        if motion_history:



            count=len(
                motion_history
            )



            motion_summary={



                "gesture_stability":

                round(

                    sum(

                        m.get(
                            "gesture_stability",
                            0
                        )

                        for m in motion_history

                    )

                    /

                    count,

                    2

                ),





                "average_confidence":

                round(

                    sum(

                        (

                        m.get(
                            "average_confidence",
                            0
                        )

                        )

                        for m in motion_history

                    )

                    /

                    count,

                    3

                ),





                "invalid_frames":

                sum(

                    m.get(
                        "invalid_frames",
                        0
                    )

                    for m in motion_history

                ),





                "time_taken":

                round(

                    sum(

                        m.get(
                            "time_taken",
                            0
                        )

                        for m in motion_history

                    )

                    /

                    count,

                    2

                ),





                "frames_analyzed":

                sum(

                    m.get(
                        "frames_analyzed",
                        0
                    )

                    for m in motion_history

                )

            }









        # =====================================
        # SIGN SCORE
        # =====================================


        average_sign_score=0



        if sign_scores:


            average_sign_score=round(

                sum(sign_scores)

                /

                len(sign_scores),

                2

            )





        if average_sign_score >=90:

            grade="Excellent"


        elif average_sign_score>=75:

            grade="Good"


        elif average_sign_score>=50:

            grade="Average"


        else:

            grade="Needs Improvement"









        # =====================================
        # MISTAKES
        # =====================================


        mistake_counter=Counter(
            common_mistakes
        )




        recommendations=[

            gesture

            for gesture,_

            in recommendation_counter.most_common(5)

        ]









        # =====================================
        # FINAL RESPONSE
        # =====================================


        return {



            "overall_score":
                accuracy,



            "accuracy":
                accuracy,



            "total_attempts":
                total_attempts,



            "correct_attempts":
                correct_attempts,



            "incorrect_attempts":
                incorrect_attempts,



            "correct_gestures":
                correct_gestures,



            "incorrect_gestures":
                incorrect_gestures,



            "confidence_trend":
                confidence_trend,



            "motion_metrics":
                motion_summary,



            "sign_score":{


                "overall_score":
                    average_sign_score,


                "grade":
                    grade

            },



            "temporal_sequence_length":
                temporal_frames,



            "common_mistakes":[


                {

                    "mistake":
                        mistake,


                    "count":
                        count

                }


                for mistake,count

                in mistake_counter.items()

            ],



            "gesture_feedback":
                gesture_feedback,



            "recommendations":
                recommendations

        }