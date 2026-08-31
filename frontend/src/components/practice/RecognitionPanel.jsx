import "../../styles/dashboard/RecognitionPanel.css";

export default function RecognitionPanel({
    handDetected,
    prediction,
    confidence,
    accuracy,
    checking,
    checkResult,
    onCheck,
    onTryAgain,
    disabled
}) {

    // ==========================================
    // SAFE CONFIDENCE
    // ==========================================

    const safeConfidence = Math.min(
        Math.max(
            Number(confidence) || 0,
            0
        ),
        100
    );

    // ==========================================
    // SAFE ACCURACY
    // ==========================================

    const safeAccuracy = Math.min(
        Math.max(
            Number(accuracy) || 0,
            0
        ),
        100
    );

    return (
        <div className="recognition-panel">

            {/* ==========================================
                HEADER
            ========================================== */}

            <div className="recognition-header">

                <div>

                    <span className="recognition-label">
                        AI Recognition
                    </span>

                    <h3>
                        {checkResult === "correct"
                            ? "Sign verified"

                            : checkResult === "incorrect"
                                ? "Sign checked"

                                : checking
                                    ? "Checking sign..."

                                    : handDetected
                                        ? "Hand detected"
                                        : "Show your hand"
                        }
                    </h3>

                </div>


                <div
                    className={
                        checkResult === "correct"
                            ? "recognition-status correct"

                            : checkResult === "incorrect"
                                ? "recognition-status incorrect"

                                : handDetected
                                    ? "recognition-status detected"

                                    : "recognition-status waiting"
                    }
                >

                    <span />

                    {checkResult === "correct"
                        ? "Correct"

                        : checkResult === "incorrect"
                            ? "Incorrect"

                            : checking
                                ? "Checking"

                                : handDetected
                                    ? "Detecting"
                                    : "Waiting"
                    }

                </div>

            </div>


            {/* ==========================================
                CORRECT RESULT
            ========================================== */}

            {checkResult === "correct" && (

                <div className="sign-result correct-result">

                    <span className="result-icon">
                        ✓
                    </span>

                    <div>

                        <strong>
                            Correct Sign
                        </strong>

                        <p>
                            Great job! You performed the sign correctly.
                        </p>

                    </div>

                </div>

            )}


            {/* ==========================================
                INCORRECT RESULT
            ========================================== */}

            {checkResult === "incorrect" && (

                <div className="sign-result incorrect-result">

                    <span className="result-icon">
                        ×
                    </span>

                    <div>

                        <strong>
                            Incorrect Sign
                        </strong>

                        <p>
                            Try again and match the reference sign.
                        </p>

                    </div>

                </div>

            )}


            {/* ==========================================
                ERROR
            ========================================== */}

            {checkResult === "error" && (

                <div className="sign-result incorrect-result">

                    <span className="result-icon">
                        !
                    </span>

                    <div>

                        <strong>
                            Unable to check sign
                        </strong>

                        <p>
                            Please try again.
                        </p>

                    </div>

                </div>

            )}


            {/* ==========================================
                STATS
            ========================================== */}

            <div className="recognition-stats">


                {/* ======================================
                    PREDICTED SIGN
                ====================================== */}

                <div className="recognition-stat">

                    <span>
                        Predicted Sign
                    </span>

                    <strong>
                        {prediction || "--"}
                    </strong>

                </div>


                {/* ======================================
                    CONFIDENCE
                ====================================== */}

                <div className="recognition-stat">

                    <span>
                        Confidence
                    </span>

                    <strong>
                        {safeConfidence.toFixed(1)}%
                    </strong>

                </div>


                {/* ======================================
                    CONFIDENCE + ACCURACY
                ====================================== */}

                <div className="recognition-metrics">


                    {/* ==================================
                        RECOGNITION CONFIDENCE
                    ================================== */}

                    <div className="confidence-section">

                        <div className="confidence-header">

                            <span>
                                Recognition Confidence
                            </span>

                            <span>
                                {safeConfidence.toFixed(1)}%
                            </span>

                        </div>


                        <div className="confidence-track">

                            <div
                                className="confidence-fill"
                                style={{
                                    width: `${safeConfidence}%`
                                }}
                            />

                        </div>

                    </div>


                    {/* ==================================
                        SIGN ACCURACY
                    ================================== */}

                    <div className="accuracy-section">

                        <div className="accuracy-header">

                            <span>
                                Sign Accuracy
                            </span>

                            <span>
                                {safeAccuracy.toFixed(1)}%
                            </span>

                        </div>


                        <div className="accuracy-track">

                            <div
                                className="accuracy-fill"
                                style={{
                                    width: `${safeAccuracy}%`
                                }}
                            />

                        </div>

                    </div>

                </div>


                {/* ======================================
                    BUTTON
                ====================================== */}

                {checkResult === "incorrect" ? (

                    <button
                        type="button"
                        className="check-btn try-again-btn"
                        onClick={onTryAgain}
                    >
                        ↻ Try Again
                    </button>

                ) : checkResult === "correct" ? (

                    <button
                        type="button"
                        className="check-btn result-correct-btn"
                        disabled
                    >
                        ✓ Correct
                    </button>

                ) : (

                    <button
                        type="button"
                        className="check-btn"
                        onClick={onCheck}
                        disabled={
                            disabled ||
                            checking
                        }
                    >
                        {checking
                            ? "Checking..."
                            : "✓ Check Sign"
                        }
                    </button>

                )}

            </div>

        </div>
    );
}