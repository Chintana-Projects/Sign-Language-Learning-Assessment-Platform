
import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    getInstructorDashboard,
    getInstructorStudents
} from "../../services/instructorDashboardService";


export default function InstructorReports() {

    const navigate = useNavigate();

    const [dashboard, setDashboard] = useState(null);
    const [students, setStudents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");


    // =====================================================
    // LOAD REPORT DATA
    // =====================================================

    useEffect(() => {

        async function loadReports() {

            try {

                setLoading(true);
                setError("");

                const [dashboardData, studentsData] =
                    await Promise.all([
                        getInstructorDashboard(),
                        getInstructorStudents()
                    ]);

                setDashboard(dashboardData);

                setStudents(
                    Array.isArray(studentsData)
                        ? studentsData
                        : []
                );

            } catch (err) {

                console.error(
                    "Failed to load instructor reports:",
                    err
                );

                setError(
                    "Unable to load instructor reports."
                );

            } finally {

                setLoading(false);

            }
        }

        loadReports();

    }, []);


    // =====================================================
    // CLASSROOM STATISTICS
    // =====================================================

    const totalStudents =
        Number(dashboard?.total_students ?? 0);

    const activeStudents =
        Number(dashboard?.active_students ?? 0);

    const completedStudents =
        Number(dashboard?.completed_students ?? 0);

    const averageAccuracy =
        Number(dashboard?.average_accuracy ?? 0);


    // =====================================================
    // TOTAL ATTEMPTS
    // =====================================================

    const totalAttempts = useMemo(() => {

        return students.reduce(
            (total, student) =>
                total +
                Number(student.total_attempts ?? 0),
            0
        );

    }, [students]);


    // =====================================================
    // CORRECT ATTEMPTS
    // =====================================================

    const correctAttempts = useMemo(() => {

        return students.reduce(
            (total, student) => {

                const attempts =
                    Array.isArray(
                        student.practice_history
                    )
                        ? student.practice_history
                        : [];

                return (
                    total +
                    attempts.filter(
                        attempt =>
                            attempt.correct === true
                    ).length
                );

            },
            0
        );

    }, [students]);


    // =====================================================
    // COMPLETION RATE
    // =====================================================

    const completionRate =
        totalStudents > 0
            ? Math.round(
                (completedStudents /
                    totalStudents) *
                100
            )
            : 0;


    // =====================================================
    // LETTER PERFORMANCE
    // =====================================================

    const letterPerformance = useMemo(() => {

        const letters = {};

        students.forEach(student => {

            const mastery =
                student.alphabet_mastery || {};

            Object.entries(mastery).forEach(
                ([letter, data]) => {

                    if (
                        !data ||
                        typeof data !== "object"
                    ) {
                        return;
                    }

                    const attempts =
                        Number(data.attempts ?? 0);

                    const accuracy =
                        Number(data.accuracy ?? 0);

                    if (!letters[letter]) {

                        letters[letter] = {
                            attempts: 0,
                            accuracyTotal: 0,
                            students: 0
                        };

                    }

                    letters[letter].attempts +=
                        attempts;

                    letters[letter].accuracyTotal +=
                        accuracy;

                    if (attempts > 0) {
                        letters[letter].students += 1;
                    }

                }
            );

        });


        return Object.entries(letters)
            .map(([letter, data]) => ({

                letter,

                attempts:
                    data.attempts,

                accuracy:
                    data.students > 0
                        ? data.accuracyTotal /
                          data.students
                        : 0

            }))
            .sort(
                (a, b) =>
                    b.attempts - a.attempts
            );

    }, [students]);


    // =====================================================
    // STUDENTS NEEDING ATTENTION
    // =====================================================

    const studentsNeedingAttention = useMemo(() => {

        return [...students]
            .filter(
                student =>
                    Number(student.accuracy ?? 0) < 60
            )
            .sort(
                (a, b) =>
                    Number(a.accuracy ?? 0) -
                    Number(b.accuracy ?? 0)
            );

    }, [students]);


    // =====================================================
    // RECENT ACTIVITY
    // =====================================================

    const recentActivity = useMemo(() => {

        const activity = [];

        students.forEach(student => {

            const history =
                Array.isArray(
                    student.practice_history
                )
                    ? student.practice_history
                    : [];

            history.forEach(attempt => {

                activity.push({

                    student:
                        student.student_id ||
                        "Student",

                    letter:
                        attempt.letter ||
                        attempt.expected_letter ||
                        "-",

                    correct:
                        attempt.correct === true,

                    confidence:
                        Number(
                            attempt.confidence ?? 0
                        ),

                    timestamp:
                        attempt.timestamp ||
                        attempt.created_at ||
                        student.last_updated ||
                        null

                });

            });

        });


        return activity
            .sort((a, b) => {

                const dateA =
                    a.timestamp
                        ? new Date(
                            a.timestamp
                        ).getTime()
                        : 0;

                const dateB =
                    b.timestamp
                        ? new Date(
                            b.timestamp
                        ).getTime()
                        : 0;

                return dateB - dateA;

            })
            .slice(0, 8);

    }, [students]);


    // =====================================================
    // LOADING
    // =====================================================

    if (loading) {

        return (
            <div style={pageStyle}>

                <div style={centerStyle}>

                    <div style={loadingIconStyle}>
                        ⟳
                    </div>

                    <h2 style={{ margin: "12px 0 5px" }}>
                        Loading Instructor Reports
                    </h2>

                    <p style={mutedTextStyle}>
                        Analyzing classroom performance...
                    </p>

                </div>

            </div>
        );
    }


    // =====================================================
    // ERROR
    // =====================================================

    if (error) {

        return (
            <div style={pageStyle}>

                <div style={centerStyle}>

                    <div style={{ fontSize: "42px" }}>
                        ⚠️
                    </div>

                    <h2 style={{ margin: "12px 0 5px" }}>
                        Something went wrong
                    </h2>

                    <p style={mutedTextStyle}>
                        {error}
                    </p>

                    <button
                        onClick={() => navigate(-1)}
                        style={backButtonStyle}
                    >
                        ← Back
                    </button>

                </div>

            </div>
        );
    }


    // =====================================================
    // PAGE
    // =====================================================

    return (

        <div style={pageStyle}>

            <div style={containerStyle}>

                {/* =================================================
                    BACK BUTTON
                ================================================= */}

                <button
                    onClick={() => navigate(-1)}
                    style={backButtonStyle}
                >
                    ← Back
                </button>


                {/* =================================================
                    HEADER
                ================================================= */}

                <div style={headerStyle}>

                    <div>

                        <div style={eyebrowStyle}>
                            INSTRUCTOR ANALYTICS
                        </div>

                        <h1 style={titleStyle}>
                            Instructor Reports
                        </h1>

                        <p style={descriptionStyle}>
                            Analyze learner performance,
                            classroom progress, and practice
                            activity.
                        </p>

                    </div>

                    <div style={headerBadgeStyle}>
                        📊 Classroom Analytics
                    </div>

                </div>


                {/* =================================================
                    OVERVIEW
                ================================================= */}

                <section>

                    <div style={sectionHeadingStyle}>

                        <div>

                            <h2 style={sectionTitleStyle}>
                                Classroom Overview
                            </h2>

                            <p style={sectionSubtitleStyle}>
                                Overall learning performance
                            </p>

                        </div>

                    </div>


                    <div style={statsGridStyle}>

                        <ReportCard
                            icon="👥"
                            title="Total Students"
                            value={totalStudents}
                            description="Registered learners"
                            background="#EEF2FF"
                        />

                        <ReportCard
                            icon="📝"
                            title="Total Attempts"
                            value={totalAttempts}
                            description="Practice attempts"
                            background="#EFF6FF"
                        />

                        <ReportCard
                            icon="🎯"
                            title="Average Accuracy"
                            value={`${averageAccuracy}%`}
                            description="Overall class accuracy"
                            background="#F5F3FF"
                        />

                        <ReportCard
                            icon="🏆"
                            title="Completed"
                            value={completedStudents}
                            description={`${completionRate}% completion rate`}
                            background="#FFF7ED"
                        />

                    </div>

                </section>


                {/* =================================================
                    PERFORMANCE SUMMARY
                ================================================= */}

                <section style={cardStyle}>

                    <div style={cardHeaderStyle}>

                        <div>

                            <h2 style={cardTitleStyle}>
                                Performance Summary
                            </h2>

                            <p style={cardSubtitleStyle}>
                                Current classroom performance
                            </p>

                        </div>

                    </div>


                    <div style={summaryGridStyle}>

                        <SummaryItem
                            label="Active Students"
                            value={activeStudents}
                            icon="🟢"
                        />

                        <SummaryItem
                            label="Correct Attempts"
                            value={correctAttempts}
                            icon="✓"
                        />

                        <SummaryItem
                            label="Completion Rate"
                            value={`${completionRate}%`}
                            icon="🏆"
                        />

                        <SummaryItem
                            label="Students Needing Attention"
                            value={
                                studentsNeedingAttention.length
                            }
                            icon="⚠️"
                        />

                    </div>

                </section>


                {/* =================================================
                    LETTER PERFORMANCE
                ================================================= */}

                <section style={cardStyle}>

                    <div style={cardHeaderStyle}>

                        <div>

                            <h2 style={cardTitleStyle}>
                                Letter Performance
                            </h2>

                            <p style={cardSubtitleStyle}>
                                Practice activity across
                                sign language letters
                            </p>

                        </div>

                    </div>


                    {letterPerformance.length === 0 ? (

                        <EmptyState
                            icon="✋"
                            text="No letter practice data available yet."
                        />

                    ) : (

                        <div style={letterGridStyle}>

                            {letterPerformance.map(
                                item => (

                                    <div
                                        key={item.letter}
                                        style={letterItemStyle}
                                    >

                                        <div
                                            style={{
                                                display: "flex",
                                                justifyContent:
                                                    "space-between",
                                                alignItems:
                                                    "center",
                                                marginBottom:
                                                    "8px"
                                            }}
                                        >

                                            <strong
                                                style={{
                                                    fontSize: "17px",
                                                    color: "#111827"
                                                }}
                                            >
                                                {item.letter}
                                            </strong>

                                            <span
                                                style={{
                                                    fontSize: "12px",
                                                    color: "#6b7280"
                                                }}
                                            >
                                                {Math.round(
                                                    item.accuracy
                                                )}%
                                            </span>

                                        </div>


                                        <div
                                            style={
                                                progressTrackStyle
                                            }
                                        >

                                            <div
                                                style={{
                                                    ...progressFillStyle,
                                                    width: `${Math.min(
                                                        100,
                                                        Math.max(
                                                            0,
                                                            item.accuracy
                                                        )
                                                    )}%`
                                                }}
                                            />

                                        </div>


                                        <div
                                            style={{
                                                marginTop: "7px",
                                                fontSize: "11px",
                                                color: "#9ca3af"
                                            }}
                                        >
                                            {item.attempts} attempts
                                        </div>

                                    </div>

                                )
                            )}

                        </div>

                    )}

                </section>


                {/* =================================================
                    ATTENTION NEEDED
                ================================================= */}

                <section style={cardStyle}>

                    <div style={cardHeaderStyle}>

                        <div>

                            <h2 style={cardTitleStyle}>
                                Students Needing Attention
                            </h2>

                            <p style={cardSubtitleStyle}>
                                Learners with accuracy below 60%
                            </p>

                        </div>

                        <div style={warningBadgeStyle}>
                            {studentsNeedingAttention.length}
                        </div>

                    </div>


                    {studentsNeedingAttention.length === 0 ? (

                        <EmptyState
                            icon="✓"
                            text="All students are currently performing well."
                        />

                    ) : (

                        <div>

                            {studentsNeedingAttention
                                .slice(0, 6)
                                .map(
                                    (student, index) => (

                                        <div
                                            key={
                                                student.student_id ||
                                                `student-${index}`
                                            }
                                            style={
                                                attentionRowStyle
                                            }
                                        >

                                            <div
                                                style={
                                                    studentAvatarStyle
                                                }
                                            >
                                                {String(
                                                    student.student_id ||
                                                    "S"
                                                )
                                                    .charAt(0)
                                                    .toUpperCase()}
                                            </div>

                                            <div
                                                style={{
                                                    flex: 1
                                                }}
                                            >

                                                <div
                                                    style={{
                                                        fontWeight:
                                                            "600",
                                                        color:
                                                            "#1f2937"
                                                    }}
                                                >
                                                    {
                                                        student.student_id ||
                                                        "Student"
                                                    }
                                                </div>

                                                <div
                                                    style={{
                                                        fontSize:
                                                            "12px",
                                                        color:
                                                            "#9ca3af",
                                                        marginTop:
                                                            "3px"
                                                    }}
                                                >
                                                    Current letter:{" "}
                                                    {
                                                        student.current_letter ||
                                                        "-"
                                                    }
                                                </div>

                                            </div>

                                            <div
                                                style={
                                                    accuracyBadgeStyle
                                                }
                                            >
                                                {Number(
                                                    student.accuracy ??
                                                    0
                                                ).toFixed(2)}
                                                %
                                            </div>

                                        </div>

                                    )
                                )}

                        </div>

                    )}

                </section>


                {/* =================================================
                    RECENT ACTIVITY
                ================================================= */}

                <section style={cardStyle}>

                    <div style={cardHeaderStyle}>

                        <div>

                            <h2 style={cardTitleStyle}>
                                Recent Practice Activity
                            </h2>

                            <p style={cardSubtitleStyle}>
                                Latest learner practice attempts
                            </p>

                        </div>

                    </div>


                    {recentActivity.length === 0 ? (

                        <EmptyState
                            icon="✋"
                            text="No practice activity available yet."
                        />

                    ) : (

                        <div style={activityListStyle}>

                            {recentActivity.map(
                                (item, index) => (

                                    <div
                                        key={`activity-${index}`}
                                        style={
                                            activityRowStyle
                                        }
                                    >

                                        <div
                                            style={{
                                                fontSize: "20px"
                                            }}
                                        >
                                            {item.correct
                                                ? "✓"
                                                : "✕"}
                                        </div>

                                        <div
                                            style={{
                                                flex: 1
                                            }}
                                        >

                                            <div
                                                style={{
                                                    fontWeight:
                                                        "600",
                                                    color:
                                                        "#1f2937"
                                                }}
                                            >
                                                {item.student}
                                            </div>

                                            <div
                                                style={{
                                                    fontSize:
                                                        "12px",
                                                    color:
                                                        "#9ca3af",
                                                    marginTop:
                                                        "3px"
                                                }}
                                            >
                                                Letter:{" "}
                                                {item.letter}
                                            </div>

                                        </div>

                                        <div
                                            style={{
                                                textAlign:
                                                    "right"
                                            }}
                                        >

                                            <div
                                                style={{
                                                    fontSize:
                                                        "13px",
                                                    fontWeight:
                                                        "600",
                                                    color:
                                                        item.correct
                                                            ? "#15803D"
                                                            : "#DC2626"
                                                }}
                                            >
                                                {item.correct
                                                    ? "Correct"
                                                    : "Incorrect"}
                                            </div>

                                            {item.timestamp && (

                                                <div
                                                    style={{
                                                        fontSize:
                                                            "11px",
                                                        color:
                                                            "#9ca3af",
                                                        marginTop:
                                                            "3px"
                                                    }}
                                                >
                                                    {formatDate(
                                                        item.timestamp
                                                    )}
                                                </div>

                                            )}

                                        </div>

                                    </div>

                                )
                            )}

                        </div>

                    )}

                </section>

            </div>

        </div>
    );
}


// =============================================================
// REPORT CARD
// =============================================================

function ReportCard({
    icon,
    title,
    value,
    description,
    background
}) {

    return (
        <div style={reportCardStyle}>

            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "flex-start"
                }}
            >

                <div>

                    <div style={smallLabelStyle}>
                        {title}
                    </div>

                    <div style={bigValueStyle}>
                        {value}
                    </div>

                    <div style={smallDescriptionStyle}>
                        {description}
                    </div>

                </div>

                <div
                    style={{
                        ...reportIconStyle,
                        background
                    }}
                >
                    {icon}
                </div>

            </div>

        </div>
    );
}


