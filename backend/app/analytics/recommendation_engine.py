from datetime import datetime


class RecommendationEngine:

    def generate(
        self,
        learner_profile,
        confusion_pairs=None,
        trends=None,
        learning_state=None
    ):
        recommendations = []

        confusion_pairs = confusion_pairs or []
        trends = trends or []

        alphabet_profiles = learner_profile.get("alphabet_mastery", {})
        completed_letters = learner_profile.get("completed_letters", [])

        # =====================================
        # No Practice History
        # =====================================
        if not alphabet_profiles:
            return [
                {
                    "alphabet": "A",
                    "reason": "Start learning from the beginning.",
                    "priority": "HIGH"
                }
            ]

        # =====================================
        # Confusion Detection
        # =====================================
        for confusion in confusion_pairs:
            expected = confusion.get("expected") or confusion.get("target_alphabet")
            predicted = confusion.get("predicted") or confusion.get("confused_with")
            count = confusion.get("count")
            if count is None:
                count = confusion.get("mistake_count", 0)

            if expected:
                recommendations.append({
                    "alphabet": expected,
                    "reason": f"Frequently confused with {predicted} ({count} times).",
                    "priority": "HIGH"
                })

        # =====================================
        # Performance Trend Analysis
        # =====================================
        for trend in trends:
            gesture = trend.get("gesture")
            overall = trend.get("overall_trend")

            if not gesture:
                continue

            if overall == "DECLINING":
                recommendations.append({
                    "alphabet": gesture,
                    "reason": "Performance is declining. Revision required.",
                    "priority": "HIGH"
                })

            elif overall == "IMPROVING":
                recommendations.append({
                    "alphabet": gesture,
                    "reason": "High improvement trend. Ready for advanced practice.",
                    "priority": "LOW"
                })

        # =====================================
        # Analyze Learner Profile
        # =====================================
        for letter, profile in alphabet_profiles.items():
            if (
        letter in completed_letters
        and profile.get("mastery_level") == "mastered"
    ):
                continue

            mastery = profile.get("accuracy", 0)
            confidence = profile.get("average_confidence", 0)
            attempts = profile.get("attempts", 0)

            confused_with = profile.get("confused_with", {})
            consecutive_incorrect = profile.get("consecutive_incorrect", 0)
            consecutive_correct = profile.get("consecutive_correct", 0)
            last_practice = profile.get("last_practiced")

            # -------------------------------
            # Consecutive Mistakes
            # -------------------------------
            if consecutive_incorrect >= 5:
                recommendations.append({
        "alphabet": letter,
        "reason": "Requires instructor style correction.",
        "priority": "HIGH"
    })
            elif consecutive_incorrect >= 3:
                recommendations.append({
        "alphabet": letter,
        "reason": f"Repeated mistakes detected ({consecutive_incorrect} consecutive failures).",
        "priority": "MEDIUM"
    })

            # -------------------------------
            # Profile Confusion Check
            # -------------------------------
            if confused_with:
                confused_letter = max(
                    confused_with,
                    key=confused_with.get
                )
                confusion_count = confused_with[confused_letter]

                if confusion_count >= 3:
                    recommendations.append({
                        "alphabet": letter,
                        "reason": f"Frequently confused with {confused_letter} ({confusion_count} times).",
                        "priority": "HIGH"
                    })

            # -------------------------------
            # Low Mastery
            # -------------------------------
            if mastery < 50:
                recommendations.append({
                    "alphabet": letter,
                    "reason": "Low mastery level.",
                    "priority": "HIGH"
                })

            # -------------------------------
            # Low Confidence
            # -------------------------------
            elif confidence < 40 and mastery < 80:
                recommendations.append({
                    "alphabet": letter,
                    "reason": "Low confidence despite correct predictions.",
                    "priority": "HIGH"
                })

            # -------------------------------
            # Not Enough Practice
            # -------------------------------
            elif attempts < 3 and mastery < 80:
                recommendations.append({
                    "alphabet": letter,
                    "reason": "Needs more practice attempts.",
                    "priority": "MEDIUM"
                })

            if last_practice:
                try:
                    last = datetime.fromisoformat(last_practice)
                    days = (datetime.now() - last).days
                    if (
            days >= 7
            and letter in completed_letters
            and learner_profile.get("current_letter") != letter
            and learner_profile.get("current_letter") not in [letter, "A", "B", "C"]
        ):
                        recommendations.append({
                "alphabet": letter,
                "reason": "Time to revise this previously learned alphabet.",
                "priority": "LOW"
            })
                except Exception:
                    pass
                if (
                mastery >= 90
                and confidence >= 70
                and attempts >= 5
                and consecutive_correct >= 3
            ):
                    recommendations.append({
                    "alphabet": letter,
                    "reason": "Stable performance achieved. Ready to progress.",
                    "priority": "LOW"
                })

        # =====================================
        # Remove Duplicate Alphabet Entries
        # Keep Highest Priority
        # =====================================
        priority_rank = {
            "HIGH": 0,
            "MEDIUM": 1,
            "LOW": 2
        }

        unique = {}

        for item in recommendations:
            letter = item["alphabet"]

            if (
                letter not in unique
                or priority_rank[item["priority"]] < priority_rank[unique[letter]["priority"]]
            ):
                unique[letter] = item

        recommendations = list(unique.values())

                # =====================================
        # Learning State Recommendation
        # =====================================

        if learning_state:
            level = learning_state.get("level")
            current_letter = learner_profile.get("current_letter")
            next_letter = learner_profile.get("next_letter")

            if level == "Beginner" and current_letter:
                recommendations.append({
                    "alphabet": current_letter,
                    "reason": "Keep practicing your current alphabet before moving ahead.",
                    "priority": "HIGH"
                })

            elif level == "Improving" and current_letter:
                recommendations.append({
                    "alphabet": current_letter,
                    "reason": "You're improving. Practice a few more times for consistency.",
                    "priority": "MEDIUM"
                })

            elif level == "Good" and next_letter:
                recommendations.append({
                    "alphabet": next_letter,
                    "reason": "You are ready to begin learning the next alphabet.",
                    "priority": "LOW"
                })

        # =====================================
        # Remove Duplicate Recommendations Again
        # =====================================

        unique = {}

        for item in recommendations:
            letter = item["alphabet"]

            if (
                letter not in unique
                or priority_rank[item["priority"]]
                < priority_rank[unique[letter]["priority"]]
            ):
                unique[letter] = item

        recommendations = list(unique.values())

        # =====================================
        # Final Sort
        # =====================================

        recommendations.sort(
            key=lambda x: (
                priority_rank[x["priority"]],
                x.get("alphabet") or ""
            )
        )

        # =====================================
        # Add Next Alphabet If Needed
        # =====================================
        if not recommendations:
            alphabet_order = [
                chr(i)
                for i in range(ord("A"), ord("Z") + 1)
            ]

            for letter in alphabet_order:
                if letter not in completed_letters:
                    recommendations.append({
                        "alphabet": letter,
                        "reason": "Next alphabet in learning sequence.",
                        "priority": "HIGH"
                    })
                    break

        # =====================================
        # All Alphabets Completed
        # =====================================
        if not recommendations:
            recommendations.append({
                "alphabet": None,
                "reason": "Excellent progress. Continue learning new alphabets.",
                "priority": "LOW"
            })

        # =====================================
        # FINAL RETURN
        # =====================================
        return recommendations