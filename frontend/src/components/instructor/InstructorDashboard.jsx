import { useEffect, useState } from "react";

import InstructorHeader from "./InstructorHeader";
import InstructorStats from "./InstructorStats";
import StudentsTable from "./StudentsTable";

import { getInstructorDashboard } from "../../services/instructorDashboardService";

export default function InstructorDashboard() {
    const [dashboard, setDashboard] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        async function loadDashboard() {
            try {
                setLoading(true);
                setError("");

                const data = await getInstructorDashboard();

                setDashboard(data);
            } catch (err) {
                console.error(
                    "Failed to load instructor dashboard:",
                    err
                );

                setError(
                    "Unable to load instructor dashboard."
                );
            } finally {
                setLoading(false);
            }
        }

        loadDashboard();
    }, []);

    if (loading) {
        return (
            <div style={pageStyle}>
                <div style={centerMessageStyle}>
                    <div style={spinnerStyle}>⟳</div>

                    <h2 style={{ margin: "10px 0 5px" }}>
                        Loading Instructor Dashboard
                    </h2>

                    <p style={{ margin: 0, color: "#9ca3af" }}>
                        Fetching student progress...
                    </p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div style={pageStyle}>
                <div style={centerMessageStyle}>
                    <div
                        style={{
                            fontSize: "42px",
                            marginBottom: "10px"
                        }}
                    >
                        ⚠️
                    </div>

                    <h2 style={{ margin: "0 0 8px" }}>
                        Something went wrong
                    </h2>

                    <p style={{ margin: 0, color: "#6b7280" }}>
                        {error}
                    </p>
                </div>
            </div>
        );
    }

    if (!dashboard) {
        return (
            <div style={pageStyle}>
                <div style={centerMessageStyle}>
                    <div
                        style={{
                            fontSize: "42px",
                            marginBottom: "10px"
                        }}
                    >
                        📊
                    </div>

                    <h2 style={{ margin: "0 0 8px" }}>
                        No dashboard data
                    </h2>

                    <p style={{ margin: 0, color: "#6b7280" }}>
                        There is currently no instructor
                        dashboard information available.
                    </p>
                </div>
            </div>
        );
    }

    const students = dashboard.students || [];

    const studentsNeedingAttention = students
        .filter(
            (student) =>
                Number(student.accuracy ?? 0) < 60
        )
        .sort(
            (a, b) =>
                Number(a.accuracy ?? 0) -
                Number(b.accuracy ?? 0)
        );

    return (
        <div style={pageStyle}>
            <div style={dashboardContainerStyle}>

                <InstructorHeader />

                <InstructorStats
                    dashboard={dashboard}
                />

                {/* Attention Needed */}
                <AttentionSection
                    students={studentsNeedingAttention}
                />

                {/* Student Progress */}
                <StudentsTable
                    students={students}
                />

            </div>
        </div>
    );
}


/* ============================================
   ATTENTION NEEDED SECTION
============================================ */