// =============================================================
// SUMMARY ITEM
// =============================================================

function SummaryItem({
    label,
    value,
    icon
}) {

    return (
        <div style={summaryItemStyle}>

            <div style={summaryIconStyle}>
                {icon}
            </div>

            <div>

                <div style={summaryLabelStyle}>
                    {label}
                </div>

                <div style={summaryValueStyle}>
                    {value}
                </div>

            </div>

        </div>
    );
}


// =============================================================
// EMPTY STATE
// =============================================================

function EmptyState({
    icon,
    text
}) {

    return (
        <div style={emptyStateStyle}>

            <div style={{ fontSize: "28px" }}>
                {icon}
            </div>

            <span>
                {text}
            </span>

        </div>
    );
}


// =============================================================
// DATE FORMAT
// =============================================================

function formatDate(value) {

    try {

        const date = new Date(value);

        if (Number.isNaN(date.getTime())) {
            return String(value);
        }

        return date.toLocaleString(
            "en-IN",
            {
                day: "2-digit",
                month: "short",
                year: "numeric",
                hour: "2-digit",
                minute: "2-digit"
            }
        );

    } catch {

        return String(value);

    }
}


// =============================================================
// STYLES
// =============================================================

const pageStyle = {
    minHeight: "100vh",
    background:
        "linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%)",
    padding: "28px 24px",
    boxSizing: "border-box"
};


