from app.feedback.rules.rule_loader import RuleLoader


class GestureRules:
    """
    Dynamic gesture rule manager.

    New gestures can be added by creating
    a new rule file without changing this class.
    """


    def __init__(self):

        self.loader = RuleLoader()



    # -----------------------------------------
    # Get Rule
    # -----------------------------------------

    def get_rule(self, gesture):

        return self.loader.get_rule(
            gesture.upper()
        )



    # -----------------------------------------
    # Generate Rule Feedback
    # -----------------------------------------

    def evaluate(
            self,
            gesture,
            landmarks,
            deviations,
            messages
    ):


        rule = self.get_rule(
            gesture
        )


        if rule is None:

            return False



        return rule.evaluate(

            landmarks,

            deviations,

            messages

        )