function AttentionSection({ students }) {
    return (
        <div
            style={{
                background: "#ffffff",
                borderRadius: "16px",
                border: "1px solid #e5e7eb",
                boxShadow:
                    "0 4px 14px rgba(15, 23, 42, 0.06)",
                marginBottom: "28px",
                overflow: "hidden"
            }}
        >
            {/* Section Header */}
            <div
                style={{
                    padding: "20px 24px",
                    borderBottom:
                        "1px solid #eef0f4",
                    display: "flex",
                    alignItems: "center",
                    gap: "12px"
                }}
            >
                <div
                    style={{
                        width: "40px",
                        height: "40px",
                        borderRadius: "11px",
                        background: "#FEF2F2",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        fontSize: "19px"
                    }}
                >
                    ⚠️
                </div>

                <div>
                    <h2
                        style={{
                            margin: 0,
                            fontSize: "18px",
                            color: "#111827"
                        }}
                    >
                        Attention Needed
                    </h2>

                    <p
                        style={{
                            margin: "4px 0 0",
                            color: "#9ca3af",
                            fontSize: "13px"
                        }}
                    >
                        Learners who may need additional practice
                    </p>
                </div>
            </div>

            {/* Students */}
            {students.length === 0 ? (
                <div
                    style={{
                        padding: "25px",
                        display: "flex",
                        alignItems: "center",
                        gap: "12px",
                        color: "#15803D"
                    }}
                >
                    <span style={{ fontSize: "22px" }}>
                        ✓
                    </span>

                    <div>
                        <strong>
                            All students are doing well!
                        </strong>

                        <div
                            style={{
                                fontSize: "13px",
                                color: "#6b7280",
                                marginTop: "3px"
                            }}
                        >
                            No learners currently require
                            immediate attention.
                        </div>
                    </div>
                </div>
            ) : (
                <div>
                    {students.map((student, index) => (
                        <AttentionStudent
                            key={
                                student.student_id ||
                                `attention-${index}`
                            }
                            student={student}
                        />
                    ))}
                </div>
            )}
        </div>
    );
}


/* ============================================
   ATTENTION STUDENT
============================================ */

function AttentionStudent({ student }) {
    const accuracy =
        Number(student.accuracy ?? 0);

    const completed =
        Number(student.completed_letters ?? 0);

    const studentName =
        student.student_id || "Student";

    return (
        <div
            style={{
                padding: "16px 24px",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                gap: "20px",
                borderBottom:
                    "1px solid #f1f3f5",
                flexWrap: "wrap"
            }}
        >
            <div
                style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "12px"
                }}
            >
                <div
                    style={{
                        width: "38px",
                        height: "38px",
                        borderRadius: "50%",
                        background: "#FEF2F2",
                        color: "#DC2626",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        fontWeight: "700"
                    }}
                >
                    {String(studentName)
                        .charAt(0)
                        .toUpperCase()}
                </div>

                <div>
                    <div
                        style={{
                            fontWeight: "600",
                            color: "#1f2937"
                        }}
                    >
                        {studentName}
                    </div>

                    <div
                        style={{
                            fontSize: "12px",
                            color: "#9ca3af"
                        }}
                    >
                        Current letter:{" "}
                        {student.current_letter || "-"}
                    </div>
                </div>
            </div>

            <div
                style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "28px"
                }}
            >
                <div style={{ textAlign: "right" }}>
                    <div
                        style={{
                            fontSize: "11px",
                            color: "#9ca3af",
                            textTransform: "uppercase",
                            fontWeight: "600"
                        }}
                    >
                        Progress
                    </div>

                    <div
                        style={{
                            fontSize: "13px",
                            color: "#4b5563",
                            fontWeight: "600"
                        }}
                    >
                        {completed}/26 letters
                    </div>
                </div>

                <div
                    style={{
                        padding: "6px 11px",
                        borderRadius: "20px",
                        background: "#FEF2F2",
                        color: "#DC2626",
                        fontWeight: "700",
                        fontSize: "13px"
                    }}
                >
                    {accuracy}%
                </div>
            </div>
        </div>
    );
}


/* ============================================
   PAGE
============================================ */

const pageStyle = {
    minHeight: "100vh",
    background:
        "linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%)",
    padding: "32px 24px",
    boxSizing: "border-box"
};


/* ============================================
   DASHBOARD CONTAINER
============================================ */

const dashboardContainerStyle = {
    width: "100%",
    maxWidth: "1400px",
    margin: "0 auto"
};


/* ============================================
   LOADING / ERROR / EMPTY STATE
============================================ */

const centerMessageStyle = {
    minHeight: "70vh",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    textAlign: "center",
    color: "#1f2937"
};


const spinnerStyle = {
    fontSize: "42px",
    color: "#4F46E5",
    animation: "spin 1s linear infinite"
};