import { useLocation, useNavigate } from "react-router-dom";
import "../styles/certification.css";

export default function CertificationResult() {

    const location = useLocation();
    const navigate = useNavigate();

    const certificateId =
        location.state?.certificate_id || null;

    const score =
        location.state?.score || 0;

    const passed =
        location.state?.passed || false;

    const results =
        location.state?.results || [];

    const certificate = {

        certificate_id: certificateId,

        student_name:
            localStorage.getItem(
                "student_name"
            ) || "Learner",

        score: score,

        level:
            score >= 86
                ? "Professional"
                : score >= 71
                ? "Intermediate"
                : score >= 60
                ? "Beginner"
                : "Not Certified",

        issued_at:
            new Date().toISOString()

    };

    return (

        <div className="certification-page">

            {/* RESULT CARD */}

            <div className="certification-result-card">

                <div className="result-icon-large">
                    {passed ? "🏆" : "📘"}
                </div>

                <h1>
                    {passed
                        ? "Certification Passed!"
                        : "Certification Completed"}
                </h1>

                <p>
                    {passed
                        ? "Congratulations! You successfully passed the certification assessment."
                        : "You completed the assessment. Keep practicing and try again."}
                </p>

                {/* SCORE */}

                <div className="final-score-box">

                    <span>
                        Final Score
                    </span>

                    <strong>
                        {Number(score).toFixed(1)}%
                    </strong>

                </div>

                {/* LEVEL */}

                {passed && (

                    <div
                        style={{
                            marginTop: "20px",
                            textAlign: "center"
                        }}
                    >

                        <h3>
                            Certification Level
                        </h3>

                        <p
                            style={{
                                fontSize: "22px",
                                fontWeight: "700",
                                color: "#2563eb"
                            }}
                        >
                            {certificate.level}
                        </p>

                    </div>

                )}

                {/* CERTIFICATE ID */}

                {passed && certificateId && (

                    <div
                        style={{
                            marginTop: "20px",
                            textAlign: "center"
                        }}
                    >

                        <h3>
                            Certificate ID
                        </h3>

                        <p
                            style={{
                                fontSize: "20px",
                                fontWeight: "bold",
                                letterSpacing: "2px"
                            }}
                        >
                            {certificateId}
                        </p>

                        <button
                            onClick={() =>
                                navigate(
                                    "/certificate",
                                    {
                                        state: {
                                            certificate
                                        }
                                    }
                                )
                            }
                            style={{
                                marginTop: "20px",
                                padding: "12px 24px",
                                background: "#2563eb",
                                color: "#fff",
                                border: "none",
                                borderRadius: "8px",
                                cursor: "pointer",
                                fontWeight: "600"
                            }}
                        >
                            🏆 View Certificate
                        </button>

                    </div>

                )}

            </div>

            {/* RESULTS TABLE */}

            <section className="certification-section">

                <div className="section-heading">

                    <h3>
                        Assessment Results
                    </h3>

                    <p>
                        Review your performance for each letter.
                    </p>

                </div>

                <div className="results-table">

                    <div className="results-header">

                        <span>Letter</span>
                        <span>Prediction</span>
                        <span>Confidence</span>
                        <span>Result</span>

                    </div>

                    {results.map((item, index) => (

                        <div
                            key={index}
                            className="results-row"
                        >

                            <span>
                                {item.letter}
                            </span>

                            <span>
                                {item.predicted}
                            </span>

                            <span>
                                {(
                                    Number(
                                        item.confidence || 0
                                    ) * 100
                                ).toFixed(1)}
                                %
                            </span>

                            <span
                                className={
                                    item.correct
                                        ? "result-correct"
                                        : "result-incorrect"
                                }
                            >
                                {item.correct
                                    ? "✓ Correct"
                                    : "✗ Incorrect"}
                            </span>

                        </div>

                    ))}

                </div>

            </section>

            {/* BACK BUTTON */}

            <div
                style={{
                    textAlign: "center",
                    marginTop: "30px"
                }}
            >

                <button
                    className="return-btn"
                    onClick={() =>
                        navigate(
                            "/dashboard/certification"
                        )
                    }
                >
                    Back to Certification
                </button>

            </div>

        </div>

    );

}