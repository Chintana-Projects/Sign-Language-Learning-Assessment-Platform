import { useEffect, useState } from "react";
import "./Reports.css";
import { useAuth } from "../context/AuthContext";

export default function Reports() {

    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const { user } = useAuth();

    const studentId = user?.id;


    // ============================================================
    // FETCH REPORT
    // ============================================================

    useEffect(() => {

        if (!studentId) {
            setLoading(false);
            setError("Student information is unavailable.");
            return;
        }

        const fetchReport = async () => {

            try {

                setLoading(true);
                setError("");

                console.log(
                    "Loading reports for student:",
                    studentId
                );

                const response = await fetch(
    `http://127.0.0.1:8000/assessment/report/${studentId}`
);

                if (!response.ok) {

                    throw new Error(
                        `HTTP error: ${response.status}`
                    );

                }

                const data = await response.json();

                console.log(
                    "REPORT DATA:",
                    data
                );

                if (!data.success) {

                    throw new Error(
                        "Report request was unsuccessful."
                    );

                }

                setReport(data);

            } catch (err) {

                console.error(
                    "REPORT ERROR:",
                    err
                );

                setError(
                    "Unable to load report."
                );

            } finally {

                setLoading(false);

            }

        };

        fetchReport();

    }, [studentId]);


    // ============================================================
    // LOADING STATE
    // ============================================================

    if (loading) {

        return (

            <div className="reports-page">

                <div className="reports-loading">

                    <div className="reports-loading-icon">
                        📊
                    </div>

                    <h2>
                        Loading Reports...
                    </h2>

                    <p>
                        Fetching your learning progress.
                    </p>

                </div>

            </div>

        );

    }


    // ============================================================
    // ERROR STATE
    // ============================================================

    if (error) {

        return (

            <div className="reports-page">

                <div className="reports-error">

                    <div>
                        ⚠️
                    </div>

                    <h2>
                        Unable to Load Reports
                    </h2>

                    <p>
                        {error}
                    </p>

                    <button
                        onClick={() => window.location.reload()}
                    >
                        Try Again
                    </button>

                </div>

            </div>

        );

    }


    // ============================================================
    // EMPTY STATE
    // ============================================================

    if (!report) {

        return (

            <div className="reports-page">

                <div className="reports-error">

                    <div>
                        📊
                    </div>

                    <h2>
                        No Report Available
                    </h2>

                    <p>
                        There is no learning report available
                        for this student.
                    </p>

                </div>

            </div>

        );

    }


    // ============================================================
    // REPORT DATA
    // ============================================================

    const summary = report.summary || {};

    const practicedLetters =
        (report.letters_practiced || [])
            .filter(
                (letter) =>
                    letter !== "COMPLETED" &&
                    /^[A-Z]$/.test(letter)
            );

    const weakLetters =
        (report.weak_letters || [])
            .filter(
                (item) =>
                    item.letter !== "COMPLETED"
            );

    const recentAttempts =
        report.recent_attempts || [];


    // ============================================================
    // FORMAT DATE
    // ============================================================

    const formatDate = (timestamp) => {

        if (!timestamp) {
            return "Unknown date";
        }

        try {

            return new Date(timestamp).toLocaleString(
                "en-IN",
                {
                    day: "2-digit",
                    month: "short",
                    year: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                }
            );

        } catch {

            return timestamp;

        }

    };


    // ============================================================
// DOWNLOAD PDF REPORT
// ============================================================

const downloadReport = async () => {

    if (!studentId) {
        return;
    }

    try {

        const response = await fetch(
    `http://127.0.0.1:8000/assessment/report/${studentId}/export`
);

        if (!response.ok) {

    const text = await response.text();

    console.error(
        "Backend response:",
        text
    );

    throw new Error(
        `HTTP error: ${response.status}`
    );
}
        const blob = await response.blob();

        const url = window.URL.createObjectURL(blob);

        const link = document.createElement("a");

        link.href = url;

        link.download = `SignSync_Report_${studentId}.pdf`;

        document.body.appendChild(link);

        link.click();

        link.remove();

        window.URL.revokeObjectURL(url);

    } catch (err) {

        console.error(
            "REPORT DOWNLOAD ERROR:",
            err
        );

        alert(
            "Unable to download the report. Please try again."
        );
    }
};


    // ============================================================
    // MAIN REPORT
    // ============================================================

    return (

        <div className="reports-page">


            {/* =====================================================
                HEADER
            ===================================================== */}

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

    <div className="reports-header-actions">

        <button
            className="download-report-btn"
            onClick={downloadReport}
        >
            📄 Download Report
        </button>

        <div className="reports-header-icon">
            📊
        </div>

    </div>

</div>


            {/* =====================================================
                SUMMARY
            ===================================================== */}

            <section className="report-summary">


                {/* TOTAL ATTEMPTS */}

                <div className="report-card">

                    <div className="report-card-icon">
                        🎯
                    </div>

                    <div>

                        <span>
                            Total Attempts
                        </span>

                        <strong>
                            {summary.total_attempts ?? 0}
                        </strong>

                    </div>

                </div>


                {/* CORRECT ATTEMPTS */}

                <div className="report-card">

                    <div className="report-card-icon">
                        ✓
                    </div>

                    <div>

                        <span>
                            Correct Attempts
                        </span>

                        <strong>
                            {summary.correct_attempts ?? 0}
                        </strong>

                    </div>

                </div>


                {/* ACCURACY */}

                <div className="report-card">

                    <div className="report-card-icon">
                        📈
                    </div>

                    <div>

                        <span>
                            Accuracy
                        </span>

                        <strong>
                            {summary.accuracy ?? 0}%
                        </strong>

                    </div>

                </div>


                {/* AVERAGE CONFIDENCE */}

                <div className="report-card">

                    <div className="report-card-icon">
                        🧠
                    </div>

                    <div>

                        <span>
                            Avg. Confidence
                        </span>

                        <strong>
                            {summary.average_confidence ?? 0}%
                        </strong>

                    </div>

                </div>


                {/* AVERAGE SCORE */}

                <div className="report-card">

                    <div className="report-card-icon">
                        ⭐
                    </div>

                    <div>

                        <span>
                            Average Score
                        </span>

                        <strong>
                            {summary.average_score ?? 0}
                        </strong>

                    </div>

                </div>

            </section>


            {/* =====================================================
                LETTERS PRACTICED
            ===================================================== */}

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


            {/* =====================================================
                LETTERS TO IMPROVE
            ===================================================== */}

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


                {weakLetters.length === 0 ? (

                    <div className="success-message">
                        🎉 Great job! No weak letters found.
                    </div>

                ) : (

                    <div className="weak-letters">

                        {weakLetters.map(
                            (item) => {

                                const accuracy =
                                    Math.min(
                                        Math.max(
                                            Number(item.accuracy) || 0,
                                            0
                                        ),
                                        100
                                    );

                                return (

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
                                                    {item.correct ?? 0} /{" "}
                                                    {item.attempts ?? 0} correct
                                                </span>

                                            </div>

                                            <b>
                                                {accuracy}%
                                            </b>

                                        </div>


                                        <div className="accuracy-bar">

                                            <div
                                                className="accuracy-fill"
                                                style={{
                                                    width: `${accuracy}%`
                                                }}
                                            />

                                        </div>

                                    </div>

                                );

                            }
                        )}

                    </div>

                )}

            </section>


{/* =====================================================
    RECENT ATTEMPTS
===================================================== */}

<section className="report-section">

    <div className="report-section-header">

        <div>
            <span className="reports-eyebrow">
                ACTIVITY
            </span>

            <h2>
                Recent Attempts
            </h2>

            <p className="report-section-subtitle">
                Your latest sign language practice attempts
            </p>
        </div>

        <span className="section-count">
            {recentAttempts.length}
        </span>

    </div>


    {recentAttempts.length === 0 ? (

        <div className="empty-attempts">
            <div className="empty-attempts-icon">
                ✋
            </div>

            <h3>
                No practice attempts yet
            </h3>

            <p>
                Start practicing to see your activity here.
            </p>
        </div>

    ) : (

        <div className="attempts-list">

            {recentAttempts.map((attempt, index) => {

                const confidence =
                    Number(attempt.confidence || 0) * 100;

                const score =
                    Number(attempt.score || 0);

                return (

                    <div
                        className={`attempt-card ${
                            attempt.correct
                                ? "attempt-correct"
                                : "attempt-incorrect"
                        }`}
                        key={
                            attempt.assessment_id ||
                            `${attempt.timestamp}-${index}`
                        }
                    >

                        {/* LEFT: LETTERS */}

                        <div className="attempt-letters">

                            <div className="attempt-letter-box">

                                <span className="attempt-label">
                                    Expected
                                </span>

                                <div className="attempt-letter">
                                    {attempt.expected}
                                </div>

                            </div>


                            <div className="attempt-arrow">
                                →
                            </div>


                            <div className="attempt-letter-box">

                                <span className="attempt-label">
                                    Detected
                                </span>

                                <div
                                    className={`attempt-letter detected ${
                                        attempt.correct
                                            ? "detected-correct"
                                            : "detected-incorrect"
                                    }`}
                                >
                                    {attempt.predicted}
                                </div>

                            </div>

                        </div>


                        {/* MIDDLE: RESULT */}

                        <div className="attempt-main">

                            <div
                                className={`attempt-status ${
                                    attempt.correct
                                        ? "status-correct"
                                        : "status-incorrect"
                                }`}
                            >

                                <span className="status-icon">
                                    {attempt.correct
                                        ? "✓"
                                        : "✕"}
                                </span>

                                <span>
                                    {attempt.correct
                                        ? "Correct"
                                        : "Incorrect"}
                                </span>

                            </div>


                            <div className="attempt-date">
                                {formatDate(
                                    attempt.timestamp
                                )}
                            </div>

                        </div>


                        {/* RIGHT: METRICS */}

                        <div className="attempt-metrics">

                            <div className="attempt-metric">

                                <span>
                                    Confidence
                                </span>

                                <strong>
                                    {confidence.toFixed(1)}%
                                </strong>

                            </div>


                            <div className="attempt-metric">

                                <span>
                                    Score
                                </span>

                                <strong>
                                    {score.toFixed(1)}
                                </strong>

                            </div>

                        </div>

                    </div>

                );

            })}

        </div>

    )}

</section>


        </div>
    );
}

