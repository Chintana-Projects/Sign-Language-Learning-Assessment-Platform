import React, {
    useRef,
    useEffect,
    useState
} from "react";
import RecognitionPanel from "./practice/RecognitionPanel";
import Webcam from "react-webcam";

import {
    startHandTracking
} from "../utils/handTracker";


function WebcamCapture({
    sessionId,
    
    onCheckResult,
    onResult
}) {

    const webcamRef = useRef(null);

    const trackerStartedRef = useRef(false);
    const trackerCleanupRef = useRef(null);
const signCheckedRef = useRef(false);
    const latestLandmarksRef = useRef([]);

    // Prevent overlapping frame requests
    const frameRequestInProgressRef = useRef(false);

    const lastFrameSentRef = useRef(0);

    const handLostTimerRef = useRef(null);

    const FRAME_INTERVAL = 300;
    const [
    signChecked,
    setSignChecked
] = useState(false);

const [
    checkResult,
    setCheckResult
] = useState(null);

const [
    frozenConfidence,
    setFrozenConfidence
] = useState(0);

const [
    frozenPrediction,
    setFrozenPrediction
] = useState(null);


    // ==========================================
    // STATES
    // ==========================================

    const [
        cameraReady,
        setCameraReady
    ] = useState(false);

    const [
        checking,
        setChecking
    ] = useState(false);

    const [
        realtimeResult,
        setRealtimeResult
    ] = useState(null);

    const [
        handDetected,
        setHandDetected
    ] = useState(false);


    // ==========================================
    // SEND FRAME TO BACKEND
    // ==========================================

    async function sendFrameToBackend(detection) {

        if (!sessionId) {
    return;
}

/*
 * Once Check Sign is clicked,
 * freeze the current result.
 */
if (signCheckedRef.current) {
    return;
}

        // Prevent overlapping requests
        if (frameRequestInProgressRef.current) {
            return;
        }

        const now = Date.now();

        // Limit request frequency
        if (
            now - lastFrameSentRef.current <
            FRAME_INTERVAL
        ) {
            return;
        }

        // Make sure we have exactly 21 landmarks
        if (
            !Array.isArray(detection.landmarks) ||
            detection.landmarks.length !== 21
        ) {
            return;
        }

        lastFrameSentRef.current = now;

        frameRequestInProgressRef.current = true;

        try {

            const response = await fetch(
                `http://127.0.0.1:8000/practice/${sessionId}/frame`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({

                        landmarks:
                            detection.landmarks,

                        hand_count:
                            detection.hand_count,

                        person_count:
                            detection.person_count,

                        body_visible:
                            detection.body_visible

                    })
                }
            );


            if (!response.ok) {

                throw new Error(
                    `Frame request failed: ${response.status}`
                );

            }


            const data =
                await response.json();


            // ==========================================
            // BACKEND IS AUTHORITATIVE
            // ==========================================

            setRealtimeResult(previous => ({

                ...previous,

                ...data,

                stable_prediction:
                    data.stable_prediction || {
                        stable: false,
                        prediction: null,
                        confidence: 0,
                        stable_frames: 0,
                        required_frames: 5,
                        gesture_stability: 0
                    }

            }));


            if (onResult) {
                onResult(data);
            }

        }
        catch (error) {

            console.error(
                "Frame Error:",
                error
            );

        }
        finally {

            frameRequestInProgressRef.current =
                false;

        }

    }


    // ==========================================
    // START HAND TRACKING
    // ==========================================

    useEffect(() => {


        let interval = null;

        let cancelled = false;
        setSignChecked(false);
    signCheckedRef.current = false;
    setCheckResult(null);
    setFrozenConfidence(0);
    setFrozenPrediction(null);


        async function initialiseTracker() {

            if (cancelled) {
                return;
            }


            if (
                !webcamRef.current ||
                !webcamRef.current.video
            ) {
                return;
            }


            if (
                trackerStartedRef.current
            ) {
                return;
            }


            trackerStartedRef.current = true;


            trackerCleanupRef.current =
                await startHandTracking(

                    webcamRef.current.video,

                    detection => {

                        if (cancelled) {
                            return;
                        }


                        const {
                            landmarks,
                            hand_count,
                            person_count,
                            body_visible
                        } = detection;


                        // ==========================================
                        // VALID HAND
                        // ==========================================

                        if (
                            Array.isArray(landmarks) &&
                            landmarks.length === 21
                        ) {

                            latestLandmarksRef.current =
                                landmarks;


                            // Cancel hand-lost timer
                            if (
                                handLostTimerRef.current
                            ) {

                                clearTimeout(
                                    handLostTimerRef.current
                                );

                                handLostTimerRef.current =
                                    null;

                            }


                            setHandDetected(true);


                            // ======================================
                            // SEND FRAME
                            // ======================================

                            sendFrameToBackend({

                                landmarks,
                                hand_count,
                                person_count,
                                body_visible

                            });

                        }

                        // ==========================================
                        // NO VALID HAND
                        // ==========================================

                        else {

                            latestLandmarksRef.current = [];


                            if (
                                !handLostTimerRef.current
                            ) {

                                handLostTimerRef.current =
                                    setTimeout(() => {

                                        setHandDetected(false);


                                        setRealtimeResult({

                                            prediction: null,

                                            confidence: 0,

                                            validation: {
                                                valid: false
                                            },

                                            motion_metrics: {},

                                            performance: {},

                                            stable_prediction: {

                                                stable: false,

                                                prediction: null,

                                                confidence: 0,

                                                stable_frames: 0,

                                                required_frames: 5,

                                                gesture_stability: 0

                                            }

                                        });


                                        handLostTimerRef.current =
                                            null;

                                    }, 1000);

                            }

                        }

                    }

                );

        }


        // ==========================================
        // WAIT FOR CAMERA
        // ==========================================

        interval = setInterval(() => {

            if (
                webcamRef.current &&
                webcamRef.current.video &&
                webcamRef.current.video.readyState === 4
            ) {

                setCameraReady(true);

                initialiseTracker();

                clearInterval(interval);

            }

        }, 300);


        // ==========================================
        // CLEANUP
        // ==========================================

        return () => {

            cancelled = true;


            if (interval) {
                clearInterval(interval);
            }


            if (
                trackerCleanupRef.current
            ) {

                trackerCleanupRef.current();

                trackerCleanupRef.current =
                    null;

            }


            if (
                handLostTimerRef.current
            ) {

                clearTimeout(
                    handLostTimerRef.current
                );

                handLostTimerRef.current =
                    null;

            }


            trackerStartedRef.current =
                false;


            frameRequestInProgressRef.current =
                false;


            latestLandmarksRef.current =
                [];


            lastFrameSentRef.current =
                0;

        };

    }, [sessionId]);


    // ==========================================
    // CHECK SIGN
    // ==========================================
