
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import "../styles/AccessibilityTrainer.css";

export default function AccessibilityTrainer() {
    const navigate = useNavigate();

    const [dashboard, setDashboard] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const loadDashboard = async () => {
            try {
                const response = await fetch(
                    "http://localhost:8000/instructor/dashboard"
                );

                if (!response.ok) {
                    throw new Error("Failed to load dashboard");
                }

                const data = await response.json();
                setDashboard(data);
            } catch (err) {
                console.error(err);
                setError("Unable to load dashboard data.");
            } finally {
                setLoading(false);
            }
        };

        loadDashboard();
    }, []);

    if (loading) {
        return (
            <div className="trainer-state">
                <h2>Loading dashboard...</h2>
            </div>
        );
    }

    if (error) {
        return (
            <div className="trainer-state">
                <h2>{error}</h2>
            </div>
        );
    }

    if (!dashboard) {
        return null;
    }

    const students = Array.isArray(dashboard.students)
        ? dashboard.students
        : [];

    const openLearner = (id) => {
        if (!id) return;

        navigate(`/accessibility-trainer/learner/${id}`);
    };

    return (
        <div className="accessibility-trainer-content">

            {/* STATISTICS */}
            <section className="trainer-stats">

                <div className="trainer-stat-card">
                    <div className="stat-icon">👥</div>

                    <div>
                        <span>Total Learners</span>
                        <h2>
                            {dashboard.total_students ?? 0}
                        </h2>
                    </div>
                </div>

                <div className="trainer-stat-card">
                    <div className="stat-icon">🎯</div>

                    <div>
                        <span>Active Learners</span>
                        <h2>
                            {dashboard.active_students ?? 0}
                        </h2>
                    </div>
                </div>

                <div className="trainer-stat-card">
                    <div className="stat-icon">📚</div>

                    <div>
                        <span>Completed Learners</span>
                        <h2>
                            {dashboard.completed_students ?? 0}
                        </h2>
                    </div>
                </div>

                <div className="trainer-stat-card">
                    <div className="stat-icon">⭐</div>

                    <div>
                        <span>Average Accuracy</span>
                        <h2>
                            {Number(
                                dashboard.average_accuracy ?? 0
                            ).toFixed(2)}%
                        </h2>
                    </div>
                </div>

            </section>


            {/* QUICK ACTIONS */}
            <section className="trainer-tools">

                <div className="section-header">
                    <div>
                        <h2>Trainer Tools</h2>

                        <p>
                            Quickly access learner management
                            and performance analytics.
                        </p>
                    </div>
                </div>

                <div className="trainer-tools-grid">

                    <button
                        className="trainer-tool-card"
                        onClick={() =>
                            navigate(
                                "/accessibility-trainer/learners"
                            )
                        }
                    >
                        <div className="tool-icon">
                            👥
                        </div>

                        <div>
                            <h3>Learners</h3>

                            <p>
                                View learner progress and
                                practice performance.
                            </p>
                        </div>

                        <span>→</span>
                    </button>


                    <button
                        className="trainer-tool-card"
                        onClick={() =>
                            navigate(
                                "/accessibility-trainer/analytics"
                            )
                        }
                    >
                        <div className="tool-icon">
                            📊
                        </div>

                        <div>
                            <h3>Analytics</h3>

                            <p>
                                Monitor skill development,
                                assessments and progress.
                            </p>
                        </div>

                        <span>→</span>
                    </button>

                </div>

            </section>


            {/* LEARNER PREVIEW */}
            <section className="learners-section">

                <div className="section-header">

                    <div>
                        <h2>Recent Learners</h2>

                        <p>
                            View a quick overview of learner progress.
                        </p>
                    </div>

                    <button
                        className="view-all-btn"
                        onClick={() =>
                            navigate(
                                "/accessibility-trainer/learners"
                            )
                        }
                    >
                        View All
                    </button>

                </div>


                <div className="learners-grid">

                    {students.length > 0 ? (

                        students
                            .slice(0, 4)
                            .map((student, index) => {

                                const learnerId =
    student.student_id ||
    `learner-${index}`;

const learnerName =
    student.student_name?.trim()
        ? student.student_name
        : `Learner ${learnerId}`;

                                const initials =
    learnerName
        .split(" ")
        .map(name => name[0])
        .slice(0, 2)
        .join("")
        .toUpperCase();

                                const completedLetters =
                                    Number(
                                        student.completed_letters || 0
                                    );

                                const progress =
                                    Math.min(
                                        100,
                                        Math.round(
                                            (completedLetters / 26) * 100
                                        )
                                    );

                                const accuracy =
                                    Number(
                                        student.accuracy || 0
                                    );

                                return (
                                    <div
                                        className="learner-card"
                                        key={learnerId}
                                    >

                                        <div className="learner-top">

                                            <div className="learner-avatar">
                                                {initials}
                                            </div>

                                            <div>
                                                <h3>
                                                    {learnerName}
                                                </h3>

                                                <p>
    {student.current_letter === "COMPLETED"
        ? "🏆 Certified Learner"
        : `Current lesson: ${student.current_letter || "-"}`
    }
</p>
                                            </div>

                                        </div>


                                        <div className="progress-info">

                                            <span>
                                                Progress
                                            </span>

                                            <strong>
                                                {progress}%
                                            </strong>

                                        </div>


                                        <div className="progress-bar">

                                            <div
    className="progress-fill"
    style={{
        width: `${progress}%`,
        background:
            progress < 30
                ? "#ef4444"
                : progress < 70
                ? "#f59e0b"
                : "#10b981"
    }}
/>

                                        </div>


                                        <div className="learner-bottom">

                                            <span>
                                                Accuracy
                                            </span>

                                            <strong>
                                                {accuracy.toFixed(2)}%
                                            </strong>

                                        </div>


                                        <button
                                            className="learner-button"
                                            onClick={() =>
                                                openLearner(
                                                    student.student_id
                                                )
                                            }
                                        >
                                            View Learner
                                        </button>

                                    </div>
                                );
                            })

                    ) : (

                        <div className="no-learners">
                            No learners found.
                        </div>

                    )}

                </div>

            </section>

        </div>
    );
}
