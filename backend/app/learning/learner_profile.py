import json
import os
from datetime import datetime


class LearnerProfileService:

    # =====================================================
    # CONSTRUCTOR
    # =====================================================

    def __init__(self):

        self.profile_path = os.path.join(
            os.path.dirname(__file__),
            "learner_profiles.json"
        )

        self.alphabets = [
            chr(i)
            for i in range(ord("A"), ord("Z") + 1)
        ]

        self.profiles = self._load_profiles()

    # =====================================================
    # LOAD PROFILES
    # =====================================================

    def _load_profiles(self):

        if not os.path.exists(self.profile_path):
            return {}

        try:

            with open(
                self.profile_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                if isinstance(data, dict):
                    return data

        except Exception as e:

            print(
                "LearnerProfile Load Error:",
                e
            )

        return {}

    # =====================================================
    # SAVE PROFILES
    # =====================================================

    def _save_profiles(self):

        try:

            directory = os.path.dirname(self.profile_path)

            if directory:
                os.makedirs(
                    directory,
                    exist_ok=True
                )

            with open(
                self.profile_path,
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
                "LearnerProfile Save Error:",
                e
            )

    # =====================================================
    # CREATE DEFAULT ALPHABET DATA
    # =====================================================

    def _create_alphabet_data(self):

        return {

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

    # =====================================================
    # CREATE DEFAULT PROFILE
    # =====================================================

    def _create_default_profile(
        self,
        student_id
    ):

        alphabet_mastery = {}

        for letter in self.alphabets:

            alphabet_mastery[letter] = (
                self._create_alphabet_data()
            )

        now = datetime.now().isoformat()

        profile = {

            "student_id": str(student_id),

            "created_at": now,

            "last_updated": now,

            "total_sessions": 0,

            "total_attempts": 0,

            "correct_attempts": 0,

            "incorrect_attempts": 0,

            "overall_accuracy": 0.0,

            "completed_letters": [],

            "current_letter": "A",

            "next_letter": "A",

            "alphabet_mastery": alphabet_mastery,

"lesson_progress": {
    "completed": 0,
    "total": 26,
    "percentage": 0.0
}

        }

        return profile

    # =====================================================
    # GET OR CREATE PROFILE
    # =====================================================

    def _get_or_create_profile(
        self,
        student_id
    ):

        student_id = str(student_id)

        if student_id not in self.profiles:

            self.profiles[student_id] = (
                self._create_default_profile(
                    student_id
                )
            )

            self._save_profiles()

        return self.profiles[student_id]

    # =====================================================
    # FIND NEXT UNCOMPLETED LETTER
    # =====================================================

    def _find_next_letter(
        self,
        completed_letters
    ):

        completed = set(
            str(letter).upper()
            for letter in completed_letters
        )

        for letter in self.alphabets:

            if letter not in completed:
                return letter

        return None

    # =====================================================
    # UPDATE AFTER ATTEMPT
    # =====================================================

    def update_after_attempt(
        self,
        student_id,
        alphabet,
        predicted,
        confidence,
        correct
    ):

        # -------------------------------------------------
        # NORMALIZE INPUT
        # -------------------------------------------------

        student_id = str(student_id)

        alphabet = (
            str(alphabet)
            .upper()
            .strip()
        )

        predicted = (
            str(predicted).upper().strip()
            if predicted is not None
            else None
        )

        confidence = float(confidence)

        correct = bool(correct)

        # -------------------------------------------------
        # VALIDATE EXPECTED LETTER
        # -------------------------------------------------

        if alphabet not in self.alphabets:

            raise ValueError(
                f"Invalid alphabet: {alphabet}"
            )

        # -------------------------------------------------
        # GET PROFILE
        # -------------------------------------------------

        profile = self._get_or_create_profile(
            student_id
        )

        # -------------------------------------------------
        # UPDATE TIMESTAMP
        # -------------------------------------------------

        profile["last_updated"] = (
            datetime.now().isoformat()
        )

        # -------------------------------------------------
        # UPDATE TOTAL ATTEMPTS
        # -------------------------------------------------

        profile["total_attempts"] += 1

        if correct:

            profile["correct_attempts"] += 1

        else:

            profile["incorrect_attempts"] += 1

        # -------------------------------------------------
        # OVERALL ACCURACY
        # -------------------------------------------------

        profile["overall_accuracy"] = round(

            (
                profile["correct_attempts"]
                /
                profile["total_attempts"]
            ) * 100,

            2

        )

        # -------------------------------------------------
        # GET LETTER PROFILE
        # -------------------------------------------------

        letter_profile = profile[
            "alphabet_mastery"
        ].setdefault(

            alphabet,

            self._create_alphabet_data()

        )

        # -------------------------------------------------
        # UPDATE ATTEMPT COUNT
        # -------------------------------------------------

        letter_profile["attempts"] += 1

        # -------------------------------------------------
        # SAVE LAST PREDICTION
        # -------------------------------------------------

        letter_profile[
            "last_prediction"
        ] = predicted

        letter_profile[
            "last_confidence"
        ] = confidence

        # -------------------------------------------------
        # UPDATE CORRECT / INCORRECT
        # -------------------------------------------------

        if correct:

            letter_profile["correct"] += 1

            letter_profile[
                "consecutive_correct"
            ] += 1

            letter_profile[
                "consecutive_incorrect"
            ] = 0

        else:

            letter_profile["incorrect"] += 1

            letter_profile[
                "consecutive_incorrect"
            ] += 1

            letter_profile[
                "consecutive_correct"
            ] = 0

        # -------------------------------------------------
        # LETTER ACCURACY
        # -------------------------------------------------

        attempts = letter_profile["attempts"]

        letter_profile["accuracy"] = round(

            (
                letter_profile["correct"]
                /
                attempts
            ) * 100,

            2

        )

        # -------------------------------------------------
        # RUNNING AVERAGE CONFIDENCE
        # -------------------------------------------------

        previous_attempts = attempts - 1

        previous_average = (
            letter_profile[
                "average_confidence"
            ]
        )

        confidence_percentage = (
            confidence * 100
        )

        letter_profile[
            "average_confidence"
        ] = round(

            (
                (
                    previous_average
                    *
                    previous_attempts
                )
                +
                confidence_percentage
            )
            /
            attempts,

            2

        )

        # -------------------------------------------------
        # LAST PRACTICED
        # -------------------------------------------------

        letter_profile[
            "last_practiced"
        ] = datetime.now().isoformat()

        # -------------------------------------------------
        # CONFUSION TRACKING
        # -------------------------------------------------

        if (

            not correct

            and

            predicted

            and

            predicted != alphabet

            and

            predicted in self.alphabets

        ):

            confused = letter_profile[
                "confused_with"
            ]

            confused[predicted] = (
                confused.get(predicted, 0)
                + 1
            )

        # -------------------------------------------------
        # COMPLETED LETTER LOGIC
        # -------------------------------------------------

        if correct:

            if alphabet not in profile[
                "completed_letters"
            ]:

                profile[
                    "completed_letters"
                ].append(alphabet)

                profile[
                    "completed_letters"
                ] = sorted(
                    set(
                        profile[
                            "completed_letters"
                        ]
                    )
                )
                completed_count = len(
    profile.get(
        "completed_letters",
        []
    )
)
                profile["lesson_progress"] = {
    "completed": completed_count,
    "total": 26,
    "percentage": round(
        (
            completed_count / 26
        ) * 100,
        2
    )
}

        # -------------------------------------------------
        # CURRENT / NEXT LETTER
        # -------------------------------------------------

        next_letter = self._find_next_letter(

            profile[
                "completed_letters"
            ]

        )

        if next_letter:

            profile[
                "current_letter"
            ] = next_letter

            profile[
                "next_letter"
            ] = next_letter

        else:

            # All A-Z completed

            profile[
                "current_letter"
            ] = None

            profile[
                "next_letter"
            ] = None

        # -------------------------------------------------
        # SAVE PROFILE
        # -------------------------------------------------

        self.profiles[
            student_id
        ] = profile

        self._save_profiles()

        # -------------------------------------------------
        # DEBUG OUTPUT
        # -------------------------------------------------

        print(
            "\n========== LEARNER PROFILE UPDATED =========="
        )

        print(
            "Student:",
            student_id
        )

        print(
            "Expected:",
            alphabet
        )

        print(
            "Predicted:",
            predicted
        )

        print(
            "Correct:",
            correct
        )

        print(
            "Confidence:",
            confidence
        )

        print(
            "Overall Accuracy:",
            profile[
                "overall_accuracy"
            ]
        )

        print(
            "Completed:",
            profile[
                "completed_letters"
            ]
        )

        print(
            "Current Letter:",
            profile[
                "current_letter"
            ]
        )

        print(
            "Next Letter:",
            profile[
                "next_letter"
            ]
        )

        print(
            "============================================\n"
        )

        return profile

    # =====================================================
    # GET PROFILE
    # =====================================================

    def get_profile(
    self,
    student_id
):
        profile = self._get_or_create_profile(
        student_id
    )
        completed_count = len(
        profile.get(
            "completed_letters",
            []
        )
    )
        profile["lesson_progress"] = {
        "completed": completed_count,
        "total": 26,
        "percentage": round(
            (
                completed_count / 26
            ) * 100,
            2
        )
    }
        self.profiles[str(student_id)] = profile
        self._save_profiles()
        return profile
    # =====================================================
    # INCREMENT SESSION COUNT
    # =====================================================

    def increment_sessions(
        self,
        student_id
    ):

        student_id = str(student_id)

        profile = self._get_or_create_profile(
            student_id
        )

        profile[
            "total_sessions"
        ] += 1

        profile[
            "last_updated"
        ] = datetime.now().isoformat()

        self.profiles[
            student_id
        ] = profile

        self._save_profiles()

        return profile

    # =====================================================
    # UPDATE NEXT LETTER
    # =====================================================

    def update_next_letter(
        self,
        student_id,
        next_letter
    ):

        student_id = str(student_id)

        profile = self._get_or_create_profile(
            student_id
        )

        next_letter = (
            str(next_letter)
            .upper()
            .strip()
        )

        # -------------------------------------------------
        # Validate requested letter
        # -------------------------------------------------

        if (

            next_letter in self.alphabets

            and

            next_letter not in profile[
                "completed_letters"
            ]

        ):

            profile[
                "current_letter"
            ] = next_letter

            profile[
                "next_letter"
            ] = next_letter

        else:

            fallback = self._find_next_letter(

                profile[
                    "completed_letters"
                ]

            )

            profile[
                "current_letter"
            ] = fallback

            profile[
                "next_letter"
            ] = fallback

        # -------------------------------------------------
        # Save
        # -------------------------------------------------

        profile[
            "last_updated"
        ] = datetime.now().isoformat()

        self.profiles[
            student_id
        ] = profile

        self._save_profiles()

        return profile

    # =====================================================
    # RESET PROFILE
    # =====================================================

    def reset_profile(
        self,
        student_id
    ):

        student_id = str(student_id)

        self.profiles[
            student_id
        ] = self._create_default_profile(
            student_id
        )

        self._save_profiles()

        return self.profiles[
            student_id
        ]

    # =====================================================
    # DELETE PROFILE
    # =====================================================

    def delete_profile(
        self,
        student_id
    ):

        student_id = str(student_id)

        if student_id in self.profiles:

            del self.profiles[
                student_id
            ]

            self._save_profiles()

            return True

        return False

    # =====================================================
    # GET ALL PROFILES
    # =====================================================

    def get_all_profiles(self):

        return self.profiles

    # =====================================================
    # PROFILE EXISTS
    # =====================================================

    def profile_exists(
        self,
        student_id
    ):

        return str(student_id) in self.profiles