async function checkSign() {
    if (checking || signCheckedRef.current) {
        return;
    }

    const currentResult = realtimeResult;

    const stablePrediction =
        currentResult?.stable_prediction;

    // ==========================================
    // GET PREDICTION
    // ==========================================

    const predictionAtClick =
        stablePrediction?.prediction ||
        currentResult?.prediction ||
        null;

    if (!predictionAtClick) {
        console.log("No prediction available yet.");
        return;
    }

    // ==========================================
    // GET CONFIDENCE
    // ==========================================
// ==========================================
// GET CONFIDENCE
// ==========================================

const stableRawConfidence =
    Number(stablePrediction?.confidence);

const normalRawConfidence =
    Number(currentResult?.confidence);

// Choose the usable confidence.
// If stable confidence is 0 or invalid,
// use the normal backend confidence.
let rawConfidence;

if (
    Number.isFinite(stableRawConfidence) &&
    stableRawConfidence > 0
) {
    rawConfidence = stableRawConfidence;
} else if (
    Number.isFinite(normalRawConfidence)
) {
    rawConfidence = normalRawConfidence;
} else {
    rawConfidence = 0;
}

// ==========================================
// CONVERT CONFIDENCE TO PERCENTAGE
// ==========================================

const confidenceAtClick =
    rawConfidence <= 1
        ? rawConfidence * 100
        : rawConfidence;

console.log("CONFIDENCE DEBUG");
console.log("Stable confidence:", stableRawConfidence);
console.log("Normal confidence:", normalRawConfidence);
console.log("Raw confidence used:", rawConfidence);
console.log("Percentage:", confidenceAtClick);

    // ==========================================
    // CHECK LANDMARKS
    // ==========================================

    if (
        !latestLandmarksRef.current ||
        latestLandmarksRef.current.length !== 21
    ) {
        console.log("No valid hand landmarks.");
        return;
    }

    // ==========================================
    // FREEZE IMMEDIATELY
    // ==========================================

    setFrozenPrediction(predictionAtClick);

    setFrozenConfidence(confidenceAtClick);

    setSignChecked(true);

    signCheckedRef.current = true;

    setChecking(true);

    setCheckResult("checking");


    // Copy landmarks
    const landmarksAtClick = [
        ...latestLandmarksRef.current
    ];

    console.log("================================");
    console.log("CHECK SIGN CLICKED");
    console.log("Prediction:", predictionAtClick);
    console.log("Raw confidence:", rawConfidence);
    console.log(
        "Confidence percentage:",
        confidenceAtClick
    );
    console.log("================================");

    // ==========================================
    // DETERMINE RESULT USING 60%
    // ==========================================

 

    console.log(
    "Prediction at click:",
    predictionAtClick
);

console.log(
    "Confidence:",
    confidenceAtClick
);

console.log(
    "Correctness will be determined by backend."
);

    try {

        // ==========================================
        // SEND ATTEMPT TO BACKEND
        // ==========================================

        const response = await fetch(
            `http://127.0.0.1:8000/practice/${sessionId}/attempt`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    landmarks:
                        landmarksAtClick,

                    stable_prediction: {
                        ...stablePrediction,

                        prediction:
                            predictionAtClick,

                        confidence:
                            rawConfidence
                    },

                    motion_metrics:
                        currentResult?.motion_metrics || {}
                })
            }
        );

        if (!response.ok) {
            throw new Error(
                `Attempt request failed: ${response.status}`
            );
        }

        const data =
            await response.json();

