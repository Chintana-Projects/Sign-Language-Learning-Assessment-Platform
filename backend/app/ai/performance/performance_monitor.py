import time


class PerformanceMonitor:
    """
    Monitors real-time performance of the SignSync pipeline.

    Tracks:
    - Processing FPS
    - Inference latency
    - Stable prediction confidence
    """

    def __init__(self):

        self.start_time = time.time()

        self.last_frame_time = None

        self.frame_count = 0

        self.current_fps = 0.0

        self.average_fps = 0.0

        self.inference_latency = 0.0

        self.stable_confidence = 0.0

    # ===========================================
    # Call once for every processed frame
    # ===========================================

    def update_frame(self):

        now = time.time()

        self.frame_count += 1

        if self.last_frame_time is not None:

            delta = now - self.last_frame_time

            if delta > 0:

                self.current_fps = round(1.0 / delta, 2)

        self.last_frame_time = now

        elapsed = now - self.start_time

        if elapsed > 0:

            self.average_fps = round(
                self.frame_count / elapsed,
                2
            )

    # ===========================================
    # Save inference latency
    # ===========================================

    def update_latency(self, latency):

        self.inference_latency = round(
            float(latency),
            4
        )

    # ===========================================
    # Save stable confidence
    # ===========================================

    def update_confidence(self, confidence):

        self.stable_confidence = round(
            float(confidence),
            4
        )

    # ===========================================
    # Return all performance metrics
    # ===========================================

    def get_metrics(self):

        return {

            "current_fps": self.current_fps,

            "average_fps": self.average_fps,

            "inference_latency": self.inference_latency,

            "stable_confidence": self.stable_confidence,

            "frames_processed": self.frame_count

        }

    # ===========================================
    # Reset monitor
    # ===========================================

    def reset(self):

        self.start_time = time.time()

        self.last_frame_time = None

        self.frame_count = 0

        self.current_fps = 0.0

        self.average_fps = 0.0

        self.inference_latency = 0.0

        self.stable_confidence = 0.0