const containerStyle = {
    width: "100%",
    maxWidth: "1600px",
    margin: "0 auto"
};


// =============================================================
// BACK BUTTON
// =============================================================

const backButtonStyle = {
    border: "1px solid #e5e7eb",
    background: "#ffffff",
    color: "#4F46E5",
    borderRadius: "10px",
    padding: "9px 15px",
    fontSize: "13px",
    fontWeight: "600",
    cursor: "pointer",
    marginBottom: "20px",
    boxShadow:
        "0 3px 10px rgba(15, 23, 42, 0.06)"
};


const centerStyle = {
    minHeight: "70vh",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    textAlign: "center",
    color: "#1f2937"
};


const loadingIconStyle = {
    fontSize: "42px",
    color: "#4F46E5",
    animation:
        "spin 1s linear infinite"
};


const headerStyle = {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    gap: "20px",
    marginBottom: "30px",
    flexWrap: "wrap"
};


const eyebrowStyle = {
    fontSize: "11px",
    fontWeight: "800",
    letterSpacing: "1.4px",
    color: "#6366F1",
    marginBottom: "7px"
};


const titleStyle = {
    margin: 0,
    fontSize: "30px",
    lineHeight: "1.2",
    fontWeight: "750",
    letterSpacing: "-0.5px",
    color: "#111827"
};