const backendCorrect = data?.assessment?.correct === true;
setCheckResult(
    backendCorrect ? "correct" : "incorrect"
);

if (onCheckResult) {
    onCheckResult(
        backendCorrect ? "correct" : "incorrect"
    );
}
        // ==========================================
        // KEEP FROZEN RESULT
        // ==========================================

        setRealtimeResult(previous => {

    const assessment =
        data?.assessment || {};

    const predicted =
        assessment?.predicted ||
        predictionAtClick ||
        "UNKNOWN";

    const assessedConfidence =
        Number.isFinite(
            Number(assessment?.confidence)
        )
            ? Number(assessment.confidence)
            : rawConfidence;

    return {

        ...(previous || {}),

        ...data,

        prediction:
            predicted,

        confidence:
            assessedConfidence,

        stable_prediction: {

            ...(stablePrediction || {}),

            prediction:
                predicted,

            confidence:
                assessedConfidence
        }
    };
});
        if (onResult) {
            onResult(data);
        }

    } catch (error) {

        console.error(
            "Assessment Error:",
            error
        );

        /*
         * The recognition was already frozen.
         * Only the backend assessment failed.
         */
        setCheckResult("error");
        if (onCheckResult) {
    onCheckResult("error");
}

    } finally {

        setChecking(false);

    }
}
function tryAgain() {
    console.log("Trying again...");

    // Unfreeze recognition
    signCheckedRef.current = false;
    setSignChecked(false);

    // Clear previous result
    setCheckResult(null);
    if (onCheckResult) {
    onCheckResult(null);
}

    // Clear frozen values
    setFrozenPrediction(null);
    setFrozenConfidence(0);

    // Allow checking again
    setChecking(false);

    // Clear old recognition result
    setRealtimeResult(null);

    // Reset timing so a new frame can be sent immediately
    lastFrameSentRef.current = 0;

    frameRequestInProgressRef.current = false;

    console.log("Recognition restarted.");
    

}
    // ==========================================
    // CURRENT BACKEND STABILITY
    // ==========================================
    // Stability is NOT displayed anymore,
    // but it is still used internally to
    // determine whether Check Sign is allowed.

    const stable =
        realtimeResult
            ?.stable_prediction
            ?.stable === true;


    const stablePrediction =
        realtimeResult
            ?.stable_prediction
            ?.prediction || null;


    const stableConfidence =
        realtimeResult
            ?.stable_prediction
            ?.confidence ?? 0;


    // ==========================================
// DISPLAY CONFIDENCE
// ==========================================

// Backend returns confidence between 0 and 1
// Convert it into percentage.



 


    // ==========================================
    // RENDER
    // ==========================================

   return (
    <div className="webcam-capture">

 


        {/* CAMERA AREA */}
        <div className="webcam-frame">

            {/* HAND STATUS */}
            <div
                className={
                    `camera-status ${
                        handDetected
                            ? "detected"
                            : "not-detected"
                    }`
                }
            >

                <span className="status-dot"></span>

                {!cameraReady
                    ? "Camera Initializing"
                    : handDetected
                        ? "Hand Detected"
                        : "No Hand Detected"
                }

            </div>


            {/* WEBCAM */}
            <Webcam
                ref={webcamRef}
                audio={false}
                width={640}
                height={480}
                videoConstraints={{
                    facingMode: "user"
                }}
                className="webcam-video"
            />

        </div>


        {/* AI RECOGNITION — OUTSIDE CAMERA */}
     <RecognitionPanel
    handDetected={handDetected}

    prediction={
        signChecked
            ? frozenPrediction
            : realtimeResult?.prediction
    }

    confidence={
        signChecked
            ? frozenConfidence
            : (
                handDetected
                    ? (
                        stable
                            ? stableConfidence * 100
                            : (realtimeResult?.confidence ?? 0) * 100
                    )
                    : 0
            )
    }

    checking={checking}

    checkResult={checkResult}

    onCheck={checkSign}

    onTryAgain={tryAgain}

    disabled={
        checking ||
        signChecked ||
        !handDetected
    }
/>


        

    </div>
);

         

}


export default WebcamCapture;