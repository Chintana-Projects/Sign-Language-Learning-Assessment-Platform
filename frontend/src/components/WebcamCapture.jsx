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


    // ==========================================
    // CHECK / RESULT STATES
    // ==========================================

    const [
        signChecked,
        setSignChecked
    ] = useState(false);

    const [
        checkResult,
        setCheckResult
    ] = useState(null);

    const [
        signAccuracy,
        setSignAccuracy
    ] = useState(0);

    const [
        frozenConfidence,
        setFrozenConfidence
    ] = useState(0);

    const [
        frozenPrediction,
        setFrozenPrediction
    ] = useState(null);


    // ==========================================
    // GENERAL STATES
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

                ...(previous || {}),

                ...data,

                stable_prediction:
                    data.stable_prediction || {
                        stable: false,
                        prediction: null,
                        confidence: 0,
                        stable_frames: 0,
                        required_frames: 3,
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


        // Reset states when session changes
        setSignChecked(false);

        signCheckedRef.current = false;

        setCheckResult(null);

        setSignAccuracy(0);

        setFrozenConfidence(0);

        setFrozenPrediction(null);

        setRealtimeResult(null);

        setHandDetected(false);

        setCameraReady(false);


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

                                                required_frames: 3,

                                                gesture_stability: 0,

                                                majority_prediction: null,

                                                majority_ratio: 0,

                                                last_stable_prediction: null,

                                                new_stable: false

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

        if (
            checking ||
            signCheckedRef.current
        ) {
            return;
        }


        const currentResult =
            realtimeResult;


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

            console.log(
                "No prediction available yet."
            );

            return;

        }


        // ==========================================
        // GET CONFIDENCE
        // ==========================================

        const stableRawConfidence =
            Number(
                stablePrediction?.confidence
            );


        const normalRawConfidence =
            Number(
                currentResult?.confidence
            );


        let rawConfidence;


        if (
            Number.isFinite(
                stableRawConfidence
            ) &&
            stableRawConfidence > 0
        ) {

            rawConfidence =
                stableRawConfidence;

        }
        else if (
            Number.isFinite(
                normalRawConfidence
            )
        ) {

            rawConfidence =
                normalRawConfidence;

        }
        else {

            rawConfidence = 0;

        }


        // ==========================================
        // CONVERT CONFIDENCE TO PERCENTAGE
        // ==========================================

        const confidenceAtClick =
            rawConfidence <= 1
                ? rawConfidence * 100
                : rawConfidence;


        // ==========================================
        // CHECK LANDMARKS
        // ==========================================

        if (
            !latestLandmarksRef.current ||
            latestLandmarksRef.current.length !== 21
        ) {

            console.log(
                "No valid hand landmarks."
            );

            return;

        }


        // ==========================================
        // FREEZE RECOGNITION
        // ==========================================

        setFrozenPrediction(
            predictionAtClick
        );

        setFrozenConfidence(
            confidenceAtClick
        );

        setSignChecked(true);

        signCheckedRef.current = true;

        setChecking(true);

        setCheckResult("checking");


        // Copy landmarks
        const landmarksAtClick = [
            ...latestLandmarksRef.current
        ];


        // ==========================================
        // SEND ATTEMPT TO BACKEND
        // ==========================================

        try {

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

                            ...(stablePrediction || {}),

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


            // ==========================================
            // BACKEND ASSESSMENT
            // ==========================================

            const assessment =
                data?.assessment || {};


            const signScore =
                data?.sign_score || {};


            // ==========================================
            // GET ACTUAL SIGN SCORE
            // ==========================================
            //
            // Backend returns:
            //
            // sign_score:
            // {
            //     overall_score: ...
            // }
            //
            // Therefore use overall_score.
            //

            const backendScore =
                Number(
                    signScore?.overall_score ?? 0
                );


            const safeAccuracy =
                Math.min(
                    Math.max(
                        Number.isFinite(backendScore)
                            ? backendScore
                            : 0,
                        0
                    ),
                    100
                );


            // ==========================================
            // STORE ACTUAL SCORE
            // ==========================================

            setSignAccuracy(
                safeAccuracy
            );


            // ==========================================
            // DETERMINE CORRECT / INCORRECT
            // ==========================================
            //
            // Backend is authoritative.
            //

            const backendCorrect =
                assessment?.correct === true;


            const finalResult =
                backendCorrect
                    ? "correct"
                    : "incorrect";


            setCheckResult(
                finalResult
            );


            if (onCheckResult) {

                onCheckResult(
                    finalResult
                );

            }


            // ==========================================
            // KEEP FROZEN RESULT
            // ==========================================

            setRealtimeResult(previous => {

                const predicted =
                    assessment?.predicted ||
                    predictionAtClick ||
                    "UNKNOWN";


                const assessedConfidence =
                    Number.isFinite(
                        Number(
                            assessment?.confidence
                        )
                    )
                        ? Number(
                            assessment.confidence
                        )
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


        }
        catch (error) {

            console.error(
                "Assessment Error:",
                error
            );


            /*
             * Recognition was already frozen.
             * Only the backend assessment failed.
             */

            setCheckResult("error");

            setSignAccuracy(0);


            if (onCheckResult) {

                onCheckResult(
                    "error"
                );

            }

        }
        finally {

            setChecking(false);

        }

    }


    // ==========================================
    // TRY AGAIN
    // ==========================================

    function tryAgain() {

        // Unfreeze recognition
        signCheckedRef.current =
            false;

        setSignChecked(false);


        // Clear previous result
        setCheckResult(null);


        if (onCheckResult) {

            onCheckResult(
                null
            );

        }


        // Clear accuracy
        setSignAccuracy(0);


        // Clear frozen values
        setFrozenPrediction(null);

        setFrozenConfidence(0);


        // Allow checking again
        setChecking(false);


        // Clear old recognition result
        setRealtimeResult(null);


        // Reset timing so a new frame
        // can be sent immediately
        lastFrameSentRef.current =
            0;


        frameRequestInProgressRef.current =
            false;

    }


    // ==========================================
    // CURRENT BACKEND STABILITY
    // ==========================================

    const stable =
        realtimeResult
            ?.stable_prediction
            ?.stable === true;


    const stableConfidence =
        realtimeResult
            ?.stable_prediction
            ?.confidence ?? 0;


    // ==========================================
    // RENDER
    // ==========================================

    return (

        <div className="webcam-capture">


            {/* ==========================================
                CAMERA AREA
            ========================================== */}

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

                    <span className="status-dot">
                    </span>


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


            {/* ==========================================
                AI RECOGNITION
            ========================================== */}

            <RecognitionPanel

                handDetected={
                    handDetected
                }


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

                                        : (
                                            realtimeResult?.confidence ?? 0
                                        ) * 100

                                )

                                : 0

                        )

                }


                accuracy={
                    signAccuracy
                }


                checking={
                    checking
                }


                checkResult={
                    checkResult
                }


                onCheck={
                    checkSign
                }


                onTryAgain={
                    tryAgain
                }


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