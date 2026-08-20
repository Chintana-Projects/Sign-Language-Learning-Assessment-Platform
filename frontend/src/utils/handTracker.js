import {
    FilesetResolver,
    HandLandmarker
} from "@mediapipe/tasks-vision";

let handLandmarker = null;

// ==================================================
// CREATE MEDIAPIPE HAND LANDMARKER
// ==================================================

async function createHandLandmarker() {

    if (handLandmarker) {
        return handLandmarker;
    }

    const vision =
        await FilesetResolver.forVisionTasks(
            "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm"
        );

    handLandmarker =
        await HandLandmarker.createFromOptions(
            vision,
            {
                baseOptions: {
                    modelAssetPath:
                        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
                },

                runningMode: "VIDEO",

                numHands: 1,

                minHandDetectionConfidence: 0.5,

                minHandPresenceConfidence: 0.5,

                minTrackingConfidence: 0.5
            }
        );

    return handLandmarker;
}

// ==================================================
// START WEBCAM HAND TRACKING
// ==================================================

export async function startHandTracking(
    videoElement,
    onDetection
) {

    const detector =
        await createHandLandmarker();

    let active = true;

    function detect() {

        if (!active) return;

        if (
            !videoElement ||
            videoElement.readyState !== 4 ||
            videoElement.videoWidth === 0 ||
            videoElement.videoHeight === 0
        ) {
            requestAnimationFrame(detect);
            return;
        }

        try {

            const results =
                detector.detectForVideo(
                    videoElement,
                    performance.now()
                );

            let landmarks = [];
            let handCount = 0;

            if (
                results &&
                results.landmarks &&
                results.landmarks.length > 0
            ) {

                handCount = results.landmarks.length;

                const hand =
                    results.landmarks[0];

                landmarks =
                    hand.map(point => [
                        Number(point.x),
                        Number(point.y),
                        Number(point.z)
                    ]);

                if (landmarks.length !== 21) {
                    landmarks = [];
                    handCount = 0;
                }
            }

            onDetection({

                landmarks,

                hand_count: handCount,

                // Until Pose is added,
                // assume person exists only if a hand exists.
                person_count:
                    handCount > 0 ? 1 : 0,

                body_visible:
                    handCount > 0

            });

        }

        catch (error) {

            console.warn(
                "MediaPipe detection error:",
                error
            );

            onDetection({

                landmarks: [],

                hand_count: 0,

                person_count: 0,

                body_visible: false

            });

        }

        requestAnimationFrame(detect);
    }

    detect();

    return () => {

        active = false;

    };
}