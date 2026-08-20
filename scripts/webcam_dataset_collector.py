import os
import cv2
import mediapipe as mp
import numpy as np

# =====================================================
# CONFIGURATION
# =====================================================

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SAVE_ROOT = os.path.join(PROJECT_ROOT, "datasets", "custom_webcam")

LETTERS = [chr(i) for i in range(ord("A"), ord("Z") + 1)]

TARGET_IMAGES = 300

IMAGE_SIZE = 224

PADDING = 35

SAVE_EVERY_N_FRAMES = 4

BLUR_THRESHOLD = 120

# =====================================================
# CREATE FOLDERS
# =====================================================

for letter in LETTERS:
    os.makedirs(os.path.join(SAVE_ROOT, letter), exist_ok=True)

# =====================================================
# MEDIAPIPE
# =====================================================

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
)

# =====================================================
# CAMERA
# =====================================================

cap = cv2.VideoCapture(0)

current_letter = 0

collect = True

frame_counter = 0

print("\nSignSync Dataset Collector Started\n")

# =====================================================
# LOOP
# =====================================================

while cap.isOpened():

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    letter = LETTERS[current_letter]

    save_folder = os.path.join(SAVE_ROOT, letter)

    saved = len([f for f in os.listdir(save_folder) if f.endswith(".jpg")])

    hand_detected = False

    blur_score = 0

    if results.multi_hand_landmarks:

        hand_detected = True

        h, w, _ = frame.shape

        for hand in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS
            )

            xs = []
            ys = []

            for lm in hand.landmark:

                xs.append(int(lm.x * w))
                ys.append(int(lm.y * h))

            x1 = max(min(xs) - PADDING, 0)
            y1 = max(min(ys) - PADDING, 0)

            x2 = min(max(xs) + PADDING, w)
            y2 = min(max(ys) + PADDING, h)

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2,
            )

            crop = frame[y1:y2, x1:x2]

            if crop.size != 0:

                blur_score = cv2.Laplacian(
                    cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY),
                    cv2.CV_64F,
                ).var()

                crop = cv2.resize(
                    crop,
                    (IMAGE_SIZE, IMAGE_SIZE),
                )

                frame_counter += 1

                if (
                    collect
                    and saved < TARGET_IMAGES
                    and blur_score > BLUR_THRESHOLD
                    and frame_counter % SAVE_EVERY_N_FRAMES == 0
                ):

                    filename = os.path.join(
                        save_folder,
                        f"{saved+1}.jpg"
                    )

                    cv2.imwrite(filename, crop)

                    saved += 1

    progress = int((saved / TARGET_IMAGES) * 20)

    bar = "█" * progress + "░" * (20 - progress)

    cv2.putText(
        frame,
        f"Letter : {letter}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2,
    )

    cv2.putText(
        frame,
        f"Saved : {saved}/{TARGET_IMAGES}",
        (20, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        frame,
        f"Hand : {'YES' if hand_detected else 'NO'}",
        (20, 105),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0) if hand_detected else (0, 0, 255),
        2,
    )

    cv2.putText(
        frame,
        f"Blur : {blur_score:.1f}",
        (20, 140),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2,
    )

    cv2.putText(
        frame,
        bar,
        (20, 175),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2,
    )

    cv2.putText(
        frame,
        "SPACE = Next Letter",
        (20, 210),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        frame,
        "Q = Quit",
        (20, 240),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
    )

    if saved >= TARGET_IMAGES:

        collect = False

        cv2.putText(
            frame,
            "LETTER COMPLETE!",
            (300, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            3,
        )

    cv2.imshow("SignSync Dataset Collector", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord(" "):

        if current_letter < len(LETTERS) - 1:

            current_letter += 1

            collect = True

            frame_counter = 0

    elif key == ord("q"):

        break

cap.release()

cv2.destroyAllWindows()