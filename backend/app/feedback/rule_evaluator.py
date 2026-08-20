from app.feedback.gesture_rules import GestureRuleEngine


class RuleEvaluator:
    """
    Compares detected finger states with
    expected finger states and generates
    correction messages.
    """

    @staticmethod
    def evaluate(expected_letter, detected_states):

        expected = GestureRuleEngine.get_rule(
            expected_letter
        )

        messages = []

        if not expected:

            return {
                "score": 100,
                "messages": []
            }

        total = len(expected)

        matched = 0

        for finger, expected_state in expected.items():

            detected_state = detected_states.get(finger)

            if detected_state == expected_state:

                matched += 1

            else:

                messages.append(

                    f"{finger.capitalize()} finger should be {expected_state}."

                )

        score = round(
            (matched / total) * 100,
            2
        )

        return {

            "score": score,

            "messages": messages

        }