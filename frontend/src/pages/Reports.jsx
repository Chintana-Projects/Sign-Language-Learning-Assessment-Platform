import { useEffect, useState } from "react";
import "./Reports.css";
import { useAuth } from "../context/AuthContext";

export default function Reports() {
    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
const { user } = useAuth();
    const studentId = user?.id;

  
useEffect(() => {

    if (!user?.id) {
        return;
    }

    const studentId = user.id;

    console.log(
        "Loading reports for user:",
        studentId
    );

    fetch(
        `http://127.0.0.1:8000/reports/${studentId}`
    )
        .then((response) => {

            if (!response.ok) {

                throw new Error(
                    `HTTP error: ${response.status}`
                );

            }

            return response.json();
        })
        .then((data) => {

            console.log(
                "REPORT DATA:",
                data
            );

            setReport(data);
            setLoading(false);
        })
        .catch((err) => {

            console.error(
                "REPORT ERROR:",
                err
            );

            setError(
                "Unable to load report."
            );

            setLoading(false);
        });

}, [user]);



    if (loading) {
        return (
            <div className="reports-page">
                <div className="reports-loading">
                    <div className="reports-loading-icon">
                        📊
                    </div>

                    <h2>Loading Reports...</h2>

                    <p>
                        Fetching your learning progress.
                    </p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="reports-page">
                <div className="reports-error">
                    <div>⚠️</div>

                    <h2>Unable to Load Reports</h2>

                    <p>{error}</p>

                    <button
                        onClick={() => window.location.reload()}    
                    >
                        Try Again
                    </button>
                </div>
            </div>
        );
    }

    const summary = report.summary;

    const practicedLetters =
        report.letters_practiced.filter(
            (letter) =>
                letter !== "COMPLETED" &&
                /^[A-Z]$/.test(letter)
        );

    return (
        <div className="reports-page">

            {/* HEADER */}

            <div className="reports-header">

                <div>
                    <span className="reports-eyebrow">
                        LEARNING ANALYTICS
                    </span>

                    <h1>
                        My Reports
                    </h1>

                    <p>
                        Track your sign language learning
                        progress and practice performance.
                    </p>
                </div>

                <div className="reports-header-icon">
                    📊
                </div>

            </div>


            {/* SUMMARY */}

            <section className="report-summary">

                <div className="report-card">
                    <div className="report-card-icon">
                        🎯
                    </div>

                    <div>
                        <span>
                            Total Attempts
                        </span>

                        <strong>
                            {summary.total_attempts}
                        </strong>
                    </div>
                </div>


                <div className="report-card">
                    <div className="report-card-icon">
                        ✓
                    </div>

                    <div>
                        <span>
                            Correct Attempts
                        </span>

                        <strong>
                            {summary.correct_attempts}
                        </strong>
                    </div>
                </div>


                <div className="report-card">
                    <div className="report-card-icon">
                        📈
                    </div>

                    <div>
                        <span>
                            Accuracy
                        </span>

                        <strong>
                            {summary.accuracy}%
                        </strong>
                    </div>
                </div>


                <div className="report-card">
                    <div className="report-card-icon">
                        🧠
                    </div>

                    <div>
                        <span>
                            Avg. Confidence
                        </span>

                        <strong>
                            {summary.average_confidence}%
                        </strong>
                    </div>
                </div>


                <div className="report-card">
                    <div className="report-card-icon">
                        ⭐
                    </div>

                    <div>
                        <span>
                            Average Score
                        </span>

                        <strong>
                            {summary.average_score}
                        </strong>
                    </div>
                </div>

            </section>


            {/* LETTERS PRACTICED */}

            <section className="report-section">

                <div className="report-section-header">

                    <div>
                        <span className="reports-eyebrow">
                            PROGRESS
                        </span>

                        <h2>
                            Letters Practiced
                        </h2>
                    </div>

                    <span className="section-count">
                        {practicedLetters.length} / 26
                    </span>

                </div>


                <div className="letters-list">

                    {practicedLetters.length > 0 ? (
                        practicedLetters.map(
                            (letter) => (
                                <span
                                    key={letter}
                                    className="letter-badge"
                                >
                                    {letter}
                                </span>
                            )
                        )
                    ) : (
                        <p className="empty-text">
                            No letters practiced yet.
                        </p>
                    )}

                </div>

            </section>


            {/* LETTERS TO IMPROVE */}

            <section className="report-section">

                <div className="report-section-header">

                    <div>
                        <span className="reports-eyebrow">
                            FOCUS AREAS
                        </span>

                        <h2>
                            Letters to Improve
                        </h2>
                    </div>

                </div>


                {report.weak_letters.length === 0 ? (

                    <div className="success-message">
                        🎉 Great job! No weak letters found.
                    </div>

                ) : (

                    <div className="weak-letters">

                        {report.weak_letters
                            .filter(
                                (item) =>
                                    item.letter !==
                                    "COMPLETED"
                            )
                            .map((item) => (

                                <div
                                    className="weak-letter"
                                    key={item.letter}
                                >

                                    <div className="weak-letter-top">

                                        <div className="weak-letter-symbol">
                                            {item.letter}
                                        </div>

                                        <div>
                                            <strong>
                                                Letter {item.letter}
                                            </strong>

                                            <span>
                                                {item.correct} /{" "}
                                                {item.attempts} correct
                                            </span>
                                        </div>

                                        <b>
                                            {item.accuracy}%
                                        </b>

                                    </div>


                                    <div className="accuracy-bar">

                                        <div
                                            className="accuracy-fill"
                                            style={{
                                                width: `${Math.min(item.accuracy, 100)}%`
                                            }}
                                        />

                                    </div>

                                </div>

                            ))}

                    </div>

                )}

            </section>


            {/* RECENT ATTEMPTS */}

            <section className="report-section">

                <div className="report-section-header">

                    <div>
                        <span className="reports-eyebrow">
                            ACTIVITY
                        </span>

                        <h2>
                            Recent Attempts
                        </h2>
                    </div>

                    <span className="section-count">
                        {report.recent_attempts.length}
                    </span>

                </div>


                <div className="attempts-list">

                    {report.recent_attempts.map(
                        (attempt) => (

                            <div
                                className="attempt-row"
                                key={
                                    attempt.assessment_id
                                }
                            >

                                <div className="attempt-letter">
                                    {attempt.expected}
                                </div>

                                <div className="attempt-arrow">
                                    →
                                </div>

                                <div className="attempt-letter detected">
                                    {attempt.predicted}
                                </div>

                                <div className="attempt-result">

                                    <span
                                        className={
                                            attempt.correct
                                                ? "result-correct"
                                                : "result-incorrect"
                                        }
                                    >
                                        {attempt.correct
                                            ? "✓ Correct"
                                            : "✕ Incorrect"}
                                    </span>

                                </div>

                                <div className="attempt-confidence">
                                    {(
                                        attempt.confidence * 100
                                    ).toFixed(1)}
                                    % confidence
                                </div>

                            </div>

                        )
                    )}

                </div>

            </section>

        </div>
    );
}