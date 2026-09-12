import { useLocation, useNavigate } from "react-router-dom";
import { useState, useRef, useEffect } from "react";
import Webcam from "react-webcam";
import { startHandTracking } from "../utils/handTracker";

export default function CertificationSession() {

    const location = useLocation();
    const navigate = useNavigate();

    const certificationId =
        location.state?.certification_id;

    const [currentLetter, setCurrentLetter] =
        useState(
            location.state?.current_letter || "A"
        );

    const [progress, setProgress] =
        useState(
            location.state?.progress || 0
        );

    const [loading, setLoading] =
        useState(false);

    const [handDetected, setHandDetected] =
        useState(false);

    const [cameraReady, setCameraReady] =
        useState(false);

    const [stablePrediction, setStablePrediction] =
        useState(null);

    const webcamRef = useRef(null);

    const trackerStartedRef = useRef(false);
    const trackerCleanupRef = useRef(null);

    const frameRequestInProgressRef =
        useRef(false);

    const lastFrameSentRef =
        useRef(0);

    const FRAME_INTERVAL = 300;

    // ==========================================
    // SEND FRAME
    // ==========================================

    async function sendFrameToBackend(
        detection
    ) {

        if (!certificationId) {
            return;
        }

        if (
            frameRequestInProgressRef.current
        ) {
            return;
        }

        const now = Date.now();

        if (
            now -
                lastFrameSentRef.current <
            FRAME_INTERVAL
        ) {
            return;
        }

        lastFrameSentRef.current = now;

        frameRequestInProgressRef.current =
            true;

        try {

            const response =
                await fetch(
                    `http://127.0.0.1:8000/certification/${certificationId}/frame`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
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

            const data =
                await response.json();

            if (
                data?.stable_prediction
            ) {

                setStablePrediction(
                    data.stable_prediction
                );

            }

        } catch (error) {

            console.error(
                "Frame Error:",
                error
            );

        } finally {

            frameRequestInProgressRef.current =
                false;

        }

    }

    // ==========================================
    // START TRACKER
    // ==========================================

    useEffect(() => {

        let interval = null;
        let cancelled = false;

        async function initialiseTracker() {

            if (
                cancelled ||
                trackerStartedRef.current
            ) {
                return;
            }

            if (
                !webcamRef.current ||
                !webcamRef.current.video
            ) {
                return;
            }

            trackerStartedRef.current =
                true;

            trackerCleanupRef.current =
                await startHandTracking(

                    webcamRef.current.video,

                    detection => {

                        if (cancelled) {
                            return;
                        }

                        const {
                            landmarks
                        } = detection;

                        if (
                            Array.isArray(
                                landmarks
                            ) &&
                            landmarks.length === 21
                        ) {

                            setHandDetected(
                                true
                            );

                            sendFrameToBackend(
                                detection
                            );

                        } else {

                            setHandDetected(
                                false
                            );

                        }

                    }

                );

        }

        interval = setInterval(() => {

            if (
                webcamRef.current &&
                webcamRef.current.video &&
                webcamRef.current.video
                    .readyState === 4
            ) {

                setCameraReady(true);

                initialiseTracker();

                clearInterval(
                    interval
                );

            }

        }, 300);

        return () => {

            cancelled = true;

            if (interval) {
                clearInterval(
                    interval
                );
            }

            if (
                trackerCleanupRef.current
            ) {

                trackerCleanupRef.current();

            }

            trackerStartedRef.current =
                false;

        };

    }, [certificationId]);

    // ==========================================
    // CAPTURE SIGN
    // ==========================================

    const handleCaptureSign =
        async () => {

            if (
                !stablePrediction?.prediction
            ) {

                alert(
                    "No stable sign detected yet."
                );

                return;
            }

            try {

                setLoading(true);

                const response =
                    await fetch(
                        `http://127.0.0.1:8000/certification/${certificationId}/submit?predicted_letter=${stablePrediction.prediction}&confidence=${stablePrediction.confidence}`,
                        {
                            method: "POST"
                        }
                    );

                const data =
                    await response.json();

                console.log(
                    "Certification Response:",
                    data
                );

                if (!data.success) {

                    alert(
                        data.message ||
                        "Unable to process sign."
                    );

                    return;
                }

                // ==========================
                // COMPLETED
                // ==========================

               if (data.completed) {

    navigate(
        "/dashboard/certification/result",
        {
            state: {
                score: data.score,

                passed: data.passed,

                results: data.results,

                certificate_id:
                    data.certificate_id
            }
        }
    );

    return;
}

                // ==========================
                // NEXT LETTER
                // ==========================

                setCurrentLetter(
                    data.current_letter
                );

                setProgress(
                    data.progress
                );

                setStablePrediction(
                    null
                );

            } catch (error) {

                console.error(
                    "Capture Error:",
                    error
                );

                alert(
                    "Unable to capture sign."
                );

            } finally {

                setLoading(false);

            }

        };

    // ==========================================
    // UI
    // ==========================================

  return (
    <div
        style={{
            height: "100vh",
            padding: "20px",
            boxSizing: "border-box",
            overflow: "hidden",
            background: "#f5f7fb"
        }}
    >
        {/* HEADER */}
        <div
            style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: "15px"
            }}
        >
            <h2
                style={{
                    margin: 0,
                    color: "#1e293b"
                }}
            >
                Certification Assessment
            </h2>

            <div>
                <strong>
                    Progress: {progress}/26
                </strong>

                <span
                    style={{
                        marginLeft: "20px",
                        color: "#2563eb",
                        fontWeight: 600
                    }}
                >
                    {!cameraReady
                        ? "Initializing Camera"
                        : handDetected
                        ? "Hand Detected"
                        : "No Hand Detected"}
                </span>
            </div>
        </div>

        {/* MAIN LAYOUT */}
        <div
            style={{
                display: "flex",
                gap: "20px",
                height: "calc(100vh - 120px)"
            }}
        >
            {/* LEFT PANEL */}
            <div
                style={{
                    width: "320px",
                    display: "flex",
                    flexDirection: "column",
                    gap: "20px"
                }}
            >
                {/* LETTER */}
                <div
                    style={{
                        background: "#fff",
                        borderRadius: "20px",
                        height: "250px",
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center",
                        boxShadow:
                            "0 4px 12px rgba(0,0,0,0.08)"
                    }}
                >
                    <h1
                        style={{
                            fontSize: "150px",
                            margin: 0,
                            color: "#4f46e5"
                        }}
                    >
                        {currentLetter}
                    </h1>
                </div>

                {/* DETECTION */}
                <div
                    style={{
                        flex: 1,
                        background: "#fff",
                        borderRadius: "20px",
                        padding: "20px",
                        display: "flex",
                        flexDirection: "column",
                        justifyContent: "space-between",
                        boxShadow:
                            "0 4px 12px rgba(0,0,0,0.08)"
                    }}
                >
                    <div>
                        <h3>
                            Detected:
                            {" "}
                            {stablePrediction?.prediction || "-"}
                        </h3>

                        <p>
                            Confidence:
                            {" "}
                            {(
                                Number(
                                    stablePrediction?.confidence || 0
                                ) * 100
                            ).toFixed(1)}
                            %
                        </p>
                    </div>

                    <div>
                        <button
                            onClick={handleCaptureSign}
                            disabled={
                                loading ||
                                !handDetected ||
                                !stablePrediction?.stable
                            }
                            style={{
                                width: "100%",
                                padding: "15px",
                                border: "none",
                                borderRadius: "12px",
                                background:
                                    "linear-gradient(135deg,#2563eb,#7c3aed)",
                                color: "#fff",
                                fontSize: "18px",
                                fontWeight: "600",
                                cursor: "pointer"
                            }}
                        >
                            {loading
                                ? "Processing..."
                                : "Capture Sign"}
                        </button>

                        <div
                            style={{
                                display: "flex",
                                gap: "10px",
                                marginTop: "10px"
                            }}
                        >
                            <button
                                style={{
                                    flex: 1,
                                    padding: "12px",
                                    borderRadius: "10px",
                                    border: "none"
                                }}
                            >
                                Skip
                            </button>

                            <button
                                onClick={() => navigate(-1)}
                                style={{
                                    flex: 1,
                                    padding: "12px",
                                    borderRadius: "10px",
                                    border: "none",
                                    background: "#ef4444",
                                    color: "#fff"
                                }}
                            >
                                Exit
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {/* CAMERA PANEL */}
            <div
                style={{
                    flex: 1,
                    background: "#fff",
                    borderRadius: "20px",
                    padding: "10px",
                    boxShadow:
                        "0 4px 12px rgba(0,0,0,0.08)"
                }}
            >
                <Webcam
                    ref={webcamRef}
                    audio={false}
                    style={{
                        width: "100%",
                        height: "100%",
                        objectFit: "cover",
                        borderRadius: "15px"
                    }}
                />
            </div>
        </div>
    </div>
);

}