import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/certification.css";
import { useAuth } from "../context/AuthContext";

export default function Certification() {
    const navigate = useNavigate();

    // ==========================================
    // STATE DECLARATIONS
    // ==========================================
    const [currentLevel, setCurrentLevel] = useState("Beginner");
    const [canTakeCertification, setCanTakeCertification] = useState(true);
    const [progress, setProgress] = useState(0);

    const { user } = useAuth();
    const studentId = user?.id;
const [certificate, setCertificate] = useState(null);
    // ==========================================
    // CERTIFICATION LEVELS
    // ==========================================
   const levels = [
    "Beginner",
    "Intermediate",
    "Professional"
];
    const currentLevelIndex = levels.indexOf(currentLevel);

    // ==========================================
    // FETCH CERTIFICATION STATUS
    // ==========================================
    useEffect(() => {
        async function loadStatus() {
            try {
                const response = await fetch(
                    `http://127.0.0.1:8000/certification/status/${studentId}`
                );

                const data = await response.json();
                if (data.certificate_id) {
    const certResponse = await fetch(
        `http://127.0.0.1:8000/certificate/verify/${data.certificate_id}`
    );

    const certData = await certResponse.json();

    if (certData.valid) {
        setCertificate(certData.certificate);
    }
}
                console.log("Certification API Data:", data);

                setCurrentLevel(
    data.current_level || "Beginner"
);

                // Extract numeric percentage safely regardless of structure
                let progressValue = 0;
                if (typeof data.lesson_progress === "object" && data.lesson_progress !== null) {
                    progressValue = data.lesson_progress.percentage ?? 0;
                } else if (typeof data.lesson_progress === "number") {
                    progressValue = data.lesson_progress;
                }

                setProgress(Number(progressValue) || 0);
            } catch (error) {
                console.error(
                    "Failed to load certification status",
                    error
                );
            }
        }

        if (!studentId) return;

        loadStatus();
    }, [studentId]);

    // ==========================================
    // ASSESSMENTS
    // ==========================================
const assessments = [
    {
        title: "Sign Language Certification Exam",
        description:
            "Complete the certification assessment. Your certification level is awarded based on your final accuracy score.",
        level: "All Levels",
        status: certificate ? "Completed" : "Available"
    }
];

    // ==========================================
    // START ASSESSMENT
    // ==========================================
    const handleStartAssessment = async () => {
        try {
            console.log("Student ID:", user?.id);

            if (!user?.id) {
                alert("Student ID not found");
                return;
            }

            const response = await fetch(
                `http://127.0.0.1:8000/certification/start/${user.id}`,
                {
                    method: "POST"
                }
            );
            const data = await response.json();

            console.log("START RESPONSE:", data);

            if (!data.success) {
                alert(data.message || JSON.stringify(data));
                return;
            }

            navigate("/dashboard/certification/session", {
                state: {
                    certification_id: data.certification_id,
                    current_letter: data.current_letter,
                    progress: data.progress
                }
            });
        } catch (error) {
            console.error("Failed to start certification:", error);
        }
    };

    // Safely parse displayed progress to ensure React never receives an object
    const displayProgress = typeof progress === "object" 
        ? progress?.percentage ?? 0 
        : progress;

    // ==========================================
    // RENDER
    // ==========================================
    return (
        <div className="certification-page">
            {/* HEADER */}
            <div className="certification-header">
                <div>
                    <h2>Certification</h2>
                    <p>
                        Evaluate your sign language skills and earn
                        certification.
                    </p>
                </div>
            </div>

            <div
                style={{
                    display: "flex",
                    justifyContent: "flex-end",
                    marginBottom: "20px"
                }}
            >
                <button
    onClick={() =>
        navigate("/dashboard/leaderboard")
    }
    style={{
        display: "flex",
        alignItems: "center",
        gap: "10px",
        padding: "12px 24px",
        background: "linear-gradient(135deg, #2563eb, #7c3aed)",
        color: "#fff",
        border: "none",
        borderRadius: "12px",
        fontSize: "16px",
        fontWeight: "600",
        cursor: "pointer",
        boxShadow: "0 4px 12px rgba(37,99,235,0.3)",
        transition: "all 0.3s ease"
    }}
    onMouseOver={(e) => {
        e.currentTarget.style.transform =
            "translateY(-2px)";
        e.currentTarget.style.boxShadow =
            "0 8px 20px rgba(37,99,235,0.4)";
    }}
    onMouseOut={(e) => {
        e.currentTarget.style.transform =
            "translateY(0)";
        e.currentTarget.style.boxShadow =
            "0 4px 12px rgba(37,99,235,0.3)";
    }}
>
    🏆 View Leaderboard
</button>
            </div>

            {/* CERTIFICATION OVERVIEW */}
            <section className="certification-overview">
                {/* CURRENT LEVEL */}
                <div className="certification-level-card">
                    <span className="certification-label">
                        CURRENT LEVEL
                    </span>
                    <div className="certification-level-display">
                        <div className="certification-trophy">
                            🏆
                        </div>
                        <div>
                            <h1>{currentLevel}</h1>
                            <p>Your current certification level</p>
                        </div>
                    </div>
                </div>

                {/* PROGRESS */}
                <div className="certification-progress-card">
                    <div className="progress-header">
                        <div>
                            <span>PROGRESS TO NEXT LEVEL</span>
                            <h3>
                                {currentLevelIndex < levels.length - 1
                                    ? levels[currentLevelIndex + 1]
                                    : "Professional"}
                            </h3>
                        </div>
                        <strong>{displayProgress}%</strong>
                    </div>

                    <div className="certification-progress-bar">
                        <div
                            className="certification-progress-fill"
                            style={{ width: `${displayProgress}%` }}
                        />
                    </div>

                    <p>
                        Complete your certification assessment to advance
                        to the next level.
                    </p>
                </div>
            </section>
{/* CERTIFICATE */}
{certificate && (
    <section className="certification-section">

        <div className="section-heading">
            <h3>Your Certificate</h3>
            <p>
                You have successfully earned a certification.
            </p>
        </div>

        <div className="certificate-summary-card">

            <div className="certificate-badge-large">
                {certificate.level === "Professional"
                    ? "👑"
                    : certificate.level === "Intermediate"
                    ? "🥈"
                    : "📘"}
            </div>

            <div className="certificate-info">

                <h3>
                    {certificate.level} Certificate
                </h3>

                <div className="certificate-stats">

    <div className="stat-box">
        <span>Score</span>
        <strong>{certificate.score}%</strong>
    </div>

    <div className="stat-box">
        <span>Level</span>
        <strong>{certificate.level}</strong>
    </div>

    <div className="stat-box">
        <span>Certificate ID</span>
        <strong>{certificate.certificate_id}</strong>
    </div>

</div>

            </div>

            <button
                className="view-certificate-btn"
                onClick={() =>
                    navigate("/certificate", {
                        state: {
                            certificate
                        }
                    })
                }
            >
                View Certificate →
            </button>

        </div>

    </section>
)}
            {/* AVAILABLE ASSESSMENTS */}
            <section className="certification-section">
                <div className="section-heading">
                    <div>
                        <h3>Certification Assessments</h3>
                        <p>
                            Complete assessments to progress through the
                            certification levels.
                        </p>
                    </div>
                </div>

                <div className="certification-assessment-grid">
                    {assessments.map((assessment) => (
                        <div
                            key={assessment.level}
                            className={`certification-assessment-card ${
                                assessment.status === "Locked"
                                    ? "locked"
                                    : assessment.status === "Completed"
                                    ? "completed"
                                    : ""
                            }`}
                        >
                            {/* CARD TOP */}
                            <div className="assessment-card-top">
                                <div className="assessment-icon">
                                    {assessment.status === "Completed"
                                        ? "✓"
                                        : assessment.status === "Locked"
                                        ? "🔒"
                                        : "🏆"}
                                </div>

                                <span
                                    className={`assessment-status ${
                                        assessment.status === "Available"
                                            ? "available"
                                            : assessment.status ===
                                              "Completed"
                                            ? "completed-status"
                                            : "locked-status"
                                    }`}
                                >
                                    {assessment.status}
                                </span>
                            </div>

                            {/* TITLE */}
                            <h4>{assessment.title}</h4>

                            {/* DESCRIPTION */}
                            <p>{assessment.description}</p>

                            {/* FOOTER */}
                            <div className="assessment-card-footer">
                                <span>Level: {assessment.level}</span>

                                <button
                                    disabled={
                                        assessment.status !== "Available"
                                    }
                                    onClick={
                                        assessment.status === "Available"
                                            ? handleStartAssessment
                                            : undefined
                                    }
                                >
                                    {assessment.status === "Available"
                                        ? "Start Assessment"
                                        : assessment.status === "Completed"
                                        ? "Completed"
                                        : "Locked"}
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            </section>

            {/* EVALUATION CRITERIA */}
            <section className="certification-section">
                <div className="section-heading">
                    <h3>Certification Evaluation</h3>
                    <p>
                        Your certification performance is calculated using the
                        following criteria.
                    </p>
                </div>

                <div className="evaluation-grid">

    <div className="evaluation-item">
        <strong>60% - 70%</strong>
        <span>Beginner Certificate</span>
    </div>

    <div className="evaluation-item">
        <strong>71% - 85%</strong>
        <span>Intermediate Certificate</span>
    </div>

    <div className="evaluation-item">
        <strong>86% - 100%</strong>
        <span>Professional Certificate</span>
    </div>

</div>
            </section>

            {/* CERTIFICATION LEVELS */}
            <section className="certification-section">
                <div className="section-heading">
                    <h3>Certification Levels</h3>
                    <p>
    Earn your certification level based on your final
    assessment accuracy.
</p>
                </div>

                <div className="certification-levels">
                    {levels.map((level, index) => (
                        <div
                            key={level}
                            className={`certification-level-step ${
                                index === currentLevelIndex
                                    ? "current"
                                    : index < currentLevelIndex
                                    ? "completed"
                                    : ""
                            }`}
                        >
                            <div className="level-number">
                                {index < currentLevelIndex
                                    ? "✓"
                                    : index + 1}
                            </div>
                            <span>{level}</span>
                        </div>
                    ))}
                </div>
            </section>
        </div>
    );
}