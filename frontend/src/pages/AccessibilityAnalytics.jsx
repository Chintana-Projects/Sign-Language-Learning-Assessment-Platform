
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import "./AccessibilityAnalytics.css";

export default function AccessibilityAnalytics() {

    const navigate = useNavigate();

    const [dashboard, setDashboard] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {

        const loadDashboard = async () => {

            try {

                setLoading(true);
                setError("");

                const response = await fetch(
                    "http://localhost:8000/instructor/dashboard"
                );

                if (!response.ok) {
                    throw new Error(
                        "Failed to load analytics."
                    );
                }

                const data = await response.json();

                setDashboard(data);

            } catch (err) {

                console.error(
                    "Analytics Error:",
                    err
                );

                setError(
                    "Unable to load analytics data."
                );

            } finally {

                setLoading(false);

            }

        };

        loadDashboard();

    }, []);


    // =====================================================
    // LOADING
    // =====================================================

    if (loading) {

        return (
            <div className="analytics-message">
                <h2>Loading analytics...</h2>
            </div>
        );

    }


    // =====================================================
    // ERROR
    // =====================================================

    if (error) {

        return (
            <div className="analytics-message">
                <h2>{error}</h2>
            </div>
        );

    }


    if (!dashboard) {
        return null;
    }


    // =====================================================
    // DATA
    // =====================================================

    const skillDevelopment =
        dashboard.skill_development || {};

    const strongestLetters =
        skillDevelopment.strongest_letters || [];

    const weakestLetters =
        skillDevelopment.weakest_letters || [];

    const letterPerformance =
        skillDevelopment.letter_performance || [];

    const overallProgress =
        Number(
            skillDevelopment.overall_progress || 0
        );


    // =====================================================
    // CERTIFICATION STATUS
    // =====================================================

    const students =
        Array.isArray(dashboard.students)
            ? dashboard.students
            : [];

    const completedLearners =
        Number(
            dashboard.completed_students || 0
        );

    const notStartedLearners =
        students.filter(
            student =>
                Number(
                    student.completed_letters || 0
                ) === 0
        ).length;

    const inProgressLearners =
        Math.max(
            0,
            Number(
                dashboard.total_students || 0
            ) -
            completedLearners -
            notStartedLearners
        );


    // =====================================================
    // GET PERFORMANCE LEVEL
    // =====================================================

    const getPerformanceLevel = (accuracy) => {

        const value = Number(accuracy || 0);

        if (value >= 80) {
            return "strong";
        }

        if (value >= 60) {
            return "medium";
        }

        return "weak";
    };


    // =====================================================
    // MAIN
    // =====================================================

    return (

        <div className="analytics-content">

            {/* =================================================
                BACK BUTTON
            ================================================= */}

            <div className="analytics-top-bar">

                <button
                    type="button"
                    className="analytics-back-button"
                    onClick={() =>
                        navigate(
                            "/accessibility-trainer"
                        )
                    }
                >
                    ← Back to Dashboard
                </button>

            </div>


            {/* =================================================
                LEARNER ENGAGEMENT
            ================================================= */}

            <section className="analytics-section">

                <div className="analytics-section-header">

                    <div>

                        <h2>
                            Learner Engagement
                        </h2>

                        <p>
                            Monitor learner participation
                            and practice activity.
                        </p>

                    </div>

                </div>


                <div className="analytics-stats-grid">

                    <div className="analytics-stat-card">

                        <div className="analytics-stat-icon">
                            🏃
                        </div>

                        <div>

                            <span>
                                Active Learners
                            </span>

                            <h3>
                                {dashboard.active_students ?? 0}
                            </h3>

                        </div>

                    </div>


                    <div className="analytics-stat-card">

                        <div className="analytics-stat-icon">
                            🔄
                        </div>

                        <div>

                            <span>
                                Practice Sessions
                            </span>

                            <h3>
                                {Array.isArray(dashboard.students)
                                    ? dashboard.students.reduce(
                                        (total, student) =>
                                            total +
                                            Number(
                                                student.total_sessions || 0
                                            ),
                                        0
                                    )
                                    : 0}
                            </h3>

                        </div>

                    </div>


                    <div className="analytics-stat-card">

                        <div className="analytics-stat-icon">
                            ✋
                        </div>

                        <div>

                            <span>
                                Total Attempts
                            </span>

                            <h3>
                                {Array.isArray(dashboard.students)
                                    ? dashboard.students.reduce(
                                        (total, student) =>
                                            total +
                                            Number(
                                                student.total_attempts || 0
                                            ),
                                        0
                                    )
                                    : 0}
                            </h3>

                        </div>

                    </div>


                    <div className="analytics-stat-card">

                        <div className="analytics-stat-icon">
                            📊
                        </div>

                        <div>

                            <span>
                                Total Learners
                            </span>

                            <h3>
                                {dashboard.total_students ?? 0}
                            </h3>

                        </div>

                    </div>

                </div>

            </section>


            {/* =================================================
                SKILL DEVELOPMENT
            ================================================= */}

            <section className="analytics-section">

                <div className="analytics-section-header">

                    <div>

                        <h2>
                            Skill Development
                        </h2>

                        <p>
                            Monitor class progress and identify
                            strong and weak sign language skills.
                        </p>

                    </div>

                </div>


                {/* =================================================
                    OVERALL PROGRESS
                ================================================= */}

                <div className="overall-progress-card">

                    <div className="progress-heading">

                        <div>

                            <h3>
                                Overall Class Progress
                            </h3>

                            <p>
                                Percentage of alphabet lessons
                                completed across all learners.
                            </p>

                        </div>

                        <strong>
                            {overallProgress.toFixed(2)}%
                        </strong>

                    </div>


                    <div className="analytics-progress-bar">

                        <div
                            className="analytics-progress-fill"
                            style={{
                                width: `${Math.min(
                                    100,
                                    Math.max(
                                        0,
                                        overallProgress
                                    )
                                )}%`
                            }}
                        />

                    </div>

                </div>


                {/* =================================================
                    STRONG + WEAK
                ================================================= */}

                <div className="skill-columns">


                    {/* =================================================
                        STRONGEST
                    ================================================= */}

                    <div className="skill-card">

                        <h3>
                            Strongest Skills
                        </h3>

                        <p>
                            Signs learners are performing well in.
                        </p>


                        <div className="skill-list">

                            {strongestLetters.length > 0 ? (

                                strongestLetters.map(
                                    (item) => (

                                        <div
                                            className="skill-row"
                                            key={item.letter}
                                        >

                                            <div className="skill-letter">
                                                {item.letter}
                                            </div>

                                            <div className="skill-details">

                                                <strong>
                                                    {item.students} learners
                                                </strong>

                                                <span>
                                                    {Number(
                                                        item.accuracy || 0
                                                    ).toFixed(2)}%
                                                </span>

                                            </div>

                                        </div>

                                    )
                                )

                            ) : (

                                <p className="empty-text">
                                    No skill data available.
                                </p>

                            )}

                        </div>

                    </div>


                    {/* =================================================
                        NEEDS IMPROVEMENT
                    ================================================= */}

                    <div className="skill-card">

                        <h3>
                            Needs Improvement
                        </h3>

                        <p>
                            Signs that may require additional
                            practice.
                        </p>


                        <div className="skill-list">

                            {weakestLetters.length > 0 ? (

                                weakestLetters.map(
                                    (item) => (

                                        <div
                                            className="skill-row"
                                            key={item.letter}
                                        >

                                            <div className="skill-letter weak">
                                                {item.letter}
                                            </div>

                                            <div className="skill-details">

                                                <strong>
                                                    {item.students} learners
                                                </strong>

                                                <span>
                                                    {Number(
                                                        item.accuracy || 0
                                                    ).toFixed(2)}%
                                                </span>

                                            </div>

                                        </div>

                                    )
                                )

                            ) : (

                                <p className="empty-text">
                                    No skill data available.
                                </p>

                            )}

                        </div>

                    </div>

                </div>


                {/* =================================================
                    LETTER PERFORMANCE
                ================================================= */}

                <div className="letter-performance-card">

                    <div className="letter-performance-header">

                        <div>

                            <h3>
                                Letter Performance
                            </h3>

                            <p>
                                Accuracy across all alphabet signs.
                            </p>

                        </div>

                        <div className="performance-legend">

                            <span>
                                <i className="legend-dot strong-dot"></i>
                                Strong
                            </span>

                            <span>
                                <i className="legend-dot medium-dot"></i>
                                Average
                            </span>

                            <span>
                                <i className="legend-dot weak-dot"></i>
                                Needs Practice
                            </span>

                        </div>

                    </div>


                    <div className="letter-performance-grid">

                        {letterPerformance.length > 0 ? (

                            letterPerformance.map(
                                (item) => {

                                    const accuracy =
                                        Number(
                                            item.accuracy || 0
                                        );

                                    const level =
                                        getPerformanceLevel(
                                            accuracy
                                        );

                                    return (

                                        <div
                                            className={`letter-performance-item ${level}`}
                                            key={item.letter}
                                            title={`${item.letter}: ${accuracy.toFixed(1)}% accuracy`}
                                        >

                                            <div className="letter-performance-letter">
                                                {item.letter}
                                            </div>

                                            <div className="letter-performance-value">
                                                {accuracy.toFixed(1)}%
                                            </div>

                                        </div>

                                    );

                                }
                            )

                        ) : (

                            <p className="empty-text">
                                No letter performance data available.
                            </p>

                        )}

                    </div>

                </div>

            </section>


          
{/* =================================================
    CERTIFICATION MONITORING
================================================= */}

<section className="analytics-section">

    <div className="analytics-section-header">

        <div>

            <h2>
                Certification Monitoring
            </h2>

            <p>
                Monitor learner completion status
                and certification readiness.
            </p>

        </div>

    </div>


    {/* =================================================
        CERTIFICATION SUMMARY
    ================================================= */}

    <div className="certification-summary">

        <div className="certification-summary-info">

            <div>

                <span className="certification-summary-label">
                    Certification Readiness
                </span>

                <h3>
                    {dashboard.total_students
                        ? Math.round(
                            (completedLearners /
                                Number(dashboard.total_students)) *
                            100
                        )
                        : 0
                    }%
                </h3>

                <p>
                    Learners who have completed all 26 alphabet signs.
                </p>

            </div>

        </div>


        <div className="certification-summary-progress">

            <div className="certification-summary-progress-bar">

                <div
                    className="certification-summary-progress-fill"
                    style={{
                        width: `${
                            dashboard.total_students
                                ? Math.min(
                                    100,
                                    Math.max(
                                        0,
                                        (completedLearners /
                                            Number(dashboard.total_students)) *
                                        100
                                    )
                                )
                                : 0
                        }%`
                    }}
                />

            </div>

            <span>
                {completedLearners} of{" "}
                {dashboard.total_students ?? 0} learners ready
            </span>

        </div>

    </div>


    {/* =================================================
        CERTIFICATION STATUS
    ================================================= */}

    <div className="certification-grid">

        <div className="certification-card completed">

            <div className="certification-number">
                {completedLearners}
            </div>

            <div>

                <strong>
                    Completed
                </strong>

                <p>
                    Learners who completed all
                    26 letters.
                </p>

            </div>

        </div>


        <div className="certification-card progress">

            <div className="certification-number">
                {inProgressLearners}
            </div>

            <div>

                <strong>
                    In Progress
                </strong>

                <p>
                    Learners currently developing
                    their skills.
                </p>

            </div>

        </div>


        <div className="certification-card not-started">

            <div className="certification-number">
                {notStartedLearners}
            </div>

            <div>

                <strong>
                    Not Started
                </strong>

                <p>
                    Learners with no completed
                    lessons.
                </p>

            </div>

        </div>

    </div>

</section>



        </div>
    );
}