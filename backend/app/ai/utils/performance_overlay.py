import cv2


class PerformanceOverlay:

    def draw(self, frame, result):

        if frame is None:
            return None

        fps = result["performance"]["fps"]
        latency = result["performance"]["latency_ms"]

        prediction = result.get("prediction")
        confidence = result.get("confidence", 0)

        stable = result.get("stable", False)
        stable_frames = result.get("stable_frames", 0)

        validation = result.get("validation", {})

        # -------------------------------
        # FPS
        # -------------------------------

        cv2.putText(
            frame,
            f"FPS: {fps}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        # -------------------------------
        # Latency
        # -------------------------------

        cv2.putText(
            frame,
            f"Latency: {latency} ms",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )

        # -------------------------------
        # Prediction
        # -------------------------------

        if prediction:

            cv2.putText(
                frame,
                f"Prediction: {prediction}",
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Confidence: {confidence*100:.1f}%",
                (10, 130),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 200, 255),
                2
            )

        # -------------------------------
        # Stable Gesture
        # -------------------------------

        color = (0, 255, 0) if stable else (0, 0, 255)

        cv2.putText(
            frame,
            f"Stable: {stable}",
            (10, 170),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

        cv2.putText(
            frame,
            f"Stable Frames: {stable_frames}",
            (10, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

        # -------------------------------
        # Validation Status
        # -------------------------------

        reason = validation.get("reason", "UNKNOWN")

        cv2.putText(
            frame,
            f"Validation: {reason}",
            (10, 240),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        return frame