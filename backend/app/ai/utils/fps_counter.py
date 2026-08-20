import time
from collections import deque


class FPSCounter:
    """
    SignSync FPS Counter

    Purpose:
    --------
    Measures real-time processing speed.

    Used for:
    - Webcam processing
    - MediaPipe inference
    - ML prediction pipeline


    Features:
    ---------
    ✔ Real-time FPS calculation
    ✔ Smooth average FPS
    ✔ Frame counting
    ✔ Processing latency measurement
    """



    def __init__(self, buffer_size=30):

        # Store timestamps of recent frames
        self.timestamps = deque(
            maxlen=buffer_size
        )


        # Total processed frames

        self.frame_count = 0



        # Last frame start time

        self.start_time = None



        # Last latency

        self.last_latency = 0






    # ==========================================
    # Start Frame Timer
    # ==========================================

    def start(self):

        self.start_time = time.time()






    # ==========================================
    # End Frame Timer
    # ==========================================

    def update(self):

        current_time = time.time()


        self.frame_count += 1



        # Save timestamp

        self.timestamps.append(
            current_time
        )



        # Calculate latency

        if self.start_time:


            self.last_latency = (

                current_time

                -

                self.start_time

            ) * 1000



        self.start_time = None






    # ==========================================
    # Calculate FPS
    # ==========================================

    def get_fps(self):


        if len(self.timestamps) < 2:

            return 0



        time_difference = (

            self.timestamps[-1]

            -

            self.timestamps[0]

        )



        if time_difference == 0:

            return 0



        fps = (

            len(self.timestamps)-1

        ) / time_difference



        return round(
            fps,
            2
        )






    # ==========================================
    # Processing Latency
    # ==========================================

    def get_latency(self):


        return round(

            self.last_latency,

            2

        )






    # ==========================================
    # Statistics
    # ==========================================

    def get_stats(self):


        return {


            "fps":

                self.get_fps(),



            "latency_ms":

                self.get_latency(),



            "frames_processed":

                self.frame_count

        }







    # ==========================================
    # Reset
    # ==========================================

    def reset(self):


        self.timestamps.clear()


        self.frame_count = 0


        self.start_time = None


        self.last_latency = 0







# ==========================================
# Test
# ==========================================

if __name__ == "__main__":


    fps = FPSCounter()



    for i in range(10):

        fps.start()


        time.sleep(0.05)


        fps.update()



        print(
            fps.get_stats()
        )