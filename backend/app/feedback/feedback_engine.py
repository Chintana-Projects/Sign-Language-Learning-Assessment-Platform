from app.feedback.landmark_analyzer import LandmarkAnalyzer
from app.feedback.gesture_rules import GestureRules


class FeedbackEngine:
    """
    SignSync Intelligent Feedback Engine

    Pipeline:
    Prediction
        ↓
    Validation Feedback
        ↓
    Landmark Analysis
        ↓
    Gesture Rules
        ↓
    Intelligent Feedback
    """

    def __init__(self):
        self.rules = GestureRules()
        self.landmark_analyzer = LandmarkAnalyzer()

    # =====================================================
    # Evaluate Gesture
    # =====================================================
    def evaluate(
        self,
        expected,
        predicted,
        confidence,
        landmarks,
        validation_reason=None,
        stable_prediction=None,
        motion_metrics=None,
    ):
        expected = str(expected).upper()
        predicted = str(predicted).upper()

        correct = expected == predicted

        feedback_messages = []
        mistakes = []
        improvement_tips = []

        motion_metrics = motion_metrics or {}

        # =====================================================
        # Validation Feedback
        # =====================================================

        if validation_reason == "NO_HAND":
            return {
                "expected": expected,
                "predicted": predicted,
                "correct": False,
                "confidence": round(confidence, 3),
                "feedback_type": "validation",
                "feedback_title": "No Hand Detected",
                "feedback_messages": ["No hand was detected."],
                "mistakes": ["Place your hand inside the camera view."],
                "improvement_tips": ["Keep your hand centered before signing."],
                "landmark_analysis": {},
            }

        elif validation_reason == "HAND_OUTSIDE_FRAME":
            return {
                "expected": expected,
                "predicted": predicted,
                "correct": False,
                "confidence": round(confidence, 3),
                "feedback_type": "validation",
                "feedback_title": "Hand Outside Frame",
                "feedback_messages": [
                    "Your hand moved outside the camera view."
                ],
                "mistakes": ["Keep your entire hand visible."],
                "improvement_tips": [
                    "Move your hand toward the center of the frame."
                ],
                "landmark_analysis": {},
            }

        elif validation_reason == "HAND_TOO_SMALL":
            return {
                "expected": expected,
                "predicted": predicted,
                "correct": False,
                "confidence": round(confidence, 3),
                "feedback_type": "validation",
                "feedback_title": "Hand Too Far",
                "feedback_messages": ["Your hand is too far from the camera."],
                "mistakes": ["Hand occupies very little of the frame."],
                "improvement_tips": ["Move your hand closer to the webcam."],
                "landmark_analysis": {},
            }

        elif validation_reason == "MULTIPLE_HANDS":
            return {
                "expected": expected,
                "predicted": predicted,
                "correct": False,
                "confidence": round(confidence, 3),
                "feedback_type": "validation",
                "feedback_title": "Multiple Hands Detected",
                "feedback_messages": [
                    "Only one signing hand should be visible."
                ],
                "mistakes": ["Multiple hands confuse the recognizer."],
                "improvement_tips": [
                    "Keep only the active signing hand inside the frame."
                ],
                "landmark_analysis": {},
            }

        elif validation_reason == "INVALID_LANDMARKS":
            return {
                "expected": expected,
                "predicted": predicted,
                "correct": False,
                "confidence": round(confidence, 3),
                "feedback_type": "validation",
                "feedback_title": "Incomplete Hand",
                "feedback_messages": ["Incomplete hand landmarks detected."],
                "mistakes": ["Some fingers are not visible."],
                "improvement_tips": ["Keep your complete hand visible."],
                "landmark_analysis": {},
            }

        elif validation_reason == "NO_PERSON":
            return {
                "expected": expected,
                "predicted": predicted,
                "correct": False,
                "confidence": round(confidence, 3),
                "feedback_type": "validation",
                "feedback_title": "No Person Detected",
                "feedback_messages": ["No person is visible in the camera."],
                "mistakes": ["Stand in front of the webcam."],
                "improvement_tips": ["Keep your upper body visible."],
                "landmark_analysis": {},
            }

        elif validation_reason == "MULTIPLE_PEOPLE":
            return {
                "expected": expected,
                "predicted": predicted,
                "correct": False,
                "confidence": round(confidence, 3),
                "feedback_type": "validation",
                "feedback_title": "Multiple People",
                "feedback_messages": ["Multiple people detected."],
                "mistakes": ["Only one learner should appear."],
                "improvement_tips": ["Move others outside the camera."],
                "landmark_analysis": {},
            }

        elif validation_reason == "PARTIAL_BODY":
            return {
                "expected": expected,
                "predicted": predicted,
                "correct": False,
                "confidence": round(confidence, 3),
                "feedback_type": "validation",
                "feedback_title": "Partial Body",
                "feedback_messages": [
                    "Upper body is not completely visible."
                ],
                "mistakes": ["Camera cannot see your complete posture."],
                "improvement_tips": [
                    "Sit farther back so your upper body is visible."
                ],
                "landmark_analysis": {},
            }

        elif validation_reason == "PARTIAL_HAND":
            return {
                "expected": expected,
                "predicted": predicted,
                "correct": False,
                "confidence": round(confidence, 3),
                "feedback_type": "validation",
                "feedback_title": "Partial Hand",
                "feedback_messages": ["Entire hand is not visible."],
                "mistakes": ["Some fingers are outside the frame."],
                "improvement_tips": ["Keep your full hand inside the camera."],
                "landmark_analysis": {},
            }

        # =====================================================
        # Prediction Evaluation
        # =====================================================

        # Safe extraction at root level to prevent UnboundLocalError
        gesture_stability = motion_metrics.get("gesture_stability", 100)
        time_taken = motion_metrics.get("time_taken", 0)
        consistency = motion_metrics.get("prediction_consistency", 100)

        stable = True
        unstable_frames = 0

        if stable_prediction:
            stable = stable_prediction.get("stable", True)
            unstable_frames = stable_prediction.get("unstable_frames", 0)

        # ----------------------------------------
        # Correct / Incorrect Prediction Header
        # ----------------------------------------

        if correct:
            feedback_type = "correct"

            if confidence >= 0.90:
                feedback_title = "Excellent Performance"
                feedback_messages.append(
                    "Great job! Your gesture matches perfectly."
                )
            elif confidence >= 0.75:
                feedback_title = "Good Performance"
                feedback_messages.append("Correct gesture detected.")
            else:
                feedback_title = "Correct Gesture"
                feedback_messages.append(
                    "Gesture recognised, but confidence can improve."
                )
        else:
            feedback_type = "incorrect"
            feedback_title = "Needs Improvement"

            feedback_messages.append(f"Expected gesture: {expected}")
            feedback_messages.append(f"Detected gesture: {predicted}")

            mistakes.append(f"Predicted {predicted} instead of {expected}")
            improvement_tips.append(
                f"Practice the difference between {expected} and {predicted}."
            )

        # ----------------------------------------
        # Confidence Feedback
        # ----------------------------------------

        if confidence < 0.40:
            feedback_messages.append("Prediction confidence is very low.")
            improvement_tips.append("Hold the gesture longer before releasing.")
        elif confidence < 0.60:
            feedback_messages.append("Prediction confidence is moderate.")
            improvement_tips.append("Perform the gesture more clearly.")

        # ----------------------------------------
        # Stability Feedback
        # ----------------------------------------

        if gesture_stability < 60:
            feedback_messages.append("Gesture stability is poor.")
            improvement_tips.append("Keep your hand steady.")
        elif gesture_stability < 80:
            feedback_messages.append("Minor hand movement detected.")
            improvement_tips.append("Reduce unnecessary movement.")

        # ----------------------------------------
        # Stable Detector Feedback
        # ----------------------------------------

        if not stable:
            feedback_messages.append(
                "Prediction did not remain stable long enough."
            )
            improvement_tips.append("Hold the gesture for a little longer.")

        if unstable_frames > 5:
            stable_frames = 0
            if stable_prediction:
                stable_frames = stable_prediction.get("stable_frames", 0)

            if stable_frames >= 10:
                feedback_messages.append("Excellent gesture stability.")
            elif stable_frames >= 5:
                feedback_messages.append(
                    "Gesture remained stable before recognition."
                )

            improvement_tips.append(
                "Avoid moving your fingers before prediction completes."
            )

        # ----------------------------------------
        # Time Taken Feedback
        # ----------------------------------------

        if time_taken > 5:
            feedback_messages.append("Gesture took longer than expected.")
            improvement_tips.append(
                "Try recognizing the sign more confidently."
            )
        elif 0 < time_taken < 1:
            feedback_messages.append("Gesture recognized quickly.")

        # ----------------------------------------
        # Consistency Feedback
        # ----------------------------------------

        if consistency < 60:
            feedback_messages.append(
                "Predictions changed frequently during recognition."
            )
            improvement_tips.append(
                "Hold the sign steady until recognition completes."
            )
        elif consistency < 85:
            feedback_messages.append("Minor prediction fluctuations detected.")

        # =====================================================
        # Landmark Analysis
        # =====================================================

        if landmarks:
            landmark_feedback = self.landmark_analyzer.analyze(
                expected, landmarks
            )
        else:
            landmark_feedback = {
                "status": "failed",
                "messages": [],
                "deviations": [],
            }

        # ------------------------------------------
        # Merge Landmark Feedback
        # ------------------------------------------

        landmark_messages = landmark_feedback.get("messages", [])
        landmark_deviations = landmark_feedback.get("deviations", [])

        for deviation in landmark_deviations:
            if deviation not in mistakes:
                mistakes.append(deviation)

        for message in landmark_messages:
            lower = message.lower()

            # Ignore positive landmark messages
            if (
                "correct" in lower
                or "good" in lower
                or "perfect" in lower
                or "matches" in lower
            ):
                continue

            if message not in feedback_messages:
                feedback_messages.append(message)

            if message not in improvement_tips and not correct:
                improvement_tips.append(message)

        # =====================================================
        # Gesture Rule Validation
        # =====================================================

        rule_messages = []
        rule_deviations = []

        try:
            self.rules.evaluate(
                expected, landmarks, rule_deviations, rule_messages
            )
        except Exception:
            rule_messages = []
            rule_deviations = []

        # =====================================================
        # Merge Rule Feedback
        # =====================================================

        for message in rule_messages:
            if message not in feedback_messages:
                feedback_messages.append(message)

            if message not in improvement_tips and not correct:
                improvement_tips.append(message)

        for deviation in rule_deviations:
            if deviation not in mistakes:
                mistakes.append(deviation)

        # =====================================================
        # Remove Duplicate Messages
        # =====================================================

        feedback_messages = list(dict.fromkeys(feedback_messages))
        mistakes = list(dict.fromkeys(mistakes))
        improvement_tips = list(dict.fromkeys(improvement_tips))

        # =====================================================
        # Default Feedback & Improvement Tips
        # =====================================================

        if len(feedback_messages) == 0:
            if correct:
                feedback_messages.append("Excellent! Maintain the same posture.")
            else:
                feedback_messages.append("Practice this gesture again.")

        if len(improvement_tips) == 0:
            if correct:
                if confidence >= 0.90:
                    improvement_tips.append(
                        "Excellent! Your gesture is accurate and stable."
                    )
                else:
                    improvement_tips.append(
                        "Gesture is correct. Maintain the same hand posture."
                    )
            else:
                improvement_tips.append(
                    "Repeat the gesture slowly before increasing speed."
                )

        if correct and confidence >= 0.90 and gesture_stability >= 90:
            feedback_messages.append("Excellent gesture performance!")
            improvement_tips.append("Maintain this consistency.")

        # =====================================================
        # Final Response
        # =====================================================

        return {
            "expected": expected,
            "predicted": predicted,
            "correct": correct,
            "confidence": round(confidence, 3),
            "feedback_type": feedback_type,
            "feedback_title": feedback_title,
            "feedback_messages": feedback_messages,
            "mistakes": mistakes,
            "improvement_tips": improvement_tips,
            "landmark_analysis": landmark_feedback,
            "motion_metrics": motion_metrics,
            "stable_prediction": stable_prediction,
        }