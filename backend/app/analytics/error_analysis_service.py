from collections import Counter, defaultdict

from app.analytics.confidence_analyzer import ConfidenceAnalyzer
from app.analytics.performance_trend import PerformanceTrendAnalyzer
from app.analytics.revision_priority import RevisionPriorityEngine


class ErrorAnalysisService:

    def __init__(self, assessment_history):

        self.assessment_history = assessment_history

        self.confidence_analyzer = ConfidenceAnalyzer()

        self.performance_trend = PerformanceTrendAnalyzer()

        self.revision_engine = RevisionPriorityEngine()


    # =================================================
    # MAIN ANALYSIS
    # =================================================

    def analyze_student(self, student_id):

        attempts = self.assessment_history.get_student_history(
            student_id
        )


        if not attempts:

            return {

                "student_id": student_id,

                "total_attempts": 0,

                "confusion_pairs": [],

                "repeated_mistakes": [],

                "low_confidence_gestures": [],

                "performance_trends": [],

                "revision_priority": []

            }



        confusion_pairs = self.find_confusion_pairs(
            attempts
        )


        repeated_mistakes = self.find_repeated_mistakes(
            attempts
        )


        low_confidence = self.confidence_analyzer.analyze(
            attempts
        )


        trends = self.performance_trend.analyze(
            attempts
        )


        revision_priority = self.revision_engine.generate(
            confusion_pairs,
            repeated_mistakes,
            low_confidence,
            trends
        )


        return {

            "student_id": student_id,

            "total_attempts": len(attempts),

            "confusion_pairs": confusion_pairs,

            "repeated_mistakes": repeated_mistakes,

            "low_confidence_gestures": low_confidence,

            "performance_trends": trends,

            "revision_priority": revision_priority

        }



    # =================================================
    # CONFUSION DETECTION
    # =================================================

    def find_confusion_pairs(self, attempts):


        confusion_counter = Counter()


        for attempt in attempts:


            expected = str(
                attempt.get(
                    "expected",
                    ""
                )
            ).upper()


            predicted = str(
                attempt.get(
                    "predicted",
                    ""
                )
            ).upper()



            correct = attempt.get(
                "correct",
                False
            )



            if (

                not correct

                and expected

                and predicted

                and predicted != "UNKNOWN"

            ):

                confusion_counter[
                    (
                        expected,
                        predicted
                    )
                ] += 1




        result = []



        for pair, count in confusion_counter.items():


            result.append(

                {

                    "target_alphabet":
                        pair[0],


                    "confused_with":
                        pair[1],


                    "mistake_count":
                        count,


                    "reason":
                        f"Learner frequently confuses {pair[0]} with {pair[1]}",


                    "priority":
                        (
                            "HIGH"
                            if count >= 3
                            else "MEDIUM"
                        )

                }

            )



        result.sort(

            key=lambda x:
                x["mistake_count"],

            reverse=True

        )


        return result





    # =================================================
    # REPEATED MISTAKES
    # =================================================

    def find_repeated_mistakes(self, attempts):


        mistake_counter = Counter()

        session_tracker = defaultdict(set)



        for attempt in attempts:


            correct = attempt.get(
                "correct",
                False
            )


            expected = attempt.get(
                "expected"
            )


            predicted = attempt.get(
                "predicted"
            )


            session_id = attempt.get(
                "session_id"
            )



            if (

                not correct

                and expected

                and predicted

                and predicted != "UNKNOWN"

            ):


                pair = (

                    str(expected).upper(),

                    str(predicted).upper()

                )


                mistake_counter[pair] += 1



                if session_id:

                    session_tracker[pair].add(
                        session_id
                    )




        result = []



        for pair, count in mistake_counter.items():


            if count >= 2:


                result.append(

                    {

                        "target_alphabet":
                            pair[0],


                        "wrong_prediction":
                            pair[1],


                        "mistake_count":
                            count,


                        "sessions_affected":
                            len(
                                session_tracker[pair]
                            ),


                        "reason":
                            (
                                f"{pair[0]} needs revision "
                                f"because it was predicted as "
                                f"{pair[1]} repeatedly"
                            ),


                        "priority":
                            (
                                "HIGH"
                                if count >= 3
                                else "MEDIUM"
                            )

                    }

                )



        result.sort(

            key=lambda x:
                x["mistake_count"],

            reverse=True

        )


        return result