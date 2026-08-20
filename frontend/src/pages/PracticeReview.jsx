
import React, {
    useEffect,
    useState
} from "react";

import ScoreCard from "../components/ScoreCard";
import ConfidenceChart from "../components/ConfidenceChart";
import GestureFeedback from "../components/GestureFeedback";
import ReviewSummary from "../components/ReviewSummary";


// =====================================
// Confidence Formatter
// =====================================

function formatConfidence(value) {

    let confidence = Number(value ?? 0);

    if (confidence <= 1) {
        confidence = confidence * 100;
    }

    return confidence.toFixed(2);
}


// =====================================
// Practice Review
// =====================================

function PracticeReview({
    sessionId
}) {

    const [reviewData, setReviewData] = useState(null);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");


    // =====================================
    // Fetch Review Data
    // =====================================

    useEffect(() => {

        if (sessionId) {
            fetchReview();
        }

    }, [sessionId]);


    async function fetchReview() {

        try {

            setLoading(true);
            setError("");


            const response = await fetch(
                `http://127.0.0.1:8000/review/${sessionId}`
            );


            if (!response.ok) {

                throw new Error(
                    "Review API failed"
                );

            }


            const data = await response.json();


            console.log(
                "Review Response:",
                data
            );


            if (data.success) {

                setReviewData(
                    data.review
                );

            } else {

                setError(
                    "No review data available"
                );

            }

        } catch (err) {

            console.error(
                "Review Error:",
                err
            );

            setError(
                "Unable to load practice review"
            );

        } finally {

            setLoading(false);

        }

    }


    // =====================================
    // Loading State
    // =====================================

    if (loading) {

        return (

            <div className="review-loading">

                <h2>
                    ⏳ Loading Practice Review...
                </h2>

            </div>

        );

    }


    // =====================================
    // Error State
    // =====================================

    if (error) {

        return (

            <div className="review-error">

                ❌ {error}

            </div>

        );

    }


    // =====================================
    // No Review Data
    // =====================================

    if (!reviewData) {

        return (

            <div className="review-error">

                No Review Data Found

            </div>

        );

    }


    // =====================================
    // Extract Backend Data Safely
    // =====================================

    const confidenceData =
        reviewData.confidence_trend || [];


    const feedbackData =
        reviewData.gesture_feedback || [];


    const motionMetrics =
        reviewData.motion_metrics ?? {

            gesture_stability: 0,

            average_confidence: 0,

            invalid_frames: 0,

            frames_analyzed: 0,

            time_taken: 0

        };


    // =====================================
    // Sign Score
    // =====================================

    const signScore =
        reviewData.correct_attempts?.length > 0
            ? reviewData.correct_attempts[0]?.sign_score
            : reviewData.sign_score || {};


    // =====================================
    // Attempts
    // =====================================

    const correctAttempts =
        reviewData.correct_attempts?.length || 0;


    const incorrectAttempts =
        reviewData.incorrect_attempts?.length || 0;


    const totalAttempts =
        correctAttempts + incorrectAttempts;


    // =====================================
    // Accuracy
    // =====================================

    const accuracy =
        reviewData.session_statistics?.accuracy
        ??
        reviewData.accuracy
        ??
        0;


    // =====================================
    // Overall Score
    // =====================================

    const overallScore =
        reviewData.overall_score
        ??
        signScore.overall_score
        ??
        0;


    // =====================================
    // RETURN
    // =====================================

    return (

        <div className="practice-review">

            {/* =================================
                TITLE
            ================================= */}

            <h1 className="review-title">

                📊 Practice Review

            </h1>


            {/* =================================
                OVERALL SCORE
            ================================= */}

            <ScoreCard
                score={overallScore}
                correct={correctAttempts}
                total={totalAttempts}
            />


            {/* =================================
                SIGN SCORE
            ================================= */}

            <div className="card sign-score-card">

                <h2>
                    🏆 Sign Score
                </h2>


                <div className="big-score">

                    {Number(
                        signScore.overall_score
                        ??
                        overallScore
                        ??
                        0
                    ).toFixed(2)}

                    %

                </div>


                <div className="score-details">

                    <p>

                        <b>Grade:</b>{" "}

                        {
                            signScore.grade
                            ??
                            (
                                overallScore >= 90
                                    ? "Excellent"
                                    : overallScore >= 75
                                        ? "Good"
                                        : overallScore >= 50
                                            ? "Average"
                                            : "Needs Improvement"
                            )
                        }

                    </p>


                    <p>

                        <b>Accuracy:</b>{" "}

                        {
                            Number(
                                signScore.components?.accuracy
                                ??
                                accuracy
                                ??
                                0
                            ).toFixed(2)
                        }%

                    </p>


                    <p>

                        <b>Confidence:</b>{" "}

                        {
                            formatConfidence(

                                signScore.components?.confidence
                                ??
                                signScore.components?.confidence_score
                                ??
                                motionMetrics.average_confidence

                            )
                        }%

                    </p>


                    <p>

                        <b>Stability:</b>{" "}

                        {
                            Number(

                                signScore.components?.stability
                                ??
                                signScore.components?.stability_score
                                ??
                                motionMetrics.gesture_stability
                                ??
                                0

                            ).toFixed(2)

                        }%

                    </p>

                </div>

            </div>


            {/* =================================
                GESTURE ANALYSIS
            ================================= */}

            <div className="card gesture-analysis-card">

                <h2>
                    📈 Gesture Analysis
                </h2>


                <div className="metrics-grid">


                    {/* Stability */}

                    <div className="metric-item">

                        <span>
                            Stability
                        </span>

                        <strong>

                            {
                                Number(
                                    motionMetrics.gesture_stability
                                    ?? 0
                                ).toFixed(2)
                            }%

                        </strong>

                    </div>


                    {/* Confidence */}

                    <div className="metric-item">

                        <span>
                            Confidence
                        </span>

                        <strong>

                            {
                                formatConfidence(
                                    motionMetrics.average_confidence
                                )
                            }%

                        </strong>

                    </div>


                    {/* Invalid Frames */}

                    <div className="metric-item">

                        <span>
                            Invalid Frames
                        </span>

                        <strong>

                            {
                                motionMetrics.invalid_frames
                                ?? 0
                            }

                        </strong>

                    </div>


                    {/* Frames */}

                    <div className="metric-item">

                        <span>
                            Frames
                        </span>

                        <strong>

                            {
                                motionMetrics.frames_analyzed
                                ?? 0
                            }

                        </strong>

                    </div>


                    {/* Time */}

                    <div className="metric-item">

                        <span>
                            Time
                        </span>

                        <strong>

                            {
                                motionMetrics.time_taken
                                ?? 0
                            }s

                        </strong>

                    </div>

                </div>

            </div>


            {/* =================================
                CONFIDENCE GRAPH
            ================================= */}

            <ConfidenceChart
                data={confidenceData}
            />


            {/* =================================
                GESTURE FEEDBACK
            ================================= */}

            <GestureFeedback
                feedback={feedbackData}
            />


            {/* =================================
                COMMON MISTAKES
            ================================= */}

            <div className="card mistake-card">

                <h2>
                    📌 Common Mistakes
                </h2>


                {
                    reviewData.common_mistakes &&
                    Object.keys(
                        reviewData.common_mistakes
                    ).length > 0

                    ?

                    (

                        <div className="mistake-list">

                            {
                                Object.entries(
                                    reviewData.common_mistakes
                                ).map(
                                    ([mistake, count], index) => (

                                        <div
                                            className="mistake-item"
                                            key={index}
                                        >

                                            <span>
                                                {mistake}
                                            </span>

                                            <span>
                                                {count} times
                                            </span>

                                        </div>

                                    )
                                )
                            }

                        </div>

                    )

                    :

                    (

                        <p>
                            🎉 No common mistakes detected.
                        </p>

                    )
                }

            </div>


            {/* =================================
                DETAILED SUMMARY
            ================================= */}

            <ReviewSummary
                reviewData={reviewData}
            />


            {/* =================================
                RECOMMENDED PRACTICE
            ================================= */}

            <div className="card recommendation-section">

                <h2>
                    🎯 Recommended Gestures To Practice
                </h2>


                {
                    reviewData.recommended_gestures
                        ?.recommended
                        ?.length > 0

                    ?

                    (

                        reviewData.recommended_gestures.recommended.map(
                            (gesture, index) => (

                                <div
                                    className="gesture-recommendation"
                                    key={index}
                                >

                                    <h3>

                                        🔤 {gesture.practice}

                                    </h3>


                                    <p>

                                        <b>
                                            Confused With:
                                        </b>{" "}

                                        {
                                            gesture.confused_with
                                            ??
                                            "N/A"
                                        }

                                    </p>


                                    <p>

                                        {
                                            gesture.reason
                                            ??
                                            "Continue practicing this gesture."
                                        }

                                    </p>


                                    <p>

                                        <b>
                                            Mistakes:
                                        </b>{" "}

                                        {
                                            gesture.mistakes
                                            ??
                                            0
                                        }

                                    </p>

                                </div>

                            )
                        )

                    )

                    :

                    (

                        <p>
                            🎉 Excellent! No recommendations.
                        </p>

                    )
                }

            </div>


            {/* =================================
                BACK TO PRACTICE
            ================================= */}

            <div className="review-footer">

                <p>
                    Keep practicing regularly to improve
                    your sign recognition accuracy.
                </p>

            </div>

        </div>

    );

}


export default PracticeReview;