const descriptionStyle = {
    margin: "8px 0 0",
    color: "#6B7280",
    fontSize: "14px"
};


const headerBadgeStyle = {
    background: "#ffffff",
    border: "1px solid #e5e7eb",
    borderRadius: "999px",
    padding: "9px 15px",
    fontSize: "13px",
    fontWeight: "600",
    color: "#4b5563",
    boxShadow:
        "0 3px 10px rgba(15, 23, 42, 0.05)"
};


const sectionHeadingStyle = {
    marginBottom: "15px"
};


const sectionTitleStyle = {
    margin: 0,
    fontSize: "19px",
    color: "#111827"
};


const sectionSubtitleStyle = {
    margin: "4px 0 0",
    fontSize: "13px",
    color: "#9ca3af"
};


const statsGridStyle = {
    display: "grid",
    gridTemplateColumns:
        "repeat(auto-fit, minmax(220px, 1fr))",
    gap: "18px",
    marginBottom: "28px"
};


const reportCardStyle = {
    background: "#ffffff",
    border: "1px solid #e5e7eb",
    borderRadius: "16px",
    padding: "22px",
    boxShadow:
        "0 4px 14px rgba(15, 23, 42, 0.06)"
};


const smallLabelStyle = {
    fontSize: "13px",
    fontWeight: "600",
    color: "#6b7280"
};


