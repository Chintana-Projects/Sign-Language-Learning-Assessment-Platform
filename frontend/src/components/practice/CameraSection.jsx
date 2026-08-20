import { useState } from "react";
import WebcamCapture from "../WebcamCapture";
import "../../styles/dashboard/CameraSection.css";

export default function CameraSection({
    session,
    prediction,
    onResult
}) {
    const [checkResult, setCheckResult] = useState(null);

    return (
        <section className="camera-section">

            {/* ============================
                HEADER
            ============================ */}

            <div className="camera-header">

                <div className="camera-title">

                    <h2>📷 Live Camera</h2>

                    <p>
                        Perform the selected sign clearly inside the frame.
                    </p>

                </div>

                <div className="live-indicator">

                    <span />

                    LIVE

                </div>

            </div>


            {/* ============================
                CAMERA
            ============================ */}

            <div className="camera-wrapper">

                <WebcamCapture
                    sessionId={session?.session_id}
                    onResult={onResult}
                    onCheckResult={setCheckResult}
                />

            </div>


            {/* ===============================
                PRACTICE GUIDE / AI FEEDBACK
            =============================== */}

            <div className="camera-instructions">

                {/* ============================
                    BEFORE CHECKING
                ============================ */}

                {checkResult === null && (
                    <>
                        <div className="instruction-item">

                            <span>1</span>

                            <p>
                                Keep one hand fully visible inside the camera.
                            </p>

                        </div>

                        <div className="instruction-item">

                            <span>2</span>

                            <p>
                                Perform the sign naturally and hold it steady.
                            </p>

                        </div>

                        <div className="instruction-item">

                            <span>3</span>

                            <p>
                                Wait for AI recognition, then press{" "}
                                <b>Check Sign</b>.
                            </p>

                        </div>
                    </>
                )}


                {/* ============================
                    CORRECT FEEDBACK
                ============================ */}
{/* ============================
    CORRECT FEEDBACK
================================ */}

{checkResult === "correct" && (
    <div className="feedback-content">

        <div className="feedback-title">
            🤖 AI Feedback
        </div>

        <div className="feedback-success">
            ✓ {prediction?.feedback?.feedback_title || "Great job!"}
        </div>

        <p>
            {prediction?.feedback?.feedback_messages?.[0] ||
                "You performed the sign correctly."}
        </p>

        

        {prediction?.feedback?.improvement_tips?.length > 0 && (
            <div className="feedback-tip">

                💡 <strong>Tip:</strong>{" "}

                {prediction.feedback.improvement_tips[0]}

            </div>
        )}

    </div>
)}


{/* ============================
    INCORRECT FEEDBACK
================================ */}

{checkResult === "incorrect" && (
    <div className="feedback-content">

        <div className="feedback-title">
            🤖 AI Feedback
        </div>

        <div className="feedback-error">
            ✕ {prediction?.feedback?.feedback_title || "Needs Improvement"}
        </div>

        <div className="feedback-summary">

            <p>
                <strong>Expected:</strong>{" "}
                {prediction?.feedback?.expected || "--"}
            </p>

            <p>
                <strong>Detected:</strong>{" "}
                {prediction?.feedback?.predicted || "--"}
            </p>

            <p>
                <strong>Confidence:</strong>{" "}
                {(
                    (prediction?.feedback?.confidence || 0) * 100
                ).toFixed(1)}%
            </p>

        </div>


        {/* ============================
            WHAT WENT WRONG
        ============================ */}

        {prediction?.feedback?.mistakes?.length > 0 && (

            <div className="feedback-mistakes">

                <strong>🔍 What went wrong</strong>

                <ul>

                    {prediction.feedback.mistakes.map(
                        (mistake, index) => (

                            <li key={index}>
                                {mistake}
                            </li>

                        )
                    )}

                </ul>

            </div>

        )}


        {/* ============================
            IMPROVEMENT TIPS
        ============================ */}

        {prediction?.feedback?.improvement_tips?.length > 0 && (

            <div className="feedback-tips">

                <strong>💡 How to improve</strong>

                <ul>

                    {prediction.feedback.improvement_tips.map(
                        (tip, index) => (

                            <li key={index}>
                                {tip}
                            </li>

                        )
                    )}

                </ul>

            </div>

        )}

    </div>
)}


{/* ============================
    ERROR
================================ */}

{checkResult === "error" && (
    <div className="feedback-content">

        <div className="feedback-title">
            🤖 AI Feedback
        </div>

        <div className="feedback-error">
            ⚠ Unable to check sign
        </div>

        <p>
            Please try the sign again.
        </p>

    </div>
)}


                {/* ============================
                    INCORRECT FEEDBACK
                ============================ */}

                {checkResult === "incorrect" && (
                    <div className="feedback-content">

                        <div className="feedback-title">
                            🤖 AI Feedback
                        </div>

                        <div className="feedback-error">
                            ✕ Keep Practicing
                        </div>

                        <p>
                            {prediction?.feedback?.message ||
                                prediction?.feedback?.summary ||
                                "The sign was not recognized confidently enough."}
                        </p>

                        <div className="feedback-tip">
                            💡 Compare your hand position with the reference
                            sign and try again.
                        </div>

                    </div>
                )}


                {/* ============================
                    ERROR FEEDBACK
                ============================ */}

                {checkResult === "error" && (
                    <div className="feedback-content">

                        <div className="feedback-title">
                            🤖 AI Feedback
                        </div>

                        <div className="feedback-error">
                            ⚠ Unable to check sign
                        </div>

                        <p>
                            Please try the sign again.
                        </p>

                    </div>
                )}

            </div>

        </section>
    );
}