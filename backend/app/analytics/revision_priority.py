class RevisionPriorityEngine:


    def generate(
        self,
        confusion_pairs,
        repeated_mistakes,
        low_confidence_gestures,
        performance_trends
    ):


        priority_map = {}



        # =====================================
        # Helper Function
        # =====================================

        def create_entry(gesture):

            if gesture not in priority_map:

                priority_map[gesture] = {

                    "gesture": gesture,

                    "score": 0,

                    "reasons": []

                }



        # =====================================
        # Low Confidence Analysis
        # =====================================

        for item in low_confidence_gestures:


            gesture = item.get(
                "gesture"
            )


            if not gesture:
                continue


            create_entry(
                gesture
            )


            confidence = item.get(
                "average_confidence",
                100
            )



            if confidence < 50:

                priority_map[gesture]["score"] += 4

                priority_map[gesture]["reasons"].append(
                    "Very low confidence"
                )


            elif confidence < 70:

                priority_map[gesture]["score"] += 2

                priority_map[gesture]["reasons"].append(
                    "Low confidence"
                )



        # =====================================
        # Repeated Mistakes
        # =====================================

        for item in repeated_mistakes:


            gesture = item.get(
                "gesture"
            )


            if not gesture:
                continue



            create_entry(
                gesture
            )



            count = item.get(
                "mistake_count",
                0
            )



            if count >= 5:

                priority_map[gesture]["score"] += 4

                priority_map[gesture]["reasons"].append(
                    "Repeated mistakes across sessions"
                )


            elif count >= 3:

                priority_map[gesture]["score"] += 3

                priority_map[gesture]["reasons"].append(
                    "Frequent mistakes"
                )


            elif count >= 1:

                priority_map[gesture]["score"] += 1



        # =====================================
        # Confusion Analysis
        # =====================================

        for item in confusion_pairs:


            gesture = item.get(
                "expected"
            )


            predicted = item.get(
                "predicted"
            )


            if not gesture:
                continue



            create_entry(
                gesture
            )


            count = item.get(
                "count",
                0
            )



            if count >= 5:

                priority_map[gesture]["score"] += 4


            elif count >= 3:

                priority_map[gesture]["score"] += 3


            else:

                priority_map[gesture]["score"] += 1



            priority_map[gesture]["reasons"].append(
                f"Confused with {predicted}"
            )



        # =====================================
        # Performance Trend Analysis
        # =====================================

        for item in performance_trends:


            gesture = item.get(
                "gesture"
            )


            if not gesture:
                continue



            create_entry(
                gesture
            )


            # Accuracy decline

            if item.get(
                "accuracy_trend"
            ) == "DECLINING":


                priority_map[gesture]["score"] += 3


                priority_map[gesture]["reasons"].append(
                    "Accuracy declining"
                )



            # Confidence decline

            if item.get(
                "confidence_trend"
            ) == "DECLINING":


                priority_map[gesture]["score"] += 2


                priority_map[gesture]["reasons"].append(
                    "Confidence declining"
                )



            # Stability decline

            if item.get(
                "stability_trend"
            ) == "DECLINING":


                priority_map[gesture]["score"] += 2


                priority_map[gesture]["reasons"].append(
                    "Gesture stability decreasing"
                )



        # =====================================
        # Convert Score To Priority
        # =====================================

        result = []



        for item in priority_map.values():


            score = item["score"]



            if score >= 8:

                priority = "URGENT"


            elif score >= 4:

                priority = "HIGH"


            else:

                priority = "MEDIUM"



            result.append({

                "gesture":
                    item["gesture"],

                "priority":
                    priority,

                "priority_score":
                    score,

                "reasons":
                    list(
                        set(
                            item["reasons"]
                        )
                    )

            })



        # Highest priority first

        result.sort(

            key=lambda x:x["priority_score"],

            reverse=True

        )


        return result