const bigValueStyle = {
    marginTop: "9px",
    fontSize: "30px",
    lineHeight: 1,
    fontWeight: "700",
    color: "#111827"
};


const smallDescriptionStyle = {
    marginTop: "7px",
    fontSize: "12px",
    color: "#9ca3af"
};


const reportIconStyle = {
    width: "46px",
    height: "46px",
    borderRadius: "13px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "21px"
};


const cardStyle = {
    background: "#ffffff",
    border: "1px solid #e5e7eb",
    borderRadius: "16px",
    boxShadow:
        "0 4px 14px rgba(15, 23, 42, 0.06)",
    marginBottom: "28px",
    overflow: "hidden"
};


const cardHeaderStyle = {
    padding: "20px 24px",
    borderBottom: "1px solid #eef0f4",
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
    fontSize: "13px",
    color: "#9ca3af"
};


const summaryGridStyle = {
    display: "grid",
    gridTemplateColumns:
        "repeat(auto-fit, minmax(180px, 1fr))",
    gap: "14px",
    padding: "20px 24px"
};


const summaryItemStyle = {
    display: "flex",
    alignItems: "center",
    gap: "12px",
    padding: "15px",
    borderRadius: "12px",
    background: "#F8FAFC",
    border: "1px solid #eef0f4"
};


