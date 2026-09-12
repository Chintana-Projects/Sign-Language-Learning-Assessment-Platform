import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { getInstructorDashboard } from "../../services/instructorDashboardService";

export default function InstructorStudents() {
    const navigate = useNavigate();

    const [students, setStudents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        async function loadStudents() {
            try {
                setLoading(true);
                setError("");

                const data = await getInstructorDashboard();

                setStudents(data?.students || []);
            } catch (err) {
                console.error("Failed to load students:", err);
                setError("Unable to load students.");
            } finally {
                setLoading(false);
            }
        }

        loadStudents();
    }, []);

    if (loading) {
        return (
            <div style={pageStyle}>
                <div style={messageStyle}>
                    <div style={{ fontSize: "40px" }}>⟳</div>
                    <h2>Loading Students...</h2>
                    <p>Fetching learner information.</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div style={pageStyle}>
                <div style={messageStyle}>
                    <div style={{ fontSize: "40px" }}>⚠️</div>
                    <h2>Something went wrong</h2>
                    <p>{error}</p>
                </div>
            </div>
        );
    }

    return (
        <div style={pageStyle}>
            <div style={containerStyle}>

                {/* Header */}
                <div style={headerStyle}>
                    <div>
                        <div style={titleRowStyle}>
                            <div style={iconStyle}>
                                👥
                            </div>

                            <div>
                                <h1 style={titleStyle}>
                                    Students
                                </h1>

                                <p style={subtitleStyle}>
                                    Monitor and manage learner progress
                                </p>
                            </div>
                        </div>
                    </div>

                    <button
                        type="button"
                        onClick={() =>
                            navigate("/instructor/dashboard")
                        }
                        style={backButtonStyle}
                    >
                        ← Dashboard
                    </button>
                </div>

                {/* Summary */}
                <div style={summaryStyle}>
                    <div>
                        <div style={summaryLabelStyle}>
                            Total Students
                        </div>

                        <div style={summaryValueStyle}>
                            {students.length}
                        </div>
                    </div>

                    <div style={summaryIconStyle}>
                        👥
                    </div>
                </div>

                {/* Student List */}
                <div style={cardStyle}>

                    <div style={cardHeaderStyle}>
                        <div>
                            <h2 style={cardTitleStyle}>
                                All Students
                            </h2>

                            <p style={cardSubtitleStyle}>
                                View individual learner performance
                            </p>
                        </div>

                        <span style={countBadgeStyle}>
                            {students.length} Students
                        </span>
                    </div>

                    {students.length === 0 ? (
                        <div style={emptyStyle}>
                            No students found.
                        </div>
                    ) : (
                        <div style={tableWrapperStyle}>
                            <table style={tableStyle}>
                                <thead>
                                    <tr>
                                        <th style={thStyle}>
                                            Student
                                        </th>

                                        <th style={thStyle}>
                                            Current Letter
                                        </th>

                                        <th style={thStyle}>
                                            Progress
                                        </th>

                                        <th style={thStyle}>
                                            Accuracy
                                        </th>

                                        <th style={thStyle}>
                                            Sessions
                                        </th>

                                        <th style={thStyle}>
                                            Action
                                        </th>
                                    </tr>
                                </thead>

                                <tbody>
                                    {students.map(
                                        (student, index) => {

                                            const accuracy =
                                                Number(
                                                    student.accuracy ?? 0
                                                );

                                            const completed =
                                                Number(
                                                    student.completed_letters ?? 0
                                                );

                                            const studentId =
                                                student.student_id;

                                            return (
                                                <tr
                                                    key={
                                                        studentId ||
                                                        `student-${index}`
                                                    }
                                                >

                                                    {/* Student */}
                                                    <td style={tdStyle}>
                                                        <div
                                                            style={{
                                                                display: "flex",
                                                                alignItems:
                                                                    "center",
                                                                gap: "12px"
                                                            }}
                                                        >
                                                            <div
                                                                style={
                                                                    avatarStyle
                                                                }
                                                            >
                                                                {String(
                                                                    studentId ||
                                                                    "S"
                                                                )
                                                                    .charAt(0)
                                                                    .toUpperCase()}
                                                            </div>

                                                            <div>
                                                                <div
                                                                    style={
                                                                        studentNameStyle
                                                                    }
                                                                >
                                                                    {studentId ||
                                                                        "Student"}
                                                                </div>

                                                                <div
                                                                    style={
                                                                        roleStyle
                                                                    }
                                                                >
                                                                    Learner
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </td>

                                                    {/* Current Letter */}
                                                    <td style={tdStyle}>
                                                        <span
                                                            style={
                                                                letterBadgeStyle
                                                            }
                                                        >
                                                            {student.current_letter ||
                                                                "-"}
                                                        </span>
                                                    </td>

                                                    {/* Progress */}
                                                    <td style={tdStyle}>
                                                        <div
                                                            style={
                                                                progressContainerStyle
                                                            }
                                                        >
                                                            <div
                                                                style={
                                                                    progressTextStyle
                                                                }
                                                            >
                                                                {completed}/26
                                                            </div>

                                                            <div
                                                                style={
                                                                    progressBarBackgroundStyle
                                                                }
                                                            >
                                                                <div
                                                                    style={{
                                                                        ...progressBarStyle,
                                                                        width: `${Math.min(
                                                                            (completed /
                                                                                26) *
                                                                                100,
                                                                            100
                                                                        )}%`
                                                                    }}
                                                                />
                                                            </div>
                                                        </div>
                                                    </td>

                                                    {/* Accuracy */}
                                                    <td style={tdStyle}>
                                                        <span
                                                            style={{
                                                                ...accuracyBadgeStyle,
                                                                background:
                                                                    accuracy >=
                                                                    90
                                                                        ? "#ECFDF5"
                                                                        : accuracy >=
                                                                          60
                                                                        ? "#FFF7ED"
                                                                        : "#FEF2F2",
                                                                color:
                                                                    accuracy >=
                                                                    90
                                                                        ? "#15803D"
                                                                        : accuracy >=
                                                                          60
                                                                        ? "#C2410C"
                                                                        : "#DC2626"
                                                            }}
                                                        >
                                                            {accuracy}%
                                                        </span>
                                                    </td>

                                                    {/* Sessions */}
                                                    <td style={tdStyle}>
                                                        {student.total_sessions ??
                                                            0}
                                                    </td>

                                                    {/* Action */}
                                                    <td style={tdStyle}>
                                                        <button
                                                            type="button"
                                                            onClick={() =>
                                                                navigate(
                                                                    `/instructor/students/${studentId}`
                                                                )
                                                            }
                                                            style={
                                                                detailsButtonStyle
                                                            }
                                                        >
                                                            View Details →
                                                        </button>
                                                    </td>

                                                </tr>
                                            );
                                        }
                                    )}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>

            </div>
        </div>
    );
}


/* ============================================================
   STYLES
============================================================ */

const pageStyle = {
    minHeight: "100vh",
    background:
        "linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%)",
    padding: "32px 24px",
    boxSizing: "border-box"
};

const containerStyle = {
    width: "100%",
    maxWidth: "1400px",
    margin: "0 auto"
};

const headerStyle = {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "20px",
    marginBottom: "28px",
    flexWrap: "wrap"
};

const titleRowStyle = {
    display: "flex",
    alignItems: "center",
    gap: "14px"
};

const iconStyle = {
    width: "52px",
    height: "52px",
    borderRadius: "15px",
    background:
        "linear-gradient(135deg, #4F46E5, #7C3AED)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "24px"
};

const titleStyle = {
    margin: 0,
    fontSize: "30px",
    color: "#111827"
};

const subtitleStyle = {
    margin: "5px 0 0",
    color: "#6B7280",
    fontSize: "14px"
};

const backButtonStyle = {
    border: "1px solid #E5E7EB",
    background: "#FFFFFF",
    color: "#374151",
    borderRadius: "10px",
    padding: "10px 15px",
    fontSize: "13px",
    fontWeight: "600",
    cursor: "pointer"
};

const summaryStyle = {
    background: "#FFFFFF",
    border: "1px solid #E5E7EB",
    borderRadius: "16px",
    padding: "20px 24px",
    marginBottom: "22px",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    boxShadow: "0 4px 14px rgba(15, 23, 42, 0.05)"
};

const summaryLabelStyle = {
    color: "#6B7280",
    fontSize: "13px",
    fontWeight: "600"
};

const summaryValueStyle = {
    marginTop: "5px",
    fontSize: "28px",
    fontWeight: "700",
    color: "#111827"
};

const summaryIconStyle = {
    width: "44px",
    height: "44px",
    borderRadius: "12px",
    background: "#EEF2FF",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "20px"
};

const cardStyle = {
    background: "#FFFFFF",
    border: "1px solid #E5E7EB",
    borderRadius: "16px",
    overflow: "hidden",
    boxShadow: "0 4px 14px rgba(15, 23, 42, 0.05)"
};

const cardHeaderStyle = {
    padding: "20px 24px",
    borderBottom: "1px solid #EEF0F4",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "15px"
};

const cardTitleStyle = {
    margin: 0,
    fontSize: "18px",
    color: "#111827"
};

const cardSubtitleStyle = {
    margin: "4px 0 0",
    color: "#9CA3AF",
    fontSize: "13px"
};

const countBadgeStyle = {
    background: "#EEF2FF",
    color: "#4F46E5",
    padding: "7px 11px",
    borderRadius: "20px",
    fontSize: "12px",
    fontWeight: "700"
};

const tableWrapperStyle = {
    width: "100%",
    overflowX: "auto"
};

const tableStyle = {
    width: "100%",
    borderCollapse: "collapse",
    minWidth: "850px"
};

const thStyle = {
    padding: "14px 20px",
    textAlign: "left",
    fontSize: "11px",
    textTransform: "uppercase",
    color: "#9CA3AF",
    fontWeight: "700",
    background: "#F8FAFC",
    borderBottom: "1px solid #EEF0F4"
};

const tdStyle = {
    padding: "15px 20px",
    borderBottom: "1px solid #F1F3F5",
    fontSize: "13px",
    color: "#374151"
};

const avatarStyle = {
    width: "36px",
    height: "36px",
    borderRadius: "50%",
    background: "#EEF2FF",
    color: "#4F46E5",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: "700"
};

const studentNameStyle = {
    fontWeight: "600",
    color: "#1F2937"
};

const roleStyle = {
    marginTop: "2px",
    fontSize: "11px",
    color: "#9CA3AF"
};

const letterBadgeStyle = {
    display: "inline-flex",
    width: "30px",
    height: "30px",
    borderRadius: "8px",
    alignItems: "center",
    justifyContent: "center",
    background: "#F5F3FF",
    color: "#7C3AED",
    fontWeight: "700"
};

const progressContainerStyle = {
    minWidth: "100px"
};

const progressTextStyle = {
    fontSize: "12px",
    fontWeight: "600",
    marginBottom: "5px"
};

const progressBarBackgroundStyle = {
    width: "100px",
    height: "5px",
    background: "#E5E7EB",
    borderRadius: "10px",
    overflow: "hidden"
};

const progressBarStyle = {
    height: "100%",
    background: "#4F46E5",
    borderRadius: "10px"
};

const accuracyBadgeStyle = {
    padding: "6px 10px",
    borderRadius: "20px",
    fontSize: "12px",
    fontWeight: "700"
};

const detailsButtonStyle = {
    border: "none",
    background: "transparent",
    color: "#4F46E5",
    fontWeight: "700",
    fontSize: "12px",
    cursor: "pointer"
};

const emptyStyle = {
    padding: "50px",
    textAlign: "center",
    color: "#9CA3AF"
};

const messageStyle = {
    minHeight: "70vh",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    color: "#1F2937"
};