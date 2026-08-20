import math

from .rules.rule_loader import RuleLoader


class LandmarkAnalyzer:
    """
    SignSync Landmark Analysis Engine

    Responsibilities:

    - Finger state detection
    - Finger angle calculation
    - Palm orientation analysis
    - Gesture rule validation
    - Landmark comparison
    - Feedback generation
    """

    def __init__(self):

        self.rule_loader = RuleLoader()


    # =====================================================
    # Distance Calculation
    # =====================================================

    def distance(self, p1, p2):

        if not p1 or not p2:
            return 0

        return math.sqrt(
            (p1[0]-p2[0]) ** 2 +
            (p1[1]-p2[1]) ** 2 +
            (p1[2]-p2[2]) ** 2
        )



    # =====================================================
    # Angle Calculation
    # =====================================================

    def calculate_angle(
            self,
            p1,
            p2,
            p3
    ):


        try:

            v1 = (
                p1[0]-p2[0],
                p1[1]-p2[1]
            )


            v2 = (
                p3[0]-p2[0],
                p3[1]-p2[1]
            )


            dot = (
                v1[0]*v2[0]
                +
                v1[1]*v2[1]
            )


            mag1 = math.hypot(
                v1[0],
                v1[1]
            )


            mag2 = math.hypot(
                v2[0],
                v2[1]
            )


            if mag1 == 0 or mag2 == 0:
                return 0


            cosine = dot/(mag1*mag2)

            cosine = max(
                -1,
                min(
                    1,
                    cosine
                )
            )


            return round(
                math.degrees(
                    math.acos(cosine)
                ),
                2
            )


        except Exception:

            return 0




    # =====================================================
    # Finger State Detection
    # =====================================================

    def check_fingers(
            self,
            landmarks
    ):


        if len(landmarks) != 21:

            return {}



        fingers = {}



        try:


            fingers["Thumb"] = (

                "extended"

                if landmarks[4][0] < landmarks[3][0]

                else

                "folded"

            )



            fingers["Index"] = (

                "extended"

                if landmarks[8][1] < landmarks[6][1]

                else

                "folded"

            )



            fingers["Middle"] = (

                "extended"

                if landmarks[12][1] < landmarks[10][1]

                else

                "folded"

            )



            fingers["Ring"] = (

                "extended"

                if landmarks[16][1] < landmarks[14][1]

                else

                "folded"

            )



            fingers["Pinky"] = (

                "extended"

                if landmarks[20][1] < landmarks[18][1]

                else

                "folded"

            )


        except Exception:


            return {}



        return fingers




    # =====================================================
    # Finger Angles
    # =====================================================

    def get_finger_angles(
            self,
            landmarks
    ):


        if len(landmarks)!=21:

            return {}



        return {


            "Thumb":

            self.calculate_angle(

                landmarks[1],

                landmarks[2],

                landmarks[4]

            ),



            "Index":

            self.calculate_angle(

                landmarks[5],

                landmarks[6],

                landmarks[8]

            ),



            "Middle":

            self.calculate_angle(

                landmarks[9],

                landmarks[10],

                landmarks[12]

            ),



            "Ring":

            self.calculate_angle(

                landmarks[13],

                landmarks[14],

                landmarks[16]

            ),



            "Pinky":

            self.calculate_angle(

                landmarks[17],

                landmarks[18],

                landmarks[20]

            )


        }




    # =====================================================
    # Palm Orientation
    # =====================================================

    def check_palm_orientation(
            self,
            landmarks
    ):


        try:


            wrist = landmarks[0]

            middle = landmarks[9]


            if middle[1] < wrist[1]:

                return "palm_forward"


            else:

                return "palm_down"



        except Exception:

            return "unknown"




    # =====================================================
    # Feature Extraction
    # =====================================================

    def extract_features(
            self,
            landmarks
    ):


        return {


            "finger_status":

                self.check_fingers(
                    landmarks
                ),


            "finger_angles":

                self.get_finger_angles(
                    landmarks
                ),


            "palm_orientation":

                self.check_palm_orientation(
                    landmarks
                )


        }




    # =====================================================
    # Main Gesture Analysis
    # =====================================================

    def analyze(
            self,
            expected,
            landmarks
    ):


        if (
            not landmarks
            or
            len(landmarks)!=21
        ):


            return {


                "status":"failed",

                "expected":expected,

                "deviations":[
                    "Invalid landmark data"
                ],

                "messages":[
                    "Show your complete hand."
                ]

            }




        expected = str(expected).upper()



        features = self.extract_features(
            landmarks
        )


        deviations=[]

        messages=[]




        # Rule checking

        try:


            rule = self.rule_loader.get_rule(
                expected
            )


            if rule:


                rule.evaluate(

                    landmarks,

                    deviations,

                    messages

                )


        except Exception:


            pass




        deviations=list(
            dict.fromkeys(
                deviations
            )
        )


        messages=list(
            dict.fromkeys(
                messages
            )
        )



        if not deviations:


            messages.append(
                f"{expected} gesture finger position looks correct."
            )



        return {


            "status":"analyzed",

            "expected":expected,


            "finger_status":
                features["finger_status"],


            "finger_angles":
                features["finger_angles"],


            "palm_orientation":
                features["palm_orientation"],


            "deviations":
                deviations,


            "messages":
                messages

        }





    # =====================================================
    # Compare Two Landmark Sets
    # =====================================================

    def compare_landmarks(
            self,
            expected_landmarks,
            actual_landmarks
    ):


        if (

            not expected_landmarks

            or

            not actual_landmarks

            or

            len(expected_landmarks)!=21

            or

            len(actual_landmarks)!=21

        ):


            return {


                "status":"failed",

                "message":"Landmark mismatch"

            }



        avg_distance = sum(


            self.distance(
                a,
                b
            )


            for a,b in zip(

                expected_landmarks,

                actual_landmarks

            )


        )/21



        return {


            "status":"compared",

            "average_distance":
                round(
                    avg_distance,
                    4
                )

        }




    # =====================================================
    # Generate Summary
    # =====================================================

    def generate_summary(
            self,
            deviations
    ):


        if not deviations:

            return "Gesture posture looks correct."


        return (

            "Improve: "

            +

            ", ".join(
                deviations
            )

        )




    # =====================================================
    # Priority Feedback
    # =====================================================

    def get_priority_feedback(
            self,
            deviations
    ):


        keywords=[

            "thumb",
            "index",
            "middle",
            "ring",
            "pinky",
            "palm",
            "finger"

        ]



        return list(

            dict.fromkeys(

                [

                    d

                    for d in deviations

                    if any(

                        key in d.lower()

                        for key in keywords

                    )

                ]

            )

        )