const summaryIconStyle = {
    width: "36px",
    height: "36px",
    borderRadius: "10px",
    background: "#EEF2FF",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "16px"
};


const summaryLabelStyle = {
    fontSize: "11px",
    color: "#9ca3af",
    fontWeight: "600"
};


const summaryValueStyle = {
    marginTop: "3px",
    fontSize: "18px",
    fontWeight: "700",
    color: "#1f2937"
};


const letterGridStyle = {
    display: "grid",
    gridTemplateColumns:
        "repeat(auto-fill, minmax(180px, 1fr))",
    gap: "14px",
    padding: "20px 24px"
};


const letterItemStyle = {
    padding: "15px",
    borderRadius: "12px",
    border: "1px solid #eef0f4",
    background: "#ffffff"
};


const progressTrackStyle = {
    width: "100%",
    height: "7px",
    borderRadius: "999px",
    background: "#E5E7EB",
    overflow: "hidden"
};


const progressFillStyle = {
    height: "100%",
    borderRadius: "999px",
    background:
        "linear-gradient(90deg, #4F46E5, #7C3AED)"
};


const warningBadgeStyle = {
    minWidth: "28px",
    height: "28px",
    padding: "0 8px",
    borderRadius: "999px",
    background: "#FEF2F2",
    color: "#DC2626",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "12px",
    fontWeight: "700"
};


const attentionRowStyle = {
    display: "flex",
    alignItems: "center",
    gap: "13px",
    padding: "15px 24px",
    borderBottom: "1px solid #f1f3f5"
};


const studentAvatarStyle = {
    width: "38px",
    height: "38px",
    borderRadius: "50%",
    background: "#FEF2F2",
    color: "#DC2626",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: "700",
    flexShrink: 0
};


const accuracyBadgeStyle = {
    padding: "6px 10px",
    borderRadius: "20px",
    background: "#FEF2F2",
    color: "#DC2626",
    fontSize: "12px",
    fontWeight: "700"
};


const activityListStyle = {
    padding: 0
};


const activityRowStyle = {
    display: "flex",
    alignItems: "center",
    gap: "14px",
    padding: "15px 24px",
    borderBottom: "1px solid #f1f3f5"
};


const emptyStateStyle = {
    minHeight: "130px",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    gap: "8px",
    color: "#6b7280",
    fontSize: "13px"
};


const mutedTextStyle = {
    margin: 0,
    color: "#9ca3af"
};
