import cv2
import mediapipe as mp


class HandDetector:

    def __init__(
        self,
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ):

        # -------------------------------
        # MediaPipe Hands
        # -------------------------------

        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

        # -------------------------------
        # MediaPipe Pose
        # -------------------------------

        self.mp_pose = mp.solutions.pose

        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    # ==================================================
    # Detect Hands + Pose
    # ==================================================

    def detect(self, frame):

        if frame is None:

            return {
                "frame": None,
                "hand_count": 0,
                "person_count": 0,
                "body_visible": False,
                "landmarks": []
            }

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # --------------------------------------
        # Run Hand Detection
        # --------------------------------------

        hand_results = self.hands.process(rgb)

        # --------------------------------------
        # Run Pose Detection
        # --------------------------------------

        pose_results = self.pose.process(rgb)

        hand_count = 0
        landmark_data = []

        person_count = 0
        body_visible = False

        # --------------------------------------
        # Person Detection
        # --------------------------------------

        if pose_results.pose_landmarks:

            person_count = 1

            pose_landmarks = pose_results.pose_landmarks.landmark

            required_points = [
                self.mp_pose.PoseLandmark.LEFT_SHOULDER,
                self.mp_pose.PoseLandmark.RIGHT_SHOULDER,
                self.mp_pose.PoseLandmark.LEFT_ELBOW,
                self.mp_pose.PoseLandmark.RIGHT_ELBOW,
            ]

            visible_count = 0

            for point in required_points:

                landmark = pose_landmarks[point.value]

                if landmark.visibility > 0.5:
                    visible_count += 1

            body_visible = visible_count >= 3

        # --------------------------------------
        # Hand Detection
        # --------------------------------------

        if hand_results.multi_hand_landmarks:

            hand_count = len(hand_results.multi_hand_landmarks)

            for hand_landmarks in hand_results.multi_hand_landmarks:

                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

                points = []

                for lm in hand_landmarks.landmark:

                    points.append([
                        float(lm.x),
                        float(lm.y),
                        float(lm.z)
                    ])

                landmark_data.append(points)

        return {
            "frame": frame,
            "hand_count": hand_count,
            "person_count": person_count,
            "body_visible": body_visible,
            "landmarks": landmark_data
        }

    # ==================================================
    # Cleanup
    # ==================================================

    def close(self):

        self.hands.close()
        self.pose.close()