import json
import os
from datetime import datetime


class LearnerProfileService:

    # =====================================================
    # CONSTRUCTOR
    # =====================================================

    def __init__(
        self,
        profile_file="app/database/learner_profiles.json"
    ):
        self.profile_file = profile_file
        self.profiles = {}

        self.alphabets = [
            chr(i)
            for i in range(
                ord("A"),
                ord("Z") + 1
            )
        ]

        self.load_profiles()

    # =====================================================
    # LOAD PROFILES
    # =====================================================

    def load_profiles(self):

        if not os.path.exists(
            self.profile_file
        ):
            self.profiles = {}
            return

        try:

            with open(
                self.profile_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                if isinstance(data, dict):
                    self.profiles = data

                else:
                    self.profiles = {}

        except Exception as e:

            print(
                "LearnerProfileService Load Error:",
                e
            )

            self.profiles = {}

    # =====================================================
    # SAVE PROFILES
    # =====================================================

    def save_profiles(self):

        try:

            directory = os.path.dirname(
                self.profile_file
            )

            if directory:

                os.makedirs(
                    directory,
                    exist_ok=True
                )

            with open(
                self.profile_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.profiles,
                    file,
                    indent=4
                )

        except Exception as e:

            print(
                "LearnerProfileService Save Error:",
                e
            )

    # =====================================================
    # GET PROFILE
    # =====================================================

    def get_profile(self, student_id):

        student_id = str(student_id)

        if student_id not in self.profiles:

            self.profiles[student_id] = (
                self._create_default_profile(
                    student_id
                )
            )

            self.save_profiles()

        return self.profiles[student_id]

    # =====================================================
    # CREATE DEFAULT PROFILE
    # =====================================================

    def _create_default_profile(
        self,
        student_id
    ):

        now = datetime.now().isoformat()

        alphabet_mastery = {}

        for letter in self.alphabets:

            alphabet_mastery[letter] = {

                "accuracy": 0.0,

                "average_confidence": 0.0,

                "attempts": 0,

                "correct": 0,

                "incorrect": 0,

                "confused_with": {},

                "consecutive_correct": 0,

                "consecutive_incorrect": 0,

                "last_prediction": None,

                "last_confidence": 0.0,

                "last_practiced": None
            }

        return {

            "student_id":
                student_id,

            "created_at":
                now,

            "last_updated":
                now,

            "total_sessions":
                0,

            "total_attempts":
                0,

            "correct_attempts":
                0,

            "incorrect_attempts":
                0,

            "overall_accuracy":
                0.0,

            "completed_letters":
                [],

            "current_letter":
                "A",

            "next_letter":
                "A",

            "lesson_progress": {

                "completed":
                    0,

                "total":
                    26,

                "percentage":
                    0.0
            },

            "alphabet_mastery":
                alphabet_mastery
        }

    # =====================================================
    # CREATE PROFILE
    # =====================================================

    def create_profile(
        self,
        student_id
    ):

        student_id = str(student_id)

        if student_id in self.profiles:

            return self.profiles[student_id]

        self.profiles[student_id] = (
            self._create_default_profile(
                student_id
            )
        )

        self.save_profiles()

        return self.profiles[student_id]

    # =====================================================
    # PROFILE EXISTS
    # =====================================================

    def profile_exists(
        self,
        student_id
    ):

        return str(student_id) in self.profiles

    # =====================================================
    # INCREMENT SESSION
    # =====================================================

    def increment_sessions(
        self,
        student_id
    ):

        student_id = str(student_id)

        profile = self.get_profile(
            student_id
        )

        profile["total_sessions"] = (
            profile.get(
                "total_sessions",
                0
            ) + 1
        )

        profile["last_updated"] = (
            datetime.now().isoformat()
        )

        self.profiles[student_id] = profile

        self.save_profiles()

        return profile

    # =====================================================
    # CALCULATE OVERALL ACCURACY
    # =====================================================

    def calculate_overall_accuracy(
        self,
        student_id
    ):

        profile = self.get_profile(
            student_id
        )

        total = profile.get(
            "total_attempts",
            0
        )

        correct = profile.get(
            "correct_attempts",
            0
        )

        if total == 0:

            return 0.0

        return round(
            (correct / total) * 100,
            2
        )

    # =====================================================
    # GET COMPLETED LETTERS
    # =====================================================

    def get_completed_letters(
        self,
        student_id
    ):

        profile = self.get_profile(
            student_id
        )

        completed = profile.get(
            "completed_letters",
            []
        )

        if not isinstance(
            completed,
            list
        ):

            return []

        return list(completed)

    # =====================================================
    # GET CURRENT LETTER
    # =====================================================

    def get_current_letter(
        self,
        student_id
    ):

        profile = self.get_profile(
            student_id
        )

        return profile.get(
            "current_letter",
            "A"
        )

    # =====================================================
    # GET NEXT LETTER
    # =====================================================

    def get_next_letter(
        self,
        student_id
    ):

        profile = self.get_profile(
            student_id
        )

        return profile.get(
            "next_letter",
            "A"
        )

    # =====================================================
    # GET ALPHABET MASTERY
    # =====================================================

    def get_alphabet_mastery(
        self,
        student_id
    ):

        profile = self.get_profile(
            student_id
        )

        return profile.get(
            "alphabet_mastery",
            {}
        )

    # =====================================================
    # GET PRACTICED LETTERS
    # =====================================================

    def get_practiced_letters(
        self,
        student_id
    ):

        profile = self.get_profile(
            student_id
        )

        mastery = profile.get(
            "alphabet_mastery",
            {}
        )

        practiced = []

        for letter in self.alphabets:

            data = mastery.get(
                letter,
                {}
            )

            attempts = data.get(
                "attempts",
                0
            )

            if attempts > 0:

                practiced.append(letter)

        return practiced

    # =====================================================
    # GET WEAK GESTURES
    # =====================================================

    def get_weak_gestures(
        self,
        student_id
    ):

        profile = self.get_profile(
            student_id
        )

        mastery = profile.get(
            "alphabet_mastery",
            {}
        )

        weak_gestures = []

        for letter in self.alphabets:

            data = mastery.get(
                letter,
                {}
            )

            attempts = data.get(
                "attempts",
                0
            )

            accuracy = data.get(
                "accuracy",
                0.0
            )

            if (
                attempts >= 3
                and accuracy < 60
            ):

                weak_gestures.append(
                    letter
                )

        return weak_gestures

    # =====================================================
    # GET STRONG GESTURES
    # =====================================================

    def get_strong_gestures(
        self,
        student_id
    ):

        profile = self.get_profile(
            student_id
        )

        mastery = profile.get(
            "alphabet_mastery",
            {}
        )

        strong_gestures = []

        for letter in self.alphabets:

            data = mastery.get(
                letter,
                {}
            )

            attempts = data.get(
                "attempts",
                0
            )

            accuracy = data.get(
                "accuracy",
                0.0
            )

            if (
                attempts >= 3
                and accuracy >= 90
            ):

                strong_gestures.append(
                    letter
                )

        return strong_gestures

    # =====================================================
    # GET MOST CONFUSED GESTURES
    # =====================================================

    def get_confused_gestures(
        self,
        student_id
    ):

        profile = self.get_profile(
            student_id
        )

        mastery = profile.get(
            "alphabet_mastery",
            {}
        )

        confusion_data = []

        for letter in self.alphabets:

            data = mastery.get(
                letter,
                {}
            )

            confused_with = data.get(
                "confused_with",
                {}
            )

            if not confused_with:

                continue

            for predicted, count in (
                confused_with.items()
            ):

                confusion_data.append({

                    "expected":
                        letter,

                    "predicted":
                        predicted,

                    "count":
                        count
                })

        confusion_data.sort(
            key=lambda item: item["count"],
            reverse=True
        )

        return confusion_data

    # =====================================================
    # GET LEARNING LEVEL
    # =====================================================

    def get_learning_level(
        self,
        student_id
    ):

        accuracy = (
            self.calculate_overall_accuracy(
                student_id
            )
        )

        if accuracy >= 90:

            return "Mastered"

        elif accuracy >= 70:

            return "Good"

        elif accuracy >= 40:

            return "Improving"

        return "Beginner"

    # =====================================================
    # GENERATE RECOMMENDATIONS
    # =====================================================

    def generate_recommendations(
        self,
        student_id
    ):

        profile = self.get_profile(
            student_id
        )

        recommendations = []

        weak_gestures = (
            self.get_weak_gestures(
                student_id
            )
        )

        accuracy = (
            self.calculate_overall_accuracy(
                student_id
            )
        )

        current_letter = profile.get(
            "current_letter"
        )

        # -------------------------------------------------
        # WEAK LETTER RECOMMENDATION
        # -------------------------------------------------

        if weak_gestures:

            recommendations.append({

                "type":
                    "PRACTICE",

                "priority":
                    "HIGH",

                "message":
                    "Practice weak gestures: "
                    + ", ".join(
                        weak_gestures
                    )
            })

        # -------------------------------------------------
        # CURRENT LETTER
        # -------------------------------------------------

        if (
            current_letter
            and current_letter != "COMPLETED"
        ):

            recommendations.append({

                "type":
                    "NEXT_LETTER",

                "priority":
                    "NORMAL",

                "letter":
                    current_letter,

                "message":
                    f"Continue practicing "
                    f"the letter {current_letter}."
            })

        # -------------------------------------------------
        # BEGINNER
        # -------------------------------------------------

        if accuracy < 40:

            recommendations.append({

                "type":
                    "FOUNDATION",

                "priority":
                    "HIGH",

                "message":
                    "Continue basic alphabet "
                    "practice to improve consistency."
            })

        # -------------------------------------------------
        # IMPROVING
        # -------------------------------------------------

        elif accuracy < 70:

            recommendations.append({

                "type":
                    "CONSISTENCY",

                "priority":
                    "NORMAL",

                "message":
                    "Keep practicing regularly "
                    "to improve recognition accuracy."
            })

        # -------------------------------------------------
        # GOOD
        # -------------------------------------------------

        elif accuracy < 90:

            recommendations.append({

                "type":
                    "ADVANCED",

                "priority":
                    "NORMAL",

                "message":
                    "Good progress. Practice "
                    "confusing letters to improve accuracy."
            })

        # -------------------------------------------------
        # MASTERED
        # -------------------------------------------------

        else:

            recommendations.append({

                "type":
                    "MAINTENANCE",

                "priority":
                    "LOW",

                "message":
                    "Excellent work. Continue "
                    "practicing to maintain mastery."
            })

        return recommendations

    # =====================================================
    # GENERATE COMPLETE PROFILE ANALYTICS
    # =====================================================

    def generate_profile(
        self,
        student_id
    ):

        student_id = str(student_id)

        profile = self.get_profile(
            student_id
        )

        accuracy = (
            self.calculate_overall_accuracy(
                student_id
            )
        )

        completed_letters = (
            self.get_completed_letters(
                student_id
            )
        )

        practiced_letters = (
            self.get_practiced_letters(
                student_id
            )
        )

        completed_count = len(
            completed_letters
        )

        practiced_count = len(
            practiced_letters
        )

        lesson_progress = {

            "completed":
                completed_count,

            "total":
                26,

            "percentage":
                round(
                    (
                        completed_count / 26
                    ) * 100,
                    2
                )
        }

        weak_gestures = (
            self.get_weak_gestures(
                student_id
            )
        )

        strong_gestures = (
            self.get_strong_gestures(
                student_id
            )
        )

        confused_gestures = (
            self.get_confused_gestures(
                student_id
            )
        )

        learning_level = (
            self.get_learning_level(
                student_id
            )
        )

        recommendations = (
            self.generate_recommendations(
                student_id
            )
        )

        return {

            "student_id":
                student_id,

            "total_sessions":
                profile.get(
                    "total_sessions",
                    0
                ),

            "total_attempts":
                profile.get(
                    "total_attempts",
                    0
                ),

            "correct_attempts":
                profile.get(
                    "correct_attempts",
                    0
                ),

            "incorrect_attempts":
                profile.get(
                    "incorrect_attempts",
                    0
                ),

            "accuracy":
                accuracy,

            "learning_level":
                learning_level,

            # ---------------------------------------------
            # COMPLETION
            # ---------------------------------------------

            "completed_letters":
                completed_letters,

            "completed_count":
                completed_count,

            "remaining_count":
                max(
                    0,
                    26 - completed_count
                ),

            "progress_percentage":
                round(
                    (
                        completed_count / 26
                    ) * 100,
                    2
                ),

            # ---------------------------------------------
            # PRACTICE
            # ---------------------------------------------

            "practiced_letters":
                practiced_letters,

            "practiced_count":
                practiced_count,

            "practice_percentage":
                round(
                    (
                        practiced_count / 26
                    ) * 100,
                    2
                ),

            # ---------------------------------------------
            # LESSON PROGRESS
            # ---------------------------------------------

            "lesson_progress":
                lesson_progress,

            # ---------------------------------------------
            # CURRENT / NEXT
            # ---------------------------------------------

            "current_letter":
                profile.get(
                    "current_letter"
                ),

            "next_letter":
                profile.get(
                    "next_letter"
                ),

            # ---------------------------------------------
            # ANALYTICS
            # ---------------------------------------------

            "strong_gestures":
                strong_gestures,

            "weak_gestures":
                weak_gestures,

            "confused_gestures":
                confused_gestures,

            "alphabet_mastery":
                profile.get(
                    "alphabet_mastery",
                    {}
                ),

            "recommendations":
                recommendations,

            "created_at":
                profile.get(
                    "created_at"
                ),

            "last_updated":
                profile.get(
                    "last_updated"
                )
        }

    # =====================================================
    # UPDATE NEXT LETTER
    # =====================================================

    def update_next_letter(
        self,
        student_id,
        next_letter
    ):

        student_id = str(student_id)

        profile = self.get_profile(
            student_id
        )

        next_letter = (
            str(next_letter)
            .upper()
            .strip()
        )

        completed = set(
            profile.get(
                "completed_letters",
                []
            )
        )

        # -------------------------------------------------
        # VALIDATE REQUESTED LETTER
        # -------------------------------------------------

        if (
            next_letter in self.alphabets
            and next_letter not in completed
        ):

            profile["current_letter"] = (
                next_letter
            )

            profile["next_letter"] = (
                next_letter
            )

        else:

            fallback = None

            for letter in self.alphabets:

                if letter not in completed:

                    fallback = letter
                    break

            profile["current_letter"] = (
                fallback
            )

            profile["next_letter"] = (
                fallback
            )

        profile["last_updated"] = (
            datetime.now().isoformat()
        )

        self.profiles[student_id] = profile

        self.save_profiles()

        return profile

    # =====================================================
    # RESET PROFILE
    # =====================================================

    def reset_profile(
        self,
        student_id
    ):

        student_id = str(student_id)

        self.profiles[student_id] = (
            self._create_default_profile(
                student_id
            )
        )

        self.save_profiles()

        return self.profiles[student_id]

    # =====================================================
    # DELETE PROFILE
    # =====================================================

    def delete_profile(
        self,
        student_id
    ):

        student_id = str(student_id)

        if student_id not in self.profiles:

            return False

        del self.profiles[student_id]

        self.save_profiles()

        return True

    # =====================================================
    # GET ALL PROFILES
    # =====================================================

    def get_all_profiles(self):

        return list(
            self.profiles.values()
        )

    # =====================================================
    # GET PROFILE COUNT
    # =====================================================

    def get_profile_count(self):

        return len(
            self.profiles
        )

    # =====================================================
    # UPDATE PROFILE AFTER ATTEMPT
    # =====================================================

    def update_after_attempt(
        self,
        student_id,
        alphabet,
        predicted,
        confidence,
        correct
    ):
        """
        Update learner profile after one completed
        alphabet assessment attempt.
        """

        student_id = str(student_id)

        alphabet = (
            str(alphabet)
            .upper()
            .strip()
        )

        predicted = (
            str(predicted)
            .upper()
            .strip()
        )

        # -------------------------------------------------
        # VALIDATE CONFIDENCE
        # -------------------------------------------------

        try:

            confidence = float(
                confidence
            )

        except (
            TypeError,
            ValueError
        ):

            confidence = 0.0

        confidence = max(
            0.0,
            min(1.0, confidence)
        )

        # -------------------------------------------------
        # NORMALIZE CORRECT VALUE
        # -------------------------------------------------

        if isinstance(
            correct,
            str
        ):

            correct = (
                correct.strip().lower()
                in (
                    "true",
                    "1",
                    "yes"
                )
            )

        else:

            correct = bool(correct)

        # -------------------------------------------------
        # GET PROFILE
        # -------------------------------------------------

        profile = self.get_profile(
            student_id
        )

        # -------------------------------------------------
        # VALIDATE ALPHABET
        # -------------------------------------------------

        if alphabet not in self.alphabets:

            print(
                "LearnerProfileService: "
                f"Invalid alphabet '{alphabet}'"
            )

            return profile

        # -------------------------------------------------
        # UPDATE GLOBAL ATTEMPTS
        # -------------------------------------------------

        profile["total_attempts"] = (
            profile.get(
                "total_attempts",
                0
            ) + 1
        )

        if correct:

            profile["correct_attempts"] = (
                profile.get(
                    "correct_attempts",
                    0
                ) + 1
            )

        else:

            profile["incorrect_attempts"] = (
                profile.get(
                    "incorrect_attempts",
                    0
                ) + 1
            )

        # -------------------------------------------------
        # UPDATE OVERALL ACCURACY
        # -------------------------------------------------

        total_attempts = profile.get(
            "total_attempts",
            0
        )

        correct_attempts = profile.get(
            "correct_attempts",
            0
        )

        if total_attempts > 0:

            profile["overall_accuracy"] = round(
                (
                    correct_attempts
                    / total_attempts
                ) * 100,
                2
            )

        else:

            profile["overall_accuracy"] = 0.0

        # -------------------------------------------------
        # GET ALPHABET DATA
        # -------------------------------------------------

        mastery = profile.setdefault(
            "alphabet_mastery",
            {}
        )

        # -------------------------------------------------
        # DEFAULT LETTER DATA
        # -------------------------------------------------

        default_letter_data = {

            "accuracy":
                0.0,

            "average_confidence":
                0.0,

            "attempts":
                0,

            "correct":
                0,

            "incorrect":
                0,

            "confused_with":
                {},

            "consecutive_correct":
                0,

            "consecutive_incorrect":
                0,

            "last_prediction":
                None,

            "last_confidence":
                0.0,

            "last_practiced":
                None
        }

        if alphabet not in mastery:

            mastery[alphabet] = (
                default_letter_data
            )

        letter_data = mastery[alphabet]

        # -------------------------------------------------
        # UPDATE LETTER ATTEMPTS
        # -------------------------------------------------

        previous_attempts = letter_data.get(
            "attempts",
            0
        )

        letter_data["attempts"] = (
            previous_attempts + 1
        )

        # -------------------------------------------------
        # UPDATE CORRECT / INCORRECT
        # -------------------------------------------------

        if correct:

            letter_data["correct"] = (
                letter_data.get(
                    "correct",
                    0
                ) + 1
            )

            letter_data["consecutive_correct"] = (
                letter_data.get(
                    "consecutive_correct",
                    0
                ) + 1
            )

            letter_data["consecutive_incorrect"] = 0

        else:

            letter_data["incorrect"] = (
                letter_data.get(
                    "incorrect",
                    0
                ) + 1
            )

            letter_data["consecutive_incorrect"] = (
                letter_data.get(
                    "consecutive_incorrect",
                    0
                ) + 1
            )

            letter_data["consecutive_correct"] = 0

        # -------------------------------------------------
        # UPDATE LETTER ACCURACY
        # -------------------------------------------------

        letter_attempts = letter_data.get(
            "attempts",
            0
        )

        letter_correct = letter_data.get(
            "correct",
            0
        )

        if letter_attempts > 0:

            letter_data["accuracy"] = round(
                (
                    letter_correct
                    / letter_attempts
                ) * 100,
                2
            )

        else:

            letter_data["accuracy"] = 0.0

        # -------------------------------------------------
        # UPDATE AVERAGE CONFIDENCE
        # -------------------------------------------------

        previous_average = letter_data.get(
            "average_confidence",
            0.0
        )

        n = previous_attempts

        letter_data["average_confidence"] = round(
            (
                (
                    previous_average * n
                )
                + confidence
            )
            / (n + 1),
            4
        )

        # -------------------------------------------------
        # LAST PREDICTION INFORMATION
        # -------------------------------------------------

        letter_data["last_prediction"] = (
            predicted
        )

        letter_data["last_confidence"] = (
            confidence
        )

        letter_data["last_practiced"] = (
            datetime.now().isoformat()
        )

        # -------------------------------------------------
        # CONFUSION TRACKING
        # -------------------------------------------------

        if not correct:

            confused_with = (
                letter_data.setdefault(
                    "confused_with",
                    {}
                )
            )

            confused_with[predicted] = (
                confused_with.get(
                    predicted,
                    0
                ) + 1
            )

        # -------------------------------------------------
        # SAVE MASTERY DATA
        # -------------------------------------------------

        mastery[alphabet] = letter_data

        profile["alphabet_mastery"] = mastery

        # =================================================
        # COMPLETED LETTER LOGIC
        # =================================================
        #
        # A letter is completed when:
        #
        #   1. At least 3 attempts were made
        #   2. Accuracy is at least 80%
        #
        # This prevents a single lucky correct prediction
        # from completing a letter.
        #
        # =================================================

        completed_letters = profile.get(
            "completed_letters",
            []
        )

        if not isinstance(
            completed_letters,
            list
        ):

            completed_letters = []

        letter_is_completed = (
            letter_attempts >= 3
            and letter_data["accuracy"] >= 80
        )

        if (
            letter_is_completed
            and alphabet not in completed_letters
        ):

            completed_letters.append(
                alphabet
            )

        profile["completed_letters"] = (
            completed_letters
        )

        # =================================================
        # LESSON PROGRESS
        # =================================================

        completed_count = len(
            completed_letters
        )

        profile["lesson_progress"] = {

            "completed":
                completed_count,

            "total":
                len(self.alphabets),

            "percentage":
                round(
                    (
                        completed_count
                        / len(self.alphabets)
                    ) * 100,
                    2
                )
        }

        # =================================================
        # DETERMINE CURRENT / NEXT LETTER
        # =================================================

        completed_set = set(
    completed_letters
)
        if len(completed_set) == len(self.alphabets):
            profile["current_letter"] = "COMPLETED"
            profile["next_letter"] = "COMPLETED"
        else:
            current_letter = profile.get(
        "current_letter"
    )
            if (
        current_letter not in self.alphabets
        or current_letter in completed_set
    ):  
                current_letter = None
                for letter in self.alphabets:
                    if letter not in completed_set:
                        current_letter = letter
                        break
            profile["current_letter"] = current_letter
            profile["next_letter"] = current_letter


        profile["last_updated"] = (
            datetime.now().isoformat()
        )

        # =================================================
        # SAVE PROFILE
        # =================================================

        self.profiles[student_id] = profile

        self.save_profiles()

        # =================================================
        # DEBUG
        # =================================================

        print(
            "\n========== LEARNER PROFILE UPDATED =========="
        )

        print(
            "Student        :",
            student_id
        )

        print(
            "Alphabet       :",
            alphabet
        )

        print(
            "Predicted      :",
            predicted
        )

        print(
            "Correct        :",
            correct
        )

        print(
            "Confidence     :",
            confidence
        )

        print(
            "Letter Attempts:",
            letter_attempts
        )

        print(
            "Letter Accuracy:",
            letter_data["accuracy"]
        )

        print(
            "Letter Complete:",
            letter_is_completed
        )

        print(
            "Total Attempts :",
            profile.get(
                "total_attempts",
                0
            )
        )

        print(
            "Overall Acc.   :",
            profile.get(
                "overall_accuracy",
                0
            )
        )

        print(
            "Practiced      :",
            self.get_practiced_letters(
                student_id
            )
        )

        print(
            "Completed      :",
            profile.get(
                "completed_letters",
                []
            )
        )

        print(
            "Current        :",
            profile.get(
                "current_letter"
            )
        )

        print(
            "Next           :",
            profile.get(
                "next_letter"
            )
        )

        print(
            "=============================================="
        )

        return profile