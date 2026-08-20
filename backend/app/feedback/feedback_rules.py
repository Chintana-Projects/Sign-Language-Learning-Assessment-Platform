class FeedbackRules:
    """
    Stores gesture feedback rules.

    Each rule returns one or more human-readable
    correction messages.

    New rules can be added without modifying
    the Feedback Engine.
    """

    def __init__(self):

        self.rules = {

            ("A", "E"): [

                "Fold your thumb further into your palm.",

                "Keep all fingers tightly closed."

            ],

            ("A", "S"): [

                "Wrap your thumb across the front of your fingers.",

                "Close your fist completely."

            ],

            ("B", "D"): [

                "Keep all four fingers extended together.",

                "Do not bend your index finger."

            ],

            ("C", "O"): [

                "Open your hand wider to form a clear 'C' shape."

            ],

            ("D", "B"): [

                "Keep only the index finger raised.",

                "Fold the remaining fingers."

            ],

            ("E", "A"): [

                "Curl your fingers more tightly.",

                "Bring fingertips closer to your palm."

            ],

            ("F", "O"): [

                "Touch the thumb and index finger lightly.",

                "Keep the remaining fingers straight."

            ]

        }

    # -----------------------------------------
    # Return Feedback
    # -----------------------------------------

    def get_feedback(

        self,

        expected,

        predicted

    ):

        key = (

            expected.upper(),

            predicted.upper()

        )

        if key in self.rules:

            return self.rules[key]

        return [

            "Practice the gesture again while matching the reference image."

        ]