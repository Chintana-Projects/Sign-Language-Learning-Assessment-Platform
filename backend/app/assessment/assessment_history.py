import json
import os
from datetime import datetime


class AssessmentHistory:

    def __init__(self, history_file="app/database/assessment_history.json"):
        self.history_file = history_file
        self.history = []
        self.load_history()

    # ===========================================
    # LOAD HISTORY
    # ===========================================

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r") as file:
                    self.history = json.load(file)
            except Exception as e:
                print(f"Error loading assessment history: {e}")
                self.history = []
        else:
            self.history = []

    # ===========================================
    # SAVE HISTORY
    # ===========================================

    def save_history(self):
        try:
            directory = os.path.dirname(self.history_file)

            if directory:
                os.makedirs(directory, exist_ok=True)

            with open(self.history_file, "w") as file:
                json.dump(self.history, file, indent=4)

        except Exception as e:
            print(f"Error saving assessment history: {e}")

    # ===========================================
    # ADD ASSESSMENT
    # ===========================================

    def add(self, assessment):
        return self.add_attempt(assessment)

    # ===========================================
    # ADD ATTEMPT
    # ===========================================

    def add_attempt(self, attempt):
        """
        Saves a finalized attempt record completely unchanged.

        Preserves:
        - expected
        - predicted
        - confidence
        - correct status
        - motion metrics
        - feedback
        - score
        - timestamps
        - any additional fields
        """

        if attempt is None:
            return None

        # -------------------------------------------
        # Prevent duplicate assessment
        # -------------------------------------------

        assessment_id = attempt.get("assessment_id")

        if assessment_id:

            for item in self.history:

                if item.get("assessment_id") == assessment_id:
                    return item

        # -------------------------------------------
        # Preserve provided timestamp
        # -------------------------------------------

        if "saved_at" not in attempt or not attempt["saved_at"]:
            attempt["saved_at"] = datetime.now().isoformat()

        if "timestamp" not in attempt or not attempt["timestamp"]:
            attempt["timestamp"] = attempt["saved_at"]

        # -------------------------------------------
        # Create saved record
        # -------------------------------------------

        saved_record = {
            "student_id": str(attempt.get("student_id")),
            "session_id": attempt.get("session_id"),
            "assessment_id": attempt.get("assessment_id"),
            "expected": attempt.get("expected"),
            "predicted": attempt.get("predicted"),
            "confidence": attempt.get("confidence"),
            "correct": bool(attempt.get("correct")),
            "motion_metrics": attempt.get("motion_metrics", {}),
            "feedback": attempt.get("feedback", []),
            "sign_score": attempt.get("sign_score", 0),
            "timestamp": attempt.get("timestamp"),
            "saved_at": attempt.get("saved_at")
        }

        # -------------------------------------------
        # Preserve additional dynamic fields
        # -------------------------------------------

        for key, value in attempt.items():

            if key not in saved_record:
                saved_record[key] = value

        # -------------------------------------------
        # Add record to history
        # -------------------------------------------

        self.history.append(saved_record)

        # -------------------------------------------
        # Limit history
        # -------------------------------------------

        MAX_HISTORY = 5000

        if len(self.history) > MAX_HISTORY:
            self.history = self.history[-MAX_HISTORY:]

        # -------------------------------------------
        # Always save updated history
        # -------------------------------------------

        self.save_history()

        # -------------------------------------------
        # Debug information
        # -------------------------------------------

        print("\n========== HISTORY SAVED ==========")
        print("Student:", saved_record.get("student_id"))
        print("Session:", saved_record.get("session_id"))
        print("Assessment:", saved_record.get("assessment_id"))
        print("Expected:", saved_record.get("expected"))
        print("Predicted:", saved_record.get("predicted"))
        print("Correct:", saved_record.get("correct"))
        print("Total history records:", len(self.history))
        print("===================================\n")

        return saved_record

    # ===========================================
    # GET ALL ASSESSMENTS
    # ===========================================

    def get_all(self):
        return self.history

    # ===========================================
    # GET STUDENT ASSESSMENTS
    # ===========================================

    def get_student_history(self, student_id):

        if student_id is None:
            return []

        target_student_id = str(student_id)

        records = [
            item
            for item in self.history
            if str(item.get("student_id")) == target_student_id
        ]

        records.sort(
            key=lambda x: x.get("timestamp", "")
        )

        return records

    # ===========================================
    # GET SESSION ASSESSMENTS
    # ===========================================

    def get_session_history(self, session_id):

        if session_id is None:
            return []

        records = [
            item
            for item in self.history
            if item.get("session_id") == session_id
        ]

        records.sort(
            key=lambda x: x.get("timestamp", "")
        )

        return records

    # ===========================================
    # GET LATEST ASSESSMENT
    # ===========================================

    def latest(self):

        if not self.history:
            return None

        return self.history[-1]

    # ===========================================
    # CLEAR HISTORY
    # ===========================================

    def clear(self):

        self.history.clear()

        self.save_history()