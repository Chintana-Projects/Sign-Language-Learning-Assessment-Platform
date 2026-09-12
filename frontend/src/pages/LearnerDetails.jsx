import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import "../styles/learnerDetails.css";

export default function LearnerDetails() {
    const navigate = useNavigate();
    const { learnerId } = useParams();

    const [learner, setLearner] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    // =====================================================
    // FETCH LEARNER DETAILS
    // =====================================================

    useEffect(() => {
        const fetchLearnerDetails = async () => {
            try {
                setLoading(true);
                setError("");

                const response = await fetch(
                    `http://localhost:8000/instructor/students/${encodeURIComponent(
                        learnerId
                    )}`
                );

                if (!response.ok) {
                    throw new Error(
                        "Failed to fetch learner details."
                    );
                }

                const data = await response.json();

                const studentId =
                    data.student_id || learnerId;

                const learnerName =
                    data.student_name ||
                    `Learner ${studentId}`;

                const initials = learnerName
                    .split(" ")
                    .map(word => word[0])
                    .join("")
                    .substring(0, 2)
                    .toUpperCase();

                const progress =
                    data.progress_percentage ??
                    (
                        (
                            data.completed_count || 0
                        ) / 26
                    ) * 100;

                setLearner({
                    name: learnerName,

                    studentId: studentId,

                    initials: initials,

                    lesson:
                        data.current_letter || "A",

                    nextLesson:
                        data.next_letter || "A",

                    progress: Math.round(
                        Math.min(
                            100,
                            Math.max(0, progress)
                        )
                    ),

                    accuracy:
                        Number(data.accuracy ?? 0),

                    completed:
                        data.completed_count ??
                        (
                            data.completed_letters?.length || 0
                        ),

                    totalAttempts:
                        Number(data.total_attempts ?? 0),

                    totalSessions:
                        Number(data.total_sessions ?? 0),

                    strongLetters:
                        data.strong_letters || [],

                    weakLetters:
                        data.weak_letters || [],

                    alphabetMastery:
                        data.alphabet_mastery || {},

                    practiceHistory:
                        data.practice_history || [],

                    recommendations:
                        data.recommendations || []
                });
            } catch (err) {
                console.error(
                    "Learner details error:",
                    err
                );

                setError(
                    err.message ||
                    "Unable to load learner details."
                );
            } finally {
                setLoading(false);
            }
        };

        if (learnerId) {
            fetchLearnerDetails();
        }
    }, [learnerId]);

    // =====================================================
    // BACK TO DASHBOARD
    // =====================================================

    const goBack = () => {
        navigate("/accessibility-trainer");
    };

    // =====================================================
    // LOADING
    // =====================================================

    if (loading) {
        return (
            <div className="learner-details-page">

                <button
                    className="back-button"
                    type="button"
                    onClick={goBack}
                >
                    ← Back to Dashboard
                </button>

                <section className="learner-status-section">
                    <h2>
                        Loading learner details...
                    </h2>
                </section>

            </div>
        );
    }

    // =====================================================
    // ERROR
    // =====================================================

    if (error || !learner) {
        return (
            <div className="learner-details-page">

                <button
                    className="back-button"
                    type="button"
                    onClick={goBack}
                >
                    ← Back to Dashboard
                </button>

                <section className="learner-status-section">

                    <h2>Unable to Load Learner</h2>

                    <p>
                        {error ||
                            "Learner details could not be found."}
                    </p>

                </section>

            </div>
        );
    }

    // =====================================================
    // MAIN PAGE
    // =====================================================

    return (

        <div className="learner-details-page">

            {/* =================================================
                BACK BUTTON
            ================================================= */}

            <button
                className="back-button"
                type="button"
                onClick={goBack}
            >
                ← Back to Dashboard
            </button>


            {/* =================================================
                LEARNER HEADER
            ================================================= */}

            <header className="learner-details-header">

                <div className="learner-details-avatar">
                    {learner.initials}
                </div>

                <div>
                    <h1>{learner.name}</h1>

                    <p>
                        Accessibility Trainer • Learner Profile
                    </p>
                </div>

            </header>


            {/* =================================================
                OVERVIEW
            ================================================= */}

            <section className="learner-overview">

                <div className="overview-card">
                    <span>Current Lesson</span>
                    <strong>{learner.lesson}</strong>
                </div>

                <div className="overview-card">
                    <span>Overall Progress</span>
                    <strong>{learner.progress}%</strong>
                </div>

                <div className="overview-card">
                    <span>Accuracy</span>
                    <strong>
                        {learner.accuracy.toFixed(2)}%
                    </strong>
                </div>

                <div className="overview-card">
                    <span>Lessons Completed</span>
                    <strong>
                        {learner.completed}/26
                    </strong>
                </div>

            </section>


            {/* =================================================
                LEARNING PROGRESS
            ================================================= */}

            <section className="learner-status-section">

                <h2>Learning Progress</h2>

                <p>
                    View {learner.name}'s sign language
                    learning progress.
                </p>

                <div className="large-progress-bar">

                    <div
                        className="large-progress-fill"
                        style={{
                            width: `${learner.progress}%`
                        }}
                    />

                </div>

                <div className="progress-percentage">
                    {learner.progress}%
                </div>

            </section>


            {/* =================================================
                CURRENT STATUS
            ================================================= */}

            <section className="learner-status-section">

                <h2>Current Status</h2>

                <div className="status-card">

                    <div>

                        <strong>
                            Currently Learning
                        </strong>

                        <p>
                            ASL Letter {learner.lesson}
                        </p>

                    </div>

                    <span className="status-badge">
                        In Progress
                    </span>

                </div>

            </section>


            {/* =================================================
                LEARNING STATS
            ================================================= */}

            <section className="learner-status-section">

                <h2>Learning Statistics</h2>

                <div className="learner-overview">

                    <div className="overview-card">
                        <span>Total Attempts</span>
                        <strong>
                            {learner.totalAttempts}
                        </strong>
                    </div>

                    <div className="overview-card">
                        <span>Total Sessions</span>
                        <strong>
                            {learner.totalSessions}
                        </strong>
                    </div>

                    <div className="overview-card">
                        <span>Next Letter</span>
                        <strong>
                            {learner.nextLesson}
                        </strong>
                    </div>

                </div>

            </section>


            {/* =================================================
                STRONG LETTERS
            ================================================= */}

            <section className="learner-status-section">

                <h2>Strong Letters</h2>

                {learner.strongLetters.length > 0 ? (

                    <div className="letter-badge-list">

                        {learner.strongLetters.map(
                            (letter) => (
                                <span
                                    key={letter}
                                    className="status-badge"
                                >
                                    {letter}
                                </span>
                            )
                        )}

                    </div>

                ) : (

                    <p>
                        Complete more lessons to identify
                        strong letters.
                    </p>

                )}

            </section>


            {/* =================================================
                WEAK LETTERS
            ================================================= */}

            <section className="learner-status-section">

                <h2>Letters Needing Practice</h2>

                {learner.weakLetters.length > 0 ? (

                    <div className="letter-badge-list">

                        {learner.weakLetters.map(
                            (letter) => (
                                <span
                                    key={letter}
                                    className="status-badge weak-badge"
                                >
                                    {letter}
                                </span>
                            )
                        )}

                    </div>

                ) : (

                    <p>
                        Not enough practice data available yet.
                    </p>

                )}

            </section>


            {/* =================================================
                RECOMMENDATIONS
            ================================================= */}

            <section className="learner-status-section">

                <h2>Recommendations</h2>

                {learner.recommendations.length > 0 ? (

                    <div className="recommendation-list">

                        {learner.recommendations.map(
                            (
                                recommendation,
                                index
                            ) => (

                                <div
                                    key={index}
                                    className="status-card recommendation-card"
                                >

                                    <div>

                                        <strong>
                                            {
                                                recommendation.type ||
                                                "Recommendation"
                                            }
                                        </strong>

                                        <p>
                                            {
                                                recommendation.message ||
                                                "Continue practicing."
                                            }
                                        </p>

                                    </div>

                                    <span className="status-badge">
                                        {
                                            recommendation.priority ||
                                            "NORMAL"
                                        }
                                    </span>

                                </div>

                            )
                        )}

                    </div>

                ) : (

                    <p>
                        No recommendations available yet.
                    </p>

                )}

            </section>

        </div>

    );
}