
from datetime import datetime
import string
import uuid

from app.services.learner.learner_profile_service import LearnerProfileService


class SessionService:

    def __init__(self):

        self.sessions = {}

        self.profile_service = LearnerProfileService()

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

    def _get_first_uncompleted_letter(self, completed_letters):

        completed = set(
            self._normalize_letter(letter)
            for letter in completed_letters
        )

        completed.discard(None)

        for letter in self.alphabets:

            if letter not in completed:
                return letter

        return None

    # ------------------------------------------------------------

    def _get_remaining_letters(self, completed_letters):

        completed = set(
            self._normalize_letter(letter)
            for letter in completed_letters
        )

        completed.discard(None)

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
            self._normalize_letter(letter)
            for letter in completed_letters
        )

        completed.discard(None)

        if current_letter is None:

            return self._get_first_uncompleted_letter(
                completed_letters
            )

        try:

            current_index = self.alphabets.index(
                current_letter
            )

        except ValueError:

            return self._get_first_uncompleted_letter(
                completed_letters
            )

        # --------------------------------------------------------
        # First try normal A -> B -> C -> ... progression
        # --------------------------------------------------------

        for index in range(
            current_index + 1,
            len(self.alphabets)
        ):

            candidate = self.alphabets[index]

            if candidate not in completed:

                return candidate

        # --------------------------------------------------------
        # If there are uncompleted letters before current,
        # return the first one.
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
            # IMPORTANT
            #
            # Do NOT overwrite lifetime profile statistics with
            # session statistics.
            #
            # LearnerProfileService.update_after_attempt()
            # already maintains:
            #
            # total_attempts
            # correct_attempts
            # incorrect_attempts
            # overall_accuracy
            #
            # Therefore these values are intentionally NOT copied
            # from session here.
            # ----------------------------------------------------

            profile["total_sessions"] = profile.get(
                "total_sessions",
                0
            )

            # ----------------------------------------------------
            # Always use the profile as the source of truth for
            # completed letters.
            # ----------------------------------------------------

            completed_letters = profile.get(
                "completed_letters",
                []
            )

            if not isinstance(
                completed_letters,
                list
            ):

                completed_letters = []

            normalized_completed = []

            for letter in completed_letters:

                normalized = self._normalize_letter(
                    letter
                )

                if normalized is not None:
                    normalized_completed.append(
                        normalized
                    )

            # Remove duplicates while preserving order
            normalized_completed = list(
                dict.fromkeys(
                    normalized_completed
                )
            )

            profile["completed_letters"] = (
                normalized_completed
            )

            # ----------------------------------------------------
            # Lesson progress
            # ----------------------------------------------------

            profile["lesson_progress"] = {

                "completed":
                    len(normalized_completed),

                "total":
                    len(self.alphabets),

                "percentage":
                    round(
                        (
                            len(normalized_completed)
                            / len(self.alphabets)
                        ) * 100,
                        2
                    )
            }

            # ----------------------------------------------------
            # Keep profile current/next letter synchronized with
            # session when the session has a valid learning state.
            # ----------------------------------------------------

            session_current = self._normalize_letter(
                session.get("current_letter")
            )

            session_next = self._normalize_letter(
                session.get("next_letter")
            )

            if session.get("practice_status") == "completed":

                profile["current_letter"] = "COMPLETED"
                profile["next_letter"] = "COMPLETED"

            else:

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

        profile = self.profile_service.get_profile(
            student_id
        )

        if not isinstance(
            profile,
            dict
        ):

            profile = {}

        print(
            "\n=========================================="
        )

        print(
            "STARTING NEW PRACTICE SESSION"
        )

        print(
            "STUDENT:",
            student_id
        )

        print(
            "LESSON:",
            lesson_id
        )

        print(
            "PROFILE:",
            profile
        )

        print(
            "=========================================="
        )

        completed_letters = profile.get(
            "completed_letters",
            []
        )

        if not isinstance(
            completed_letters,
            list
        ):

            completed_letters = []

        # --------------------------------------------------------
        # Normalize completed letters
        # --------------------------------------------------------

        completed_letters = [

            letter

            for letter in (
                self._normalize_letter(letter)
                for letter in completed_letters
            )

            if letter is not None
        ]

        # Remove duplicates
        completed_letters = list(
            dict.fromkeys(
                completed_letters
            )
        )

        profile_current = self._normalize_letter(
            profile.get(
                "current_letter"
            )
        )

        profile_next = self._normalize_letter(
            profile.get(
                "next_letter"
            )
        )

        # ========================================================
        # DETERMINE CURRENT LETTER
        # ========================================================

        current_letter = None

        # First use profile current letter if it is valid and
        # not mastered/completed.

        if profile_current in self.alphabets:

            if profile_current not in completed_letters:

                current_letter = profile_current

        # Otherwise use profile next letter.

        if current_letter is None:

            if profile_next in self.alphabets:

                if profile_next not in completed_letters:

                    current_letter = profile_next

        # Otherwise start from first uncompleted letter.

        if current_letter is None:

            current_letter = (
                self._get_first_uncompleted_letter(
                    completed_letters
                )
            )

        # ========================================================
        # ALL LETTERS ALREADY COMPLETED
        # ========================================================

        if current_letter is None:

            session = {

                "session_id":
                    session_id,

                "lesson_id":
                    lesson_id,

                "student_id":
                    student_id,

                "current_letter":
                    "COMPLETED",

                "next_letter":
                    "COMPLETED",

                "completed_letters":
                    self.alphabets.copy(),

                "remaining_letters":
                    [],

                "practice_status":
                    "completed",

                "start_time":
                    datetime.now().isoformat(),

                "end_time":
                    None,

                "attempts":
                    0,

                "correct_attempts":
                    0,

                "incorrect_attempts":
                    0,

                "accuracy":
                    0,

                "history":
                    [],

                "last_attempt":
                    None,

                "last_processed_attempt":
                    None,

                "letter_attempts":
                    {},

                "mastery":
                    {},

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

            self.sessions[
                session_id
            ] = session

            print(
                "ALL ALPHABETS ALREADY COMPLETED"
            )

            return session

        # ========================================================
        # CREATE NORMAL SESSION
        # ========================================================

        next_letter = (
            self._get_next_uncompleted_letter(
                current_letter,
                completed_letters
            )
        )

        # IMPORTANT:
        #
        # At the beginning of a session, "next_letter" is only
        # a recommendation/preview.
        #
        # The actual current letter remains current_letter.

        remaining_letters = (
            self._get_remaining_letters(
                completed_letters
            )
        )

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
            # Session Statistics
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

        self.sessions[
            session_id
        ] = session

        # Count this as a new learner session.

        try:

            self.profile_service.increment_sessions(
                student_id
            )

        except Exception as e:

            print(
                "SESSION PROFILE UPDATE ERROR:",
                e
            )

        print(
            "\n=========================================="
        )

        print(
            "SESSION CREATED"
        )

        print(
            "SESSION:",
            session_id
        )

        print(
            "CURRENT:",
            session["current_letter"]
        )

        print(
            "NEXT:",
            session["next_letter"]
        )

        print(
            "COMPLETED:",
            session["completed_letters"]
        )

        print(
            "REMAINING:",
            session["remaining_letters"]
        )

        print(
            "=========================================="
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

            print(
                "SESSION NOT FOUND"
            )

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

            print(
                "SESSION NOT FOUND"
            )

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

            print(
                "\n========== WRONG ATTEMPT =========="
            )

            print(
                "REPEAT:",
                session.get(
                    "current_letter"
                )
            )

            self._sync_profile(
                session
            )

            return session

        # ========================================================
        # CORRECT ATTEMPT
        # ========================================================

        if current_letter is None:

            current_letter = expected_letter

        if current_letter is None:

            return session

        # --------------------------------------------------------
        # Get latest profile state.
        #
        # LearnerProfileService decides which letters are officially
        # completed/mastered.
        # --------------------------------------------------------

        profile = self.profile_service.get_profile(
            session["student_id"]
        )

        if not isinstance(
            profile,
            dict
        ):

            profile = {}

        profile_completed = profile.get(
            "completed_letters",
            []
        )

        if not isinstance(
            profile_completed,
            list
        ):

            profile_completed = []

        normalized_profile_completed = []

        for letter in profile_completed:

            normalized = self._normalize_letter(
                letter
            )

            if normalized:

                normalized_profile_completed.append(
                    normalized
                )

        normalized_profile_completed = list(
            dict.fromkeys(
                normalized_profile_completed
            )
        )

        # --------------------------------------------------------
        # Keep session completion list synchronized.
        # --------------------------------------------------------

        session["completed_letters"] = (
            normalized_profile_completed.copy()
        )

        # ========================================================
        # RECOMMENDATION
        # ========================================================

        next_letter = None

        if recommended_letter:

            recommended_letter = (
                self._normalize_letter(
                    recommended_letter
                )
            )

            if recommended_letter:

                if (
                    recommended_letter
                    not in session["completed_letters"]
                ):

                    next_letter = (
                        recommended_letter
                    )

        # ========================================================
        # NORMAL SEQUENTIAL MOVEMENT
        # ========================================================

        if next_letter is None:

            # IMPORTANT:
            #
            # Do NOT use the completed list to decide whether the
            # immediate next alphabet can be visited.
            #
            # A letter may be correct but not yet "mastered".
            #
            # Therefore normal learning progression is simply:
            #
            # A -> B -> C -> D ...
            #
            # while completed_letters separately tracks mastery.

            try:

                current_index = (
                    self.alphabets.index(
                        current_letter
                    )
                )

            except ValueError:

                current_index = -1

            next_letter = None

            # First try immediate next alphabet.

            if (
                current_index >= 0
                and current_index + 1
                < len(self.alphabets)
            ):

                candidate = self.alphabets[
                    current_index + 1
                ]

                if candidate not in (
                    session["completed_letters"]
                ):

                    next_letter = candidate

            # ----------------------------------------------------
            # If immediate next letter is already mastered,
            # continue forward until finding the next uncompleted
            # letter.
            # ----------------------------------------------------

            if next_letter is None:

                for index in range(
                    current_index + 1,
                    len(self.alphabets)
                ):

                    candidate = self.alphabets[
                        index
                    ]

                    if candidate not in (
                        session["completed_letters"]
                    ):

                        next_letter = candidate
                        break

            # ----------------------------------------------------
            # If nothing exists after current, search from A.
            # ----------------------------------------------------

            if next_letter is None:

                next_letter = (
                    self._get_first_uncompleted_letter(
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

            print(
                "\n=========================================="
            )

            print(
                "PRACTICE COMPLETED"
            )

            print(
                "COMPLETED:",
                session["completed_letters"]
            )

            print(
                "=========================================="
            )

            self._sync_profile(
                session
            )

            return session

        # ========================================================
        # MOVE TO NEXT LETTER
        # ========================================================

        session["current_letter"] = (
            next_letter
        )

        # Keep next_letter as the current target for frontend
        # compatibility.

        session["next_letter"] = (
            next_letter
        )

        session["remaining_letters"] = (
            self._get_remaining_letters(
                session["completed_letters"]
            )
        )

        print(
            "\n=========================================="
        )

        print(
            "LETTER MOVED"
        )

        print(
            "COMPLETED:",
            session["completed_letters"]
        )

        print(
            "CURRENT:",
            session["current_letter"]
        )

        print(
            "NEXT:",
            session["next_letter"]
        )

        print(
            "REMAINING:",
            session["remaining_letters"]
        )

        print(
            "=========================================="
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

        print(
            "\n=========================================="
        )

        print(
            "RECORD SESSION ATTEMPT"
        )

        print(
            "SESSION:",
            session_id
        )

        print(
            "=========================================="
        )

        session = self.sessions.get(
            session_id
        )

        if session is None:

            print(
                "SESSION NOT FOUND"
            )

            return None

        if not isinstance(
            attempt_data,
            dict
        ):

            print(
                "INVALID ATTEMPT DATA"
            )

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

                print(
                    "DUPLICATE ATTEMPT IGNORED:",
                    attempt_id
                )

                return session

            session["last_processed_attempt"] = (
                attempt_id
            )

        # ========================================================
        # DETERMINE EXPECTED LETTER
        # ========================================================

        current_letter = self._normalize_letter(
            session.get(
                "current_letter"
            )
        )

        expected_letter = self._normalize_letter(
            attempt_data.get(
                "expected",
                current_letter
            )
        )

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
        #
        # This remains the ONLY place where learner lifetime
        # attempt statistics and alphabet mastery are updated.
        # ========================================================

        profile = self.profile_service.update_after_attempt(

            student_id=session["student_id"],

            alphabet=expected_letter,

            predicted=predicted_letter,

            confidence=attempt_data.get(
                "confidence",
                0
            ),

            correct=correct
        )

        # IMPORTANT:
        # Never trust frontend "correct".
        # Backend calculates it from expected/predicted.

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
        # SESSION ATTEMPT COUNTERS
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

        analytics_letter = expected_letter

        if analytics_letter is None:

            analytics_letter = current_letter

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

            # ====================================================
            # MASTERY
            # ====================================================

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
        # RECOMMENDATION
        # ========================================================

        recommended_letter = None

        recommendations = (
            attempt_data.get(
                "recommendations",
                []
            )
        )

        if isinstance(
            recommendations,
            list
        ):

            for recommendation in recommendations:

                if not isinstance(
                    recommendation,
                    dict
                ):

                    continue

                candidate = (
                    self._normalize_letter(
                        recommendation.get(
                            "alphabet"
                        )
                    )
                )

                if candidate:

                    if candidate not in (
                        session["completed_letters"]
                    ):

                        recommended_letter = (
                            candidate
                        )

                        break

        # ========================================================
        # MOVE LETTER
        # ========================================================

        if correct:

            session = self.move_to_next_letter(

                session_id,

                recommended_letter=(
                    recommended_letter
                ),

                correct=True,

                expected_letter=(
                    expected_letter
                )
            )

        else:

            # ----------------------------------------------------
            # Wrong attempt:
            # Stay on the expected letter.
            # ----------------------------------------------------

            session["current_letter"] = (
                expected_letter
                or current_letter
            )

            session["next_letter"] = (
                expected_letter
                or current_letter
            )

            # Get latest profile completion state.

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
                profile_completed.copy()
            )

            session["remaining_letters"] = (
                self._get_remaining_letters(
                    session["completed_letters"]
                )
            )

            self._sync_profile(
                session
            )

        # ========================================================
        # FINAL DEBUG
        # ========================================================

        print(
            "\n=========================================="
        )

        print(
            "ATTEMPT RESULT"
        )

        print(
            "EXPECTED:",
            expected_letter
        )

        print(
            "PREDICTED:",
            predicted_letter
        )

        print(
            "CORRECT:",
            correct
        )

        print(
            "SESSION ATTEMPTS:",
            session["attempts"]
        )

        print(
            "SESSION CORRECT:",
            session["correct_attempts"]
        )

        print(
            "SESSION INCORRECT:",
            session["incorrect_attempts"]
        )

        print(
            "SESSION ACCURACY:",
            session["accuracy"]
        )

        print(
            "COMPLETED:",
            session["completed_letters"]
        )

        print(
            "CURRENT:",
            session["current_letter"]
        )

        print(
            "NEXT:",
            session["next_letter"]
        )

        print(
            "STATUS:",
            session["practice_status"]
        )

        print(
            "=========================================="
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

        # If session was completed or current letter is invalid,
        # restart from A.

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
            self.get_next_letter(
                current_letter
            )
        )

        # ========================================================
        # RESET SESSION STATISTICS
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
        # IMPORTANT:
        #
        # Resetting a session does NOT reset the learner profile.
        #
        # The profile contains lifetime learning progress.
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

            print(
                "SESSION DELETED:",
                session_id
            )

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
