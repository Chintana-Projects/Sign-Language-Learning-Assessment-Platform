
import React from "react";


// =====================================
// Confidence Formatter
// =====================================

function formatConfidence(value) {

    let confidence =
        Number(value ?? 0);

    if (confidence <= 1) {

        confidence =
            confidence * 100;

    }

    return Math.max(
        0,
        Math.min(
            confidence,
            100
        )
    );

}


// =====================================
// Gesture Feedback
// =====================================

function GestureFeedback({
    feedback = []
}) {


    // =====================================
    // Normalize Data
    // =====================================

    const feedbackList =
        Array.isArray(feedback)
            ? feedback
            : [];


    // =====================================
    // No Feedback
    // =====================================

    if (feedbackList.length === 0) {

        return (

            <div className="card feedback-box">

                <h2>
                    🖐 Gesture Feedback
                </h2>

                <p>
                    No gesture feedback available.
                </p>

            </div>

        );

    }


    // =====================================
    // Render
    // =====================================

    return (

        <div className="card feedback-box">

            <h2>
                🖐 Gesture Feedback
            </h2>


            {
                feedbackList.map(
                    (item, index) => {


                        // =================================
                        // Feedback Messages
                        // =================================

                        let messages = [];


                        if (
                            Array.isArray(
                                item?.feedback
                            )
                        ) {

                            messages =
                                item.feedback;

                        }

                        else if (
                            Array.isArray(
                                item?.feedback?.feedback_messages
                            )
                        ) {

                            messages =
                                item.feedback.feedback_messages;

                        }


                        // =================================
                        // Mistakes
                        // =================================

                        let mistakes =
                            item?.mistakes
                            ??
                            item?.feedback?.mistakes
                            ??
                            [];


                        if (!Array.isArray(mistakes)) {

                            mistakes =
                                [mistakes];

                        }


                        // =================================
                        // Improvement Tips
                        // =================================

                        let tips =
                            item?.tips
                            ??
                            item?.feedback?.improvement_tips
                            ??
                            [];


                        if (!Array.isArray(tips)) {

                            tips =
                                [tips];

                        }


                        // =================================
                        // Confidence
                        // =================================

                        const confidence =
                            formatConfidence(
                                item?.confidence
                            );


                        // =================================
                        // Correct Status
                        // =================================

                        const isCorrect =
                            Boolean(
                                item?.correct
                            );


                        // =================================
                        // Render Attempt
                        // =================================

                        return (

                            <div

                                key={index}

                                className={
                                    isCorrect
                                        ? "correct-feedback"
                                        : "incorrect-feedback"
                                }

                            >

                                {/* =========================
                                    ATTEMPT
                                ========================= */}

                                <h3>

                                    Attempt {index + 1}

                                </h3>


                                {/* =========================
                                    EXPECTED
                                ========================= */}

                                <p>

                                    <strong>
                                        Expected:
                                    </strong>

                                    {" "}

                                    {
                                        item?.expected
                                        ??
                                        "Unknown"
                                    }

                                </p>


                                {/* =========================
                                    DETECTED
                                ========================= */}

                                <p>

                                    <strong>
                                        Detected:
                                    </strong>

                                    {" "}

                                    {
                                        item?.predicted
                                        ??
                                        item?.prediction
                                        ??
                                        "Unknown"
                                    }

                                </p>


                                {/* =========================
                                    CONFIDENCE
                                ========================= */}

                                <p>

                                    <strong>
                                        Confidence:
                                    </strong>

                                    {" "}

                                    {
                                        confidence.toFixed(2)
                                    }%

                                </p>


                                {/* =========================
                                    STATUS
                                ========================= */}

                                <p>

                                    <strong>
                                        Status:
                                    </strong>

                                    {" "}

                                    {
                                        isCorrect
                                            ? "✅ Correct Gesture"
                                            : "❌ Needs Improvement"
                                    }

                                </p>


                                {/* =========================
                                    FEEDBACK MESSAGES
                                ========================= */}

                                {
                                    messages.length > 0 && (

                                        <div className="feedback-messages">

                                            <h4>
                                                💡 Feedback
                                            </h4>

                                            <ul>

                                                {
                                                    messages.map(
                                                        (
                                                            message,
                                                            messageIndex
                                                        ) => (

                                                            <li
                                                                key={
                                                                    messageIndex
                                                                }
                                                            >

                                                                {
                                                                    typeof message === "string"
                                                                        ? message
                                                                        : JSON.stringify(
                                                                            message
                                                                        )
                                                                }

                                                            </li>

                                                        )
                                                    )
                                                }

                                            </ul>

                                        </div>

                                    )
                                }


                                {/* =========================
                                    MISTAKES
                                ========================= */}

                                {
                                    mistakes.length > 0 && (

                                        <div className="feedback-mistakes">

                                            <h4>
                                                ⚠ Mistakes Detected
                                            </h4>

                                            <ul>

                                                {
                                                    mistakes.map(
                                                        (
                                                            mistake,
                                                            mistakeIndex
                                                        ) => (

                                                            <li
                                                                key={
                                                                    mistakeIndex
                                                                }
                                                            >

                                                                {
                                                                    typeof mistake === "string"
                                                                        ? mistake
                                                                        : JSON.stringify(
                                                                            mistake
                                                                        )
                                                                }

                                                            </li>

                                                        )
                                                    )
                                                }

                                            </ul>

                                        </div>

                                    )
                                }


                                {/* =========================
                                    IMPROVEMENT TIPS
                                ========================= */}

                                {
                                    tips.length > 0 && (

                                        <div className="feedback-tips">

                                            <h4>
                                                🚀 Improvement Tips
                                            </h4>

                                            <ul>

                                                {
                                                    tips.map(
                                                        (
                                                            tip,
                                                            tipIndex
                                                        ) => (

                                                            <li
                                                                key={
                                                                    tipIndex
                                                                }
                                                            >

                                                                {
                                                                    typeof tip === "string"
                                                                        ? tip
                                                                        : JSON.stringify(
                                                                            tip
                                                                        )
                                                                }

                                                            </li>

                                                        )
                                                    )
                                                }

                                            </ul>

                                        </div>

                                    )
                                }

                            </div>

                        );

                    }
                )
            }

        </div>

    );

}


export default GestureFeedback;

