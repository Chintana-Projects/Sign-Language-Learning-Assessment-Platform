from datetime import datetime
import string
import uuid

from app.services.learner.learner_profile_service import LearnerProfileService


class SessionService:

    def __init__(self, profile_service=None):

        self.sessions = {}

        self.profile_service = (
            profile_service
            if profile_service is not None
            else LearnerProfileService()
        )

        self.alphabets = list(string.ascii_uppercase)

    # ============================================================
    # INTERNAL HELPERS
    # ============================================================

    def _normalize_letter(self, letter):

        if letter is None:
            return None

        letter = str(letter).upper().strip()

        if letter in self.alphabets:
            return letter

        return None

    # ------------------------------------------------------------

    def _normalize_completed_letters(self, completed_letters):

        if not isinstance(completed_letters, list):
            return []

        normalized = []

        for letter in completed_letters:

            letter = self._normalize_letter(letter)

            if letter is not None:
                normalized.append(letter)

        return list(dict.fromkeys(normalized))

    # ------------------------------------------------------------

    def _get_first_uncompleted_letter(self, completed_letters):

        completed = set(
            self._normalize_completed_letters(
                completed_letters
            )
        )

        for letter in self.alphabets:

            if letter not in completed:
                return letter

        return None

    # ------------------------------------------------------------

    def _get_remaining_letters(self, completed_letters):

        completed = set(
            self._normalize_completed_letters(
                completed_letters
            )
        )

        return [
            letter
            for letter in self.alphabets
            if letter not in completed
        ]

    # ------------------------------------------------------------

    def _get_next_uncompleted_letter(
        self,
        current_letter,
        completed_letters
    ):

        current_letter = self._normalize_letter(
            current_letter
        )

        completed = set(
            self._normalize_completed_letters(
                completed_letters
            )
        )

        if current_letter is None:

            return self._get_first_uncompleted_letter(
                completed
            )

        try:

            current_index = self.alphabets.index(
                current_letter
            )

        except ValueError:

            return self._get_first_uncompleted_letter(
                completed
            )

        # --------------------------------------------------------
        # Move forward from the letter that was actually practiced
        # --------------------------------------------------------

        for index in range(
            current_index + 1,
            len(self.alphabets)
        ):

            candidate = self.alphabets[index]

            if candidate not in completed:

                return candidate

        # --------------------------------------------------------
        # If nothing remains after current letter,
        # search again from A.
        # --------------------------------------------------------

        for letter in self.alphabets:

            if letter not in completed:

                return letter

        return None

    # ============================================================
    # PROFILE SYNCHRONIZATION
    # ============================================================

    def _sync_profile(self, session):

        student_id = session.get(
            "student_id"
        )

        if student_id is None:
            return

        try:

            profile = self.profile_service.get_profile(
                student_id
            )

            if not isinstance(profile, dict):
                return

            # ----------------------------------------------------
            # Completed letters
            # ----------------------------------------------------

            completed_letters = (
                self._normalize_completed_letters(
                    profile.get(
                        "completed_letters",
                        []
                    )
                )
            )

            profile["completed_letters"] = completed_letters

            # ----------------------------------------------------
            # Lesson progress
            # ----------------------------------------------------

            profile["lesson_progress"] = {

                "completed":
                    len(completed_letters),

                "total":
                    len(self.alphabets),

                "percentage":
                    round(
                        (
                            len(completed_letters)
                            /
                            len(self.alphabets)
                        ) * 100,
                        2
                    )
            }

            # ----------------------------------------------------
            # Synchronize session state with profile
            # ----------------------------------------------------

            if session.get(
                "practice_status"
            ) == "completed":

                profile["current_letter"] = "COMPLETED"

                profile["next_letter"] = "COMPLETED"

            else:

                session_current = (
                    self._normalize_letter(
                        session.get(
                            "current_letter"
                        )
                    )
                )

                session_next = (
                    self._normalize_letter(
                        session.get(
                            "next_letter"
                        )
                    )
                )

                # IMPORTANT:
                #
                # The session's actual letter is authoritative.
                #
                # This prevents recommendation/profile data
                # from changing the letter the user selected.

                if session_current is not None:

                    profile["current_letter"] = (
                        session_current
                    )

                if session_next is not None:

                    profile["next_letter"] = (
                        session_next
                    )

            profile["last_updated"] = (
                datetime.now().isoformat()
            )

            self.profile_service.profiles[
                str(student_id)
            ] = profile

            self.profile_service.save_profiles()

        except Exception as e:

            print(
                "PROFILE SYNC ERROR:",
                e
            )

    # ============================================================
    # START PRACTICE SESSION
    # ============================================================

    def start_session(
        self,
        lesson_id: int,
        student_id="default_student"
    ):

        session_id = str(
            uuid.uuid4()
        )

        student_id = str(
            student_id
        )

        # ========================================================
        # DETERMINE SELECTED LETTER
        # ========================================================

        selected_letter = None

        if (
            isinstance(lesson_id, int)
            and
            1 <= lesson_id <= len(self.alphabets)
        ):

            selected_letter = self.alphabets[
                lesson_id - 1
            ]

        # --------------------------------------------------------
        # Invalid lesson ID
        # --------------------------------------------------------

        if selected_letter is None:

            raise ValueError(
                "Invalid lesson_id. Must be between 1 and 26."
            )

        # ========================================================
        # LOAD PROFILE
        # ========================================================

        profile = self.profile_service.get_profile(
            student_id
        )

        if not isinstance(profile, dict):

            profile = {}

        # ========================================================
        # COMPLETED LETTERS
        # ========================================================

        completed_letters = (
            self._normalize_completed_letters(
                profile.get(
                    "completed_letters",
                    []
                )
            )
        )

        # ========================================================
        # IMPORTANT FIX
        # ========================================================
        #
        # DO NOT use:
        #
        # profile["current_letter"]
        #
        # or:
        #
        # profile["next_letter"]
        #
        # to decide what the user wants to practice.
        #
        # lesson_id came directly from the selected alphabet
        # button in the frontend.
        #
        # Therefore:
        #
        # lesson_id 1  -> A
        # lesson_id 2  -> B
        # lesson_id 3  -> C
        # lesson_id 4  -> D
        # ...
        # lesson_id 26 -> Z
        #
        # The selected letter MUST remain the current letter.
        #
        # ========================================================

        current_letter = selected_letter

        # ========================================================
        # NEXT LETTER
        # ========================================================
        #
        # At the beginning of a session, next_letter is the
        # currently selected letter because that is what is
        # currently being practiced.
        #
        # It will be changed after a correct attempt.
        #
        # ========================================================

        next_letter = selected_letter

        # ========================================================
        # REMAINING LETTERS
        # ========================================================

        remaining_letters = (
            self._get_remaining_letters(
                completed_letters
            )
        )

        # ========================================================
        # CREATE SESSION
        # ========================================================

        session = {

            # ----------------------------------------------------
            # Identity
            # ----------------------------------------------------

            "session_id":
                session_id,

            "lesson_id":
                lesson_id,

            "student_id":
                student_id,

            # ----------------------------------------------------
            # Learning State
            # ----------------------------------------------------

            "current_letter":
                current_letter,

            "next_letter":
                next_letter,

            # ----------------------------------------------------
            # Progress
            # ----------------------------------------------------

            "completed_letters":
                completed_letters.copy(),

            "remaining_letters":
                remaining_letters,

            "practice_status":
                "ongoing",

            # ----------------------------------------------------
            # Time
            # ----------------------------------------------------

            "start_time":
                datetime.now().isoformat(),

            "end_time":
                None,

            # ----------------------------------------------------
            # Statistics
            # ----------------------------------------------------

            "attempts":
                0,

            "correct_attempts":
                0,

            "incorrect_attempts":
                0,

            "accuracy":
                0,

            # ----------------------------------------------------
            # History
            # ----------------------------------------------------

            "history":
                [],

            "last_attempt":
                None,

            "last_processed_attempt":
                None,

            # ----------------------------------------------------
            # Analytics
            # ----------------------------------------------------

            "letter_attempts":
                {},

            "mastery":
                {},

            # ----------------------------------------------------
            # Runtime Prediction
            # ----------------------------------------------------

            "latest_prediction":
                None,

            "latest_confidence":
                0,

            "latest_stable_prediction": {

                "stable":
                    False,

                "prediction":
                    None,

                "confidence":
                    0,

                "stable_frames":
                    0,

                "unstable_frames":
                    0
            }
        }

        # ========================================================
        # SAVE SESSION
        # ========================================================

        self.sessions[
            session_id
        ] = session

        # ========================================================
        # COUNT NEW SESSION
        # ========================================================

        try:

            self.profile_service.increment_sessions(
                student_id
            )

        except Exception as e:

            print(
                "SESSION PROFILE UPDATE ERROR:",
                e
            )

        # ========================================================
        # IMPORTANT:
        # Sync profile with the ACTUAL selected letter.
        # ========================================================

        self._sync_profile(
            session
        )

        return session

    # ============================================================
    # GET NEXT LETTER
    # ============================================================

    def get_next_letter(
        self,
        current_letter
    ):

        current_letter = self._normalize_letter(
            current_letter
        )

        if current_letter is None:
            return None

        index = self.alphabets.index(
            current_letter
        )

        if index >= len(
            self.alphabets
        ) - 1:

            return None

        return self.alphabets[
            index + 1
        ]

    # ============================================================
    # GET SESSION
    # ============================================================

    def get_session(
        self,
        session_id
    ):

        return self.sessions.get(
            session_id
        )

    # ============================================================
    # UPDATE SESSION
    # ============================================================

    def update_session(
        self,
        session_id,
        session_data
    ):

        session = self.sessions.get(
            session_id
        )

        if session is None:
            return None

        if isinstance(
            session_data,
            dict
        ):

            session.update(
                session_data
            )

        return session

    # ============================================================
    # MOVE TO NEXT LETTER
    # ============================================================

    def move_to_next_letter(
        self,
        session_id,
        recommended_letter=None,
        correct=True,
        expected_letter=None
    ):

        session = self.sessions.get(
            session_id
        )

        if session is None:
            return None

        current_letter = self._normalize_letter(
            session.get(
                "current_letter"
            )
        )

        expected_letter = self._normalize_letter(
            expected_letter
        )

        # ========================================================
        # WRONG ATTEMPT
        # ========================================================

        if not correct:

            repeat_letter = (
                expected_letter
                or current_letter
            )

            if repeat_letter:

                session["current_letter"] = (
                    repeat_letter
                )

                session["next_letter"] = (
                    repeat_letter
                )

            self._sync_profile(
                session
            )

            return session

        # ========================================================
        # CORRECT ATTEMPT
        # ========================================================

        # The expected letter is authoritative.

        practiced_letter = (
            expected_letter
            or current_letter
        )

        if practiced_letter is None:
            return session

        # ========================================================
        # LOAD LATEST PROFILE
        # ========================================================

        profile = self.profile_service.get_profile(
            session["student_id"]
        )

        if not isinstance(
            profile,
            dict
        ):

            profile = {}

        profile_completed = (
            self._normalize_completed_letters(
                profile.get(
                    "completed_letters",
                    []
                )
            )
        )

        # ========================================================
        # SYNCHRONIZE COMPLETED LETTERS
        # ========================================================

        session["completed_letters"] = (
            profile_completed.copy()
        )

        # ========================================================
        # DETERMINE NEXT LETTER
        # ========================================================
        #
        # IMPORTANT:
        #
        # recommended_letter is deliberately NOT used.
        #
        # Example:
        #
        # User selected D
        # Correct D
        #
        # Next should be E.
        #
        # Even if the recommendation system says:
        # "Practice D again"
        #
        # it cannot override the actual sequence.
        #
        # ========================================================

        next_letter = (
            self._get_next_uncompleted_letter(
                practiced_letter,
                session["completed_letters"]
            )
        )

        # ========================================================
        # EVERYTHING MASTERED
        # ========================================================

        if next_letter is None:

            session["current_letter"] = (
                "COMPLETED"
            )

            session["next_letter"] = (
                "COMPLETED"
            )

            session["completed_letters"] = (
                self.alphabets.copy()
            )

            session["remaining_letters"] = []

            session["practice_status"] = (
                "completed"
            )

            session["end_time"] = (
                datetime.now().isoformat()
            )

            self._sync_profile(
                session
            )

            return session

        # ========================================================
        # MOVE FORWARD
        # ========================================================

        session["current_letter"] = (
            next_letter
        )

        session["next_letter"] = (
            self._get_next_uncompleted_letter(
                next_letter,
                session["completed_letters"]
            )
        )

        session["remaining_letters"] = (
            self._get_remaining_letters(
                session["completed_letters"]
            )
        )

        self._sync_profile(
            session
        )

        return session

    # ============================================================
    # RECORD ATTEMPT
    # ============================================================

    def record_attempt(
        self,
        session_id,
        attempt_data
    ):

        session = self.sessions.get(
            session_id
        )

        if session is None:
            return None

        if not isinstance(
            attempt_data,
            dict
        ):

            return session

        # ========================================================
        # DUPLICATE PROTECTION
        # ========================================================

        attempt_id = attempt_data.get(
            "attempt_id"
        )

        if attempt_id:

            if session.get(
                "last_processed_attempt"
            ) == attempt_id:

                return session

            session["last_processed_attempt"] = (
                attempt_id
            )

        # ========================================================
        # EXPECTED LETTER
        # ========================================================

        current_letter = self._normalize_letter(
            session.get(
                "current_letter"
            )
        )

        # --------------------------------------------------------
        # IMPORTANT:
        #
        # The session current_letter has priority.
        #
        # We do NOT allow the frontend's "expected" field
        # to change the actual lesson being practiced.
        #
        # This prevents D from becoming the expected letter
        # simply because the profile/recommendation says D.
        #
        # ========================================================

        expected_letter = current_letter

        # ========================================================
        # PREDICTED LETTER
        # ========================================================

        predicted_letter = self._normalize_letter(
            attempt_data.get(
                "predicted"
            )
        )

        # ========================================================
        # AUTHORITATIVE CORRECT CALCULATION
        # ========================================================

        correct = (

            expected_letter is not None

            and

            predicted_letter is not None

            and

            expected_letter == predicted_letter
        )

        # ========================================================
        # UPDATE LEARNER PROFILE
        # ========================================================

        self.profile_service.update_after_attempt(

            student_id=session["student_id"],

            alphabet=expected_letter,

            predicted=predicted_letter,

            confidence=attempt_data.get(
                "confidence",
                0
            ),

            correct=correct
        )

        # ========================================================
        # STORE AUTHORITATIVE ATTEMPT RESULT
        # ========================================================

        attempt_data["expected"] = (
            expected_letter
        )

        attempt_data["predicted"] = (
            predicted_letter
        )

        attempt_data["correct"] = (
            correct
        )

        # ========================================================
        # SESSION COUNTERS
        # ========================================================

        session["attempts"] += 1

        if correct:

            session["correct_attempts"] += 1

        else:

            session["incorrect_attempts"] += 1

        # ========================================================
        # HISTORY
        # ========================================================

        session["history"].append(
            attempt_data
        )

        session["last_attempt"] = (
            attempt_data
        )

        # ========================================================
        # SESSION ACCURACY
        # ========================================================

        if session["attempts"] > 0:

            session["accuracy"] = round(

                (
                    session["correct_attempts"]
                    /
                    session["attempts"]
                ) * 100,

                2
            )

        # ========================================================
        # LETTER ANALYTICS
        # ========================================================

        analytics_letter = (
            expected_letter
            or current_letter
        )

        if analytics_letter:

            if analytics_letter not in (
                session["letter_attempts"]
            ):

                session["letter_attempts"][
                    analytics_letter
                ] = {

                    "attempts":
                        0,

                    "correct":
                        0,

                    "incorrect":
                        0,

                    "accuracy":
                        0
                }

            letter_data = (
                session["letter_attempts"][
                    analytics_letter
                ]
            )

            letter_data["attempts"] += 1

            if correct:

                letter_data["correct"] += 1

            else:

                letter_data["incorrect"] += 1

            letter_data["accuracy"] = round(

                (
                    letter_data["correct"]
                    /
                    letter_data["attempts"]
                ) * 100,

                2
            )

            # ----------------------------------------------------
            # Mastery
            # ----------------------------------------------------

            if letter_data["accuracy"] >= 80:

                mastery_level = (
                    "mastered"
                )

            elif letter_data["accuracy"] >= 50:

                mastery_level = (
                    "learning"
                )

            else:

                mastery_level = (
                    "needs_practice"
                )

            session["mastery"][
                analytics_letter
            ] = {

                "attempts":
                    letter_data["attempts"],

                "correct":
                    letter_data["correct"],

                "incorrect":
                    letter_data["incorrect"],

                "accuracy":
                    letter_data["accuracy"],

                "mastery_level":
                    mastery_level,

                "level":
                    mastery_level
            }

        # ========================================================
        # RUNTIME PREDICTION
        # ========================================================

        session["latest_prediction"] = (
            predicted_letter
        )

        session["latest_confidence"] = (
            attempt_data.get(
                "confidence",
                0
            )
        )

        if "stable_prediction" in attempt_data:

            session["latest_stable_prediction"] = (
                attempt_data[
                    "stable_prediction"
                ]
            )

        # ========================================================
        # CORRECT ATTEMPT
        # ========================================================

        if correct:

            # Keep the letter that was actually practiced.

            session["current_letter"] = (
                expected_letter
            )

            session["next_letter"] = (
                expected_letter
            )

            # ----------------------------------------------------
            # Get latest completed letters
            # ----------------------------------------------------

            latest_profile = (
                self.profile_service.get_profile(
                    session["student_id"]
                )
            )

            profile_completed = (

                latest_profile.get(
                    "completed_letters",
                    []
                )

                if isinstance(
                    latest_profile,
                    dict
                )

                else []
            )

            session["completed_letters"] = (
                self._normalize_completed_letters(
                    profile_completed
                )
            )

            session["remaining_letters"] = (
                self._get_remaining_letters(
                    session["completed_letters"]
                )
            )

            # ----------------------------------------------------
            # IMPORTANT:
            #
            # Do NOT automatically move the session to another
            # letter here.
            #
            # The frontend will receive the completed letter and
            # next recommendation separately.
            #
            # This keeps the expected letter stable for the
            # current practice attempt.
            #
            # ----------------------------------------------------

            self._sync_profile(
                session
            )

        # ========================================================
        # WRONG ATTEMPT
        # ========================================================

        else:

            # Repeat the same expected letter.

            repeat_letter = (
                expected_letter
                or current_letter
            )

            session["current_letter"] = (
                repeat_letter
            )

            session["next_letter"] = (
                repeat_letter
            )

            # ----------------------------------------------------
            # Refresh completed letters
            # ----------------------------------------------------

            latest_profile = (
                self.profile_service.get_profile(
                    session["student_id"]
                )
            )

            profile_completed = (

                latest_profile.get(
                    "completed_letters",
                    []
                )

                if isinstance(
                    latest_profile,
                    dict
                )

                else []
            )

            session["completed_letters"] = (
                self._normalize_completed_letters(
                    profile_completed
                )
            )

            session["remaining_letters"] = (
                self._get_remaining_letters(
                    session["completed_letters"]
                )
            )

            self._sync_profile(
                session
            )

        return session

    # ============================================================
    # END SESSION
    # ============================================================

    def end_session(
        self,
        session_id
    ):

        session = self.sessions.get(
            session_id
        )

        if session is None:
            return None

        session["end_time"] = (
            datetime.now().isoformat()
        )

        if session["practice_status"] != "completed":

            session["practice_status"] = (
                "ended"
            )

        self._sync_profile(
            session
        )

        return session

    # ============================================================
    # GET REVIEW DATA
    # ============================================================

    def get_review(
        self,
        session_id
    ):

        session = self.sessions.get(
            session_id
        )

        if session is None:
            return None

        return {

            "success":
                True,

            "session_id":
                session_id,

            "student_id":
                session.get(
                    "student_id"
                ),

            "current_letter":
                session.get(
                    "current_letter"
                ),

            "next_letter":
                session.get(
                    "next_letter"
                ),

            "practice_status":
                session.get(
                    "practice_status"
                ),

            "accuracy":
                session.get(
                    "accuracy",
                    0
                ),

            "total_attempts":
                session.get(
                    "attempts",
                    0
                ),

            "correct_attempts":
                session.get(
                    "correct_attempts",
                    0
                ),

            "incorrect_attempts":
                session.get(
                    "incorrect_attempts",
                    0
                ),

            "completed_letters":
                session.get(
                    "completed_letters",
                    []
                ),

            "remaining_letters":
                session.get(
                    "remaining_letters",
                    []
                ),

            "mastery":
                session.get(
                    "mastery",
                    {}
                ),

            "letter_attempts":
                session.get(
                    "letter_attempts",
                    {}
                ),

            "history":
                session.get(
                    "history",
                    []
                )
        }

    # ============================================================
    # RESET SESSION
    # ============================================================

    def reset_session(
        self,
        session_id
    ):

        session = self.sessions.get(
            session_id
        )

        if session is None:
            return None

        current_letter = self._normalize_letter(
            session.get(
                "current_letter"
            )
        )

        if current_letter is None:
            current_letter = "A"

        # ========================================================
        # RESET SESSION PROGRESS
        # ========================================================

        session["completed_letters"] = []

        session["remaining_letters"] = (
            self.alphabets.copy()
        )

        session["current_letter"] = (
            current_letter
        )

        session["next_letter"] = (
            current_letter
        )

        # ========================================================
        # RESET STATISTICS
        # ========================================================

        session["attempts"] = 0

        session["correct_attempts"] = 0

        session["incorrect_attempts"] = 0

        session["accuracy"] = 0

        # ========================================================
        # RESET HISTORY
        # ========================================================

        session["history"] = []

        session["last_attempt"] = None

        session["last_processed_attempt"] = None

        # ========================================================
        # RESET ANALYTICS
        # ========================================================

        session["letter_attempts"] = {}

        session["mastery"] = {}

        # ========================================================
        # RESET STATUS
        # ========================================================

        session["practice_status"] = (
            "ongoing"
        )

        session["end_time"] = None

        # ========================================================
        # RESET PREDICTION
        # ========================================================

        session["latest_prediction"] = None

        session["latest_confidence"] = 0

        session["latest_stable_prediction"] = {

            "stable":
                False,

            "prediction":
                None,

            "confidence":
                0,

            "stable_frames":
                0,

            "unstable_frames":
                0
        }

        # --------------------------------------------------------
        # Session reset does NOT reset learner profile.
        # --------------------------------------------------------

        self._sync_profile(
            session
        )

        return session

    # ============================================================
    # DELETE SESSION
    # ============================================================

    def delete_session(
        self,
        session_id
    ):

        if session_id in self.sessions:

            del self.sessions[
                session_id
            ]

            return True

        return False

    # ============================================================
    # VALIDATE SESSION
    # ============================================================

    def validate_session(
        self,
        session_id
    ):

        session = self.sessions.get(
            session_id
        )

        if session is None:

            return {

                "valid":
                    False,

                "message":
                    "Session not found."
            }

        return {

            "valid":
                True,

            "session":
                session
        }

    # ============================================================
    # GET SESSION SUMMARY
    # ============================================================

    def get_summary(
        self,
        session_id
    ):

        session = self.sessions.get(
            session_id
        )

        if session is None:
            return None

        return {

            "session_id":
                session.get(
                    "session_id"
                ),

            "student_id":
                session.get(
                    "student_id"
                ),

            "lesson_id":
                session.get(
                    "lesson_id"
                ),

            "current_letter":
                session.get(
                    "current_letter"
                ),

            "next_letter":
                session.get(
                    "next_letter"
                ),

            "completed_letters":
                session.get(
                    "completed_letters",
                    []
                ),

            "remaining_letters":
                session.get(
                    "remaining_letters",
                    []
                ),

            "accuracy":
                session.get(
                    "accuracy",
                    0
                ),

            "attempts":
                session.get(
                    "attempts",
                    0
                ),

            "correct_attempts":
                session.get(
                    "correct_attempts",
                    0
                ),

            "incorrect_attempts":
                session.get(
                    "incorrect_attempts",
                    0
                ),

            "practice_status":
                session.get(
                    "practice_status"
                ),

            "mastery":
                session.get(
                    "mastery",
                    {}
                ),

            "letter_attempts":
                session.get(
                    "letter_attempts",
                    {}
                )
        }