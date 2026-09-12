# app/certification/certification_session.py

from datetime import datetime
import uuid
import string


class CertificationSession:

    def __init__(self):

        self.sessions = {}

        self.alphabets = list(
            string.ascii_uppercase
        )

    # ==========================================================
    # CREATE SESSION
    # ==========================================================

    def create_session(
        self,
        student_id: str
    ):

        certification_id = str(
            uuid.uuid4()
        )

        session = {

            # --------------------------------------------------
            # Identity
            # --------------------------------------------------

            "certification_id":
                certification_id,

            "student_id":
                str(student_id),

            # --------------------------------------------------
            # Status
            # --------------------------------------------------

            "status":
                "in_progress",

            "started_at":
                datetime.now().isoformat(),

            "completed_at":
                None,

            # --------------------------------------------------
            # Alphabet Assessment
            # --------------------------------------------------

            "letters":
                self.alphabets.copy(),

            "current_index":
                0,

            "current_letter":
                "A",

            # --------------------------------------------------
            # Progress
            # --------------------------------------------------

            "completed_letters":
                [],

            # --------------------------------------------------
            # Hidden Results
            # --------------------------------------------------

            "results":
                [],

            # --------------------------------------------------
            # Final Outcome
            # --------------------------------------------------

            "score":
                0,

            "final_score":
                None,

            "passed":
                False,

            "certificate_id":
                None
        }

        self.sessions[
            certification_id
        ] = session

        return session

    # ==========================================================
    # GET SESSION
    # ==========================================================

    def get_session(
        self,
        certification_id: str
    ):

        return self.sessions.get(
            certification_id
        )

    # ==========================================================
    # UPDATE SESSION
    # ==========================================================

    def update_session(
        self,
        certification_id: str,
        data: dict
    ):

        session = self.get_session(
            certification_id
        )

        if session is None:
            return None

        session.update(
            data
        )

        return session

    # ==========================================================
    # DELETE SESSION
    # ==========================================================

    def delete_session(
        self,
        certification_id: str
    ):

        if certification_id in self.sessions:

            del self.sessions[
                certification_id
            ]

            return True

        return False