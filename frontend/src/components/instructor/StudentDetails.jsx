import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { getStudentDetails } from "../../services/instructorDashboardService";

export default function StudentDetails() {
const { studentId } = useParams();
const navigate = useNavigate();


const [student, setStudent] = useState(null);
const [loading, setLoading] = useState(true);
const [error, setError] = useState("");

/* =========================================
   LOAD STUDENT
========================================= */

useEffect(() => {
    async function loadStudent() {
        try {
            setLoading(true);
            setError("");

            const data = await getStudentDetails(studentId);

            setStudent(data);
        } catch (err) {
            console.error(
                "Failed to load student details:",
                err
            );

            setError(
                "Unable to load student details."
            );
        } finally {
            setLoading(false);
        }
    }

    if (studentId) {
        loadStudent();
    } else {
        setLoading(false);
        setError("Student ID is missing.");
    }
}, [studentId]);

/* =========================================
   LOADING
========================================= */

if (loading) {
    return (
        <div style={pageStyle}>
            <div style={centerStyle}>
                <div style={loadingIconStyle}>
                    ⟳
                </div>

                <h2 style={{ margin: "12px 0 5px" }}>
                    Loading Student Details
                </h2>

                <p style={mutedCenterTextStyle}>
                    Fetching learner performance...
                </p>
            </div>
        </div>
    );
}

/* =========================================
   ERROR
========================================= */

if (error) {
    return (
        <div style={pageStyle}>
            <div style={centerStyle}>
                <div style={errorIconStyle}>
                    ⚠️
                </div>

                <h2 style={{ margin: "0 0 8px" }}>
                    Unable to Load Student
                </h2>

                <p style={mutedCenterTextStyle}>
                    {error}
                </p>

                <button
                    type="button"
                    onClick={() =>
                        navigate(
                            "/instructor/dashboard"
                        )
                    }
                    style={backButtonStyle}
                >
                    ← Back to Dashboard
                </button>
            </div>
        </div>
    );
}

if (!student) {
    return null;
}

/* =========================================
   DATA
========================================= */

const completedLetters =
    student.completed_letters || [];

const mastery =
    student.alphabet_mastery || {};

const history =
    student.practice_history || [];

const weakLetters =
    student.weak_letters || [];

const strongLetters =
    student.strong_letters || [];

const recommendations =
    student.recommendations || [];

const completedCount =
    Number(
        student.completed_count ??
        completedLetters.length
    );

const accuracy =
    Number(
        student.accuracy ?? 0
    );

const totalAttempts =
    Number(
        student.total_attempts ??
        history.length
    );

const totalSessions =
    Number(
        student.total_sessions ?? 0
    );

const progress =
    Math.min(
        (completedCount / 26) * 100,
        100
    );

const studentName =
    student.student_id ||
    studentId ||
    "Student";

const isCompleted =
    completedCount >= 26;

/* =========================================
   PAGE
========================================= */

return (
    <div style={pageStyle}>
        <div style={containerStyle}>

            {/* =====================================
                HEADER
            ===================================== */}

            <div style={headerStyleContainer}>

                <button
                    type="button"
                    onClick={() =>
                        navigate(
                            "/instructor/dashboard"
                        )
                    }
                    style={backLinkStyle}
                >
                    ← Back to Dashboard
                </button>

                <div style={profileHeaderStyle}>

                    <div style={studentAvatarStyle}>
                        {String(studentName)
                            .charAt(0)
                            .toUpperCase()}
                    </div>

                    <div style={{ flex: 1 }}>

                        <div style={titleRowStyle}>

                            <div>
                                <h1 style={pageTitleStyle}>
                                    Student Details
                                </h1>

                                <p style={studentIdStyle}>
                                    Student ID:{" "}
                                    <strong>
                                        {studentName}
                                    </strong>
                                </p>
                            </div>

                            <div
                                style={
                                    isCompleted
                                        ? completedStatusStyle
                                        : activeStatusStyle
                                }
                            >
                                <span>
                                    {isCompleted
                                        ? "✓"
                                        : "●"}
                                </span>

                                {isCompleted
                                    ? "Alphabet Completed"
                                    : "Learning Active"}
                            </div>

                        </div>

                    </div>

                </div>
            </div>


            {/* =====================================
                SUMMARY CARDS
            ===================================== */}

            <div style={summaryGridStyle}>

                <SummaryCard
                    title="Accuracy"
                    value={`${accuracy}%`}
                    description="Overall performance"
                    icon="🎯"
                    iconBackground="#F5F3FF"
                />

                <SummaryCard
                    title="Total Attempts"
                    value={totalAttempts}
                    description="Practice attempts"
                    icon="📊"
                    iconBackground="#EEF2FF"
                />

                <SummaryCard
                    title="Total Sessions"
                    value={totalSessions}
                    description="Practice sessions"
                    icon="📝"
                    iconBackground="#ECFDF5"
                />

                <SummaryCard
                    title="Progress"
                    value={`${completedCount}/26`}
                    description="Letters completed"
                    icon="🏆"
                    iconBackground="#FFF7ED"
                />

            </div>


            {/* =====================================
                ALPHABET PROGRESS
            ===================================== */}

            <section style={cardStyle}>

                <SectionHeader
                    eyebrow="PROGRESS"
                    title="Alphabet Progress"
                    description="Track the learner's journey through the ASL alphabet."
                />

                <div style={progressSummaryStyle}>

                    <div>
                        <span style={progressLabelStyle}>
                            Letters completed
                        </span>

                        <strong
                            style={
                                progressCountStyle
                            }
                        >
                            {completedCount}/26
                        </strong>
                    </div>

                    <div
                        style={
                            progressPercentageStyle
                        }
                    >
                        {Math.round(progress)}%
                    </div>

                </div>

                <div style={progressTrackStyle}>
                    <div
                        style={{
                            ...progressFillStyle,
                            width: `${progress}%`
                        }}
                    />
                </div>

                <div style={lettersContainerStyle}>

                    {Array.from(
                        { length: 26 },
                        (_, index) =>
                            String.fromCharCode(
                                65 + index
                            )
                    ).map((letter) => {

                        const completed =
                            completedLetters.includes(
                                letter
                            );

                        return (
                            <div
                                key={letter}
                                title={
                                    completed
                                        ? `${letter} completed`
                                        : `${letter} not completed`
                                }
                                style={
                                    completed
                                        ? completedLetterStyle
                                        : incompleteLetterStyle
                                }
                            >
                                {letter}
                            </div>
                        );
                    })}

                </div>

            </section>


            {/* =====================================
                CURRENT LEARNING + STRENGTHS
            ===================================== */}

            <div style={twoColumnStyle}>

                {/* CURRENT LEARNING */}

                <section style={cardStyle}>

                    <SectionHeader
                        eyebrow="CURRENT LEARNING"
                        title="Learning Status"
                    />

                    <div style={infoGridStyle}>

                        <InfoItem
                            label="Current Letter"
                            value={
                                isCompleted
                                    ? "COMPLETED"
                                    : student.current_letter ||
                                      "-"
                            }
                        />

                        <InfoItem
                            label="Next Letter"
                            value={
                                isCompleted
                                    ? "COMPLETED"
                                    : student.next_letter ||
                                      "-"
                            }
                        />

                        <InfoItem
                            label="Completed"
                            value={`${completedCount} letters`}
                        />

                        <InfoItem
                            label="Accuracy"
                            value={`${accuracy}%`}
                        />

                    </div>

                </section>


                {/* STRONG LETTERS */}

                <section style={cardStyle}>

                    <SectionHeader
                        eyebrow="STRENGTHS"
                        title="Strong Letters"
                    />

                    {strongLetters.length === 0 ? (

                        <div style={emptyStateStyle}>
                            <span style={emptyStateIconStyle}>
                                💪
                            </span>

                            <span>
                                No strong letters identified yet.
                            </span>
                        </div>

                    ) : (

                        <div style={lettersContainerStyle}>

                            {strongLetters.map(
                                (letter) => (
                                    <span
                                        key={letter}
                                        style={
                                            strongLetterStyle
                                        }
                                    >
                                        {letter}
                                    </span>
                                )
                            )}

                        </div>
                    )}

                </section>

            </div>


            {/* =====================================
                WEAK LETTERS
            ===================================== */}

            <section style={cardStyle}>

                <SectionHeader
                    eyebrow="FOCUS AREAS"
                    title="Letters to Improve"
                    description="Letters where the learner may benefit from additional practice."
                />

                {weakLetters.length === 0 ? (

                    <div style={successBoxStyle}>
                        <span
                            style={{
                                fontSize: "18px"
                            }}
                        >
                            ✓
                        </span>

                        <div>
                            <strong>
                                No weak letters identified.
                            </strong>

                            <div
                                style={{
                                    fontSize: "12px",
                                    marginTop: "2px",
                                    color: "#166534"
                                }}
                            >
                                The learner is performing consistently.
                            </div>
                        </div>
                    </div>

                ) : (

                    <div style={weakLettersGridStyle}>

                        {weakLetters.map(
                            (letter) => {

                                const data =
                                    mastery[
                                        letter
                                    ] || {};

                                const letterAccuracy =
                                    Number(
                                        data.accuracy ??
                                        0
                                    );

                                const attempts =
                                    Number(
                                        data.attempts ??
                                        0
                                    );

                                return (
                                    <div
                                        key={letter}
                                        style={
                                            weakLetterCardStyle
                                        }
                                    >

                                        <div
                                            style={
                                                weakCardTopStyle
                                            }
                                        >

                                            <div
                                                style={
                                                    weakLetterSymbolStyle
                                                }
                                            >
                                                {letter}
                                            </div>

                                            <div
                                                style={
                                                    weakAccuracyStyle
                                                }
                                            >
                                                {letterAccuracy}%
                                            </div>

                                        </div>

                                        <div
                                            style={
                                                weakProgressTrackStyle
                                            }
                                        >
                                            <div
                                                style={{
                                                    ...weakProgressFillStyle,
                                                    width: `${Math.min(
                                                        letterAccuracy,
                                                        100
                                                    )}%`
                                                }}
                                            />
                                        </div>

                                        <p
                                            style={
                                                attemptsTextStyle
                                            }
                                        >
                                            {attempts} attempt
                                            {attempts !== 1
                                                ? "s"
                                                : ""}
                                        </p>

                                    </div>
                                );
                            }
                        )}

                    </div>
                )}

            </section>


            {/* =====================================
                RECOMMENDATIONS
            ===================================== */}

            {recommendations.length > 0 && (

                <section style={cardStyle}>

                    <SectionHeader
                        eyebrow="RECOMMENDATIONS"
                        title="Suggested Practice"
                        description="Personalized suggestions based on learner performance."
                    />

                    <div>

                        {recommendations.map(
                            (recommendation, index) => {

                                const isObject =
                                    typeof recommendation ===
                                    "object" &&
                                    recommendation !== null;

                                const type =
                                    isObject
                                        ? recommendation.type
                                        : null;

                                const priority =
                                    isObject
                                        ? recommendation.priority
                                        : null;

                                const message =
                                    isObject
                                        ? recommendation.message
                                        : recommendation;

                                return (
                                    <div
                                        key={index}
                                        style={
                                            recommendationStyle
                                        }
                                    >

                                        <div
                                            style={
                                                recommendationIconStyle
                                            }
                                        >
                                            💡
                                        </div>

                                        <div
                                            style={{
                                                flex: 1
                                            }}
                                        >

                                            <div
                                                style={
                                                    recommendationTopStyle
                                                }
                                            >

                                                {type && (
                                                    <span
                                                        style={
                                                            recommendationTypeStyle
                                                        }
                                                    >
                                                        {type}
                                                    </span>
                                                )}

                                                {priority && (
                                                    <span
                                                        style={
                                                            getPriorityStyle(
                                                                priority
                                                            )
                                                        }
                                                    >
                                                        {priority}
                                                    </span>
                                                )}

                                            </div>

                                            <div
                                                style={
                                                    recommendationMessageStyle
                                                }
                                            >
                                                {message}
                                            </div>

                                        </div>

                                    </div>
                                );
                            }
                        )}

                    </div>

                </section>
            )}


            {/* =====================================
                PRACTICE HISTORY
            ===================================== */}

            <section style={cardStyle}>

                <SectionHeader
                    eyebrow="ACTIVITY"
                    title="Practice History"
                    description="Recent practice attempts and recognition results."
                />

                {history.length === 0 ? (

                    <div style={emptyHistoryStyle}>
                        <div
                            style={{
                                fontSize: "32px",
                                marginBottom: "8px"
                            }}
                        >
                            📝
                        </div>

                        <div>
                            No practice history available.
                        </div>
                    </div>

                ) : (

                    <div
                        style={{
                            overflowX: "auto",
                            border: "1px solid #eef0f4",
                            borderRadius: "12px"
                        }}
                    >

                        <table
                            style={{
                                width: "100%",
                                borderCollapse: "collapse",
                                minWidth: "720px"
                            }}
                        >

                            <thead>

                                <tr
                                    style={{
                                        background:
                                            "#F8FAFC"
                                    }}
                                >

                                    <th
                                        style={
                                            historyHeaderStyle
                                        }
                                    >
                                        Expected
                                    </th>

                                    <th
                                        style={
                                            historyHeaderStyle
                                        }
                                    >
                                        Predicted
                                    </th>

                                    <th
                                        style={
                                            historyHeaderStyle
                                        }
                                    >
                                        Result
                                    </th>

                                    <th
                                        style={
                                            historyHeaderStyle
                                        }
                                    >
                                        Confidence
                                    </th>

                                    <th
                                        style={
                                            historyHeaderStyle
                                        }
                                    >
                                        Date
                                    </th>

                                </tr>

                            </thead>

                            <tbody>

                                {history
                                    .slice()
                                    .reverse()
                                    .slice(0, 20)
                                    .map(
                                        (
                                            attempt,
                                            index
                                        ) => {

                                            const confidence =
                                                Number(
                                                    attempt.confidence ??
                                                    0
                                                );

                                            const confidencePercent =
                                                confidence <=
                                                1
                                                    ? confidence *
                                                      100
                                                    : confidence;

                                            const correct =
                                                Boolean(
                                                    attempt.correct
                                                );

                                            return (
                                                <tr
                                                    key={
                                                        attempt.assessment_id ||
                                                        index
                                                    }
                                                    style={
                                                        historyRowStyle
                                                    }
                                                >

                                                    <td
                                                        style={
                                                            historyCellStyle
                                                        }
                                                    >
                                                        <span
                                                            style={
                                                                expectedLetterStyle
                                                            }
                                                        >
                                                            {
                                                                attempt.expected ||
                                                                "-"
                                                            }
                                                        </span>
                                                    </td>

                                                    <td
                                                        style={
                                                            historyCellStyle
                                                        }
                                                    >
                                                        <span
                                                            style={
                                                                predictedLetterStyle
                                                            }
                                                        >
                                                            {
                                                                attempt.predicted ||
                                                                "-"
                                                            }
                                                        </span>
                                                    </td>

                                                    <td
                                                        style={
                                                            historyCellStyle
                                                        }
                                                    >

                                                        <span
                                                            style={{
                                                                ...resultBadgeStyle,
                                                                background:
                                                                    correct
                                                                        ? "#ECFDF5"
                                                                        : "#FEF2F2",
                                                                color:
                                                                    correct
                                                                        ? "#15803D"
                                                                        : "#DC2626"
                                                            }}
                                                        >
                                                            {correct
                                                                ? "✓ Correct"
                                                                : "✕ Incorrect"}
                                                        </span>

                                                    </td>

                                                    <td
                                                        style={
                                                            historyCellStyle
                                                        }
                                                    >

                                                        <div
                                                            style={
                                                                confidenceContainerStyle
                                                            }
                                                        >

                                                            <span
                                                                style={
                                                                    confidenceValueStyle
                                                                }
                                                            >
                                                                {confidencePercent.toFixed(
                                                                    1
                                                                )}
                                                                %
                                                            </span>

                                                        </div>

                                                    </td>

                                                    <td
                                                        style={{
                                                            ...historyCellStyle,
                                                            color:
                                                                "#6b7280"
                                                        }}
                                                    >
                                                        {formatDate(
                                                            attempt.timestamp
                                                        )}
                                                    </td>

                                                </tr>
                                            );
                                        }
                                    )}

                            </tbody>

                        </table>

                    </div>
                )}

            </section>


            {/* =====================================
                ACCOUNT INFORMATION
            ===================================== */}

            <section style={cardStyle}>

                <SectionHeader
                    eyebrow="ACCOUNT"
                    title="Student Information"
                />

                <div style={accountGridStyle}>

                    <InfoItem
                        label="Student ID"
                        value={
                            student.student_id ||
                            studentId
                        }
                    />

                    <InfoItem
                        label="Created"
                        value={formatDate(
                            student.created_at
                        )}
                    />

                    <InfoItem
                        label="Last Updated"
                        value={formatDate(
                            student.last_updated
                        )}
                    />

                </div>

            </section>

        </div>
    </div>
);


}

/* ============================================
SUMMARY CARD
============================================ */

function SummaryCard({
title,
value,
description,
icon,
iconBackground
}) {
return (
<div
style={{
...cardStyle,
marginBottom: 0,
padding: "20px"
}}
>


        <div style={summaryCardInnerStyle}>

            <div>

                <p
                    style={
                        summaryTitleStyle
                    }
                >
                    {title}
                </p>

                <strong
                    style={
                        summaryValueStyle
                    }
                >
                    {value}
                </strong>

                <p
                    style={
                        summaryDescriptionStyle
                    }
                >
                    {description}
                </p>

            </div>

            <div
                style={{
                    ...summaryIconStyle,
                    background:
                        iconBackground ||
                        "#EEF2FF"
                }}
            >
                {icon}
            </div>

        </div>

    </div>
);


}

/* ============================================
SECTION HEADER
============================================ */

function SectionHeader({
eyebrow,
title,
description
}) {
return ( <div style={sectionHeaderStyle}>

        <span style={sectionEyebrowStyle}>
            {eyebrow}
        </span>

        <h2 style={sectionTitleStyle}>
            {title}
        </h2>

        {description && (
            <p
                style={
                    sectionDescriptionStyle
                }
            >
                {description}
            </p>
        )}

    </div>
);

}

/* ============================================
INFO ITEM
============================================ */

function InfoItem({
label,
value
}) {
return ( <div>

        <span style={infoLabelStyle}>
            {label}
        </span>

        <strong style={infoValueStyle}>
            {value}
        </strong>

    </div>
);


}

/* ============================================
DATE FORMAT
============================================ */

function formatDate(value) {
if (!value) {
return "-";
}


const date = new Date(value);

if (
    Number.isNaN(
        date.getTime()
    )
) {
    return value;
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


}

/* ============================================
PRIORITY STYLE
============================================ */

function getPriorityStyle(priority) {
const normalized =
String(priority)
.toUpperCase();

if (normalized === "HIGH") {
    return {
        ...recommendationPriorityStyle,
        background: "#FEF2F2",
        color: "#DC2626"
    };
}

if (normalized === "MEDIUM") {
    return {
        ...recommendationPriorityStyle,
        background: "#FFF7ED",
        color: "#C2410C"
    };
}

return {
    ...recommendationPriorityStyle,
    background: "#ECFDF5",
    color: "#15803D"
};


}

/* ============================================
PAGE STYLES
============================================ */

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

/* ============================================
CENTER STATES
============================================ */

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

const errorIconStyle = {
fontSize: "42px",
marginBottom: "10px"
};

const mutedCenterTextStyle = {
margin: 0,
color: "#6b7280",
fontSize: "14px"
};

/* ============================================
HEADER
============================================ */

const headerStyleContainer = {
marginBottom: "28px"
};

const backLinkStyle = {
border: "none",
background: "transparent",
color: "#4F46E5",
fontSize: "14px",
fontWeight: "700",
cursor: "pointer",
padding: 0
};

const profileHeaderStyle = {
display: "flex",
alignItems: "center",
gap: "15px",
marginTop: "18px",
padding: "20px 22px",
background: "#ffffff",
border:
"1px solid #e5e7eb",
borderRadius: "16px",
boxShadow:
"0 4px 14px rgba(15, 23, 42, 0.05)"
};

const titleRowStyle = {
display: "flex",
alignItems: "center",
justifyContent: "space-between",
gap: "20px",
flexWrap: "wrap"
};

const studentAvatarStyle = {
width: "56px",
height: "56px",
flexShrink: 0,
borderRadius: "15px",
background:
"linear-gradient(135deg, #EEF2FF 0%, #F5F3FF 100%)",
color: "#4F46E5",
display: "flex",
alignItems: "center",
justifyContent: "center",
fontSize: "22px",
fontWeight: "800"
};

const pageTitleStyle = {
margin: 0,
fontSize: "28px",
lineHeight: "1.2",
fontWeight: "750",
letterSpacing: "-0.4px",
color: "#111827"
};

const studentIdStyle = {
margin: "6px 0 0",
color: "#6b7280",
fontSize: "14px"
};

const activeStatusStyle = {
display: "inline-flex",
alignItems: "center",
gap: "7px",
padding: "8px 13px",
borderRadius: "999px",
background: "#ECFDF5",
color: "#15803D",
fontSize: "12px",
fontWeight: "700",
whiteSpace: "nowrap"
};

const completedStatusStyle = {
display: "inline-flex",
alignItems: "center",
gap: "7px",
padding: "8px 13px",
borderRadius: "999px",
background: "#FFF7ED",
color: "#C2410C",
fontSize: "12px",
fontWeight: "700",
whiteSpace: "nowrap"
};

const backButtonStyle = {
marginTop: "16px",
border: "none",
background: "#4F46E5",
color: "#ffffff",
padding: "10px 16px",
borderRadius: "9px",
fontWeight: "700",
cursor: "pointer"
};

/* ============================================
SUMMARY
============================================ */

const summaryGridStyle = {
display: "grid",
gridTemplateColumns:
"repeat(auto-fit, minmax(210px, 1fr))",
gap: "18px",
marginBottom: "28px"
};

const summaryCardInnerStyle = {
display: "flex",
justifyContent: "space-between",
alignItems: "flex-start"
};

const summaryTitleStyle = {
margin: 0,
color: "#6b7280",
fontSize: "13px",
fontWeight: "600"
};

const summaryValueStyle = {
display: "block",
marginTop: "9px",
fontSize: "28px",
lineHeight: "1",
color: "#111827",
fontWeight: "750"
};

const summaryDescriptionStyle = {
margin: "8px 0 0",
color: "#9ca3af",
fontSize: "12px"
};

const summaryIconStyle = {
width: "44px",
height: "44px",
borderRadius: "12px",
display: "flex",
alignItems: "center",
justifyContent: "center",
fontSize: "20px"
};

/* ============================================
GENERAL CARD
============================================ */

const cardStyle = {
background: "#ffffff",
borderRadius: "16px",
border:
"1px solid #e5e7eb",
boxShadow:
"0 4px 14px rgba(15, 23, 42, 0.06)",
padding: "22px",
marginBottom: "28px"
};

/* ============================================
SECTION HEADER
============================================ */

const sectionHeaderStyle = {
marginBottom: "18px"
};

const sectionEyebrowStyle = {
fontSize: "11px",
fontWeight: "800",
color: "#4F46E5",
letterSpacing: "0.08em"
};

const sectionTitleStyle = {
margin: "4px 0 0",
fontSize: "19px",
color: "#111827",
fontWeight: "700"
};

const sectionDescriptionStyle = {
margin: "5px 0 0",
color: "#9ca3af",
fontSize: "13px",
lineHeight: "1.5"
};

/* ============================================
PROGRESS
============================================ */

const progressSummaryStyle = {
display: "flex",
alignItems: "center",
justifyContent: "space-between",
marginBottom: "8px"
};

const progressLabelStyle = {
display: "block",
color: "#6b7280",
fontSize: "13px"
};

const progressCountStyle = {
display: "block",
marginTop: "3px",
color: "#111827",
fontSize: "15px"
};

const progressPercentageStyle = {
fontSize: "18px",
fontWeight: "750",
color: "#4F46E5"
};

const progressTrackStyle = {
width: "100%",
height: "9px",
background: "#E5E7EB",
borderRadius: "10px",
overflow: "hidden"
};

const progressFillStyle = {
height: "100%",
background:
"linear-gradient(90deg, #4F46E5, #7C3AED)",
borderRadius: "10px",
transition:
"width 0.3s ease"
};

const lettersContainerStyle = {
display: "flex",
flexWrap: "wrap",
gap: "8px",
marginTop: "18px"
};

const completedLetterStyle = {
width: "34px",
height: "34px",
borderRadius: "9px",
background: "#ECFDF5",
color: "#15803D",
border: "1px solid #BBF7D0",
display: "inline-flex",
alignItems: "center",
justifyContent: "center",
fontWeight: "750",
fontSize: "13px"
};

const incompleteLetterStyle = {
width: "34px",
height: "34px",
borderRadius: "9px",
background: "#F8FAFC",
color: "#9CA3AF",
border: "1px solid #E5E7EB",
display: "inline-flex",
alignItems: "center",
justifyContent: "center",
fontWeight: "650",
fontSize: "13px"
};

/* ============================================
TWO COLUMN
============================================ */

const twoColumnStyle = {
display: "grid",
gridTemplateColumns:
"repeat(auto-fit, minmax(320px, 1fr))",
gap: "28px"
};

/* ============================================
INFO
============================================ */

const infoGridStyle = {
display: "grid",
gridTemplateColumns:
"repeat(auto-fit, minmax(150px, 1fr))",
gap: "22px"
};

const accountGridStyle = {
display: "grid",
gridTemplateColumns:
"repeat(auto-fit, minmax(180px, 1fr))",
gap: "22px"
};

const infoLabelStyle = {
display: "block",
color: "#9ca3af",
fontSize: "12px",
marginBottom: "5px"
};

const infoValueStyle = {
color: "#1f2937",
fontSize: "15px"
};

/* ============================================
STRONG LETTERS
============================================ */

const strongLetterStyle = {
width: "40px",
height: "40px",
borderRadius: "10px",
background: "#ECFDF5",
color: "#15803D",
border: "1px solid #BBF7D0",
display: "inline-flex",
alignItems: "center",
justifyContent: "center",
fontWeight: "750"
};

/* ============================================
EMPTY / SUCCESS
============================================ */

const emptyStateStyle = {
display: "flex",
alignItems: "center",
gap: "10px",
padding: "14px",
background: "#F8FAFC",
borderRadius: "10px",
color: "#6b7280",
fontSize: "13px"
};

const emptyStateIconStyle = {
fontSize: "18px"
};

const successBoxStyle = {
display: "flex",
alignItems: "center",
gap: "10px",
padding: "14px 16px",
background: "#ECFDF5",
color: "#15803D",
borderRadius: "10px",
fontSize: "14px",
fontWeight: "600"
};

/* ============================================
WEAK LETTERS
============================================ */

const weakLettersGridStyle = {
display: "grid",
gridTemplateColumns:
"repeat(auto-fit, minmax(220px, 1fr))",
gap: "14px"
};

const weakLetterCardStyle = {
padding: "16px",
border:
"1px solid #FECACA",
background: "#FEF2F2",
borderRadius: "12px"
};

const weakCardTopStyle = {
display: "flex",
justifyContent: "space-between",
alignItems: "center"
};

const weakLetterSymbolStyle = {
width: "38px",
height: "38px",
borderRadius: "10px",
background: "#ffffff",
color: "#DC2626",
display: "flex",
alignItems: "center",
justifyContent: "center",
fontWeight: "750",
fontSize: "16px"
};

const weakAccuracyStyle = {
color: "#DC2626",
fontWeight: "750",
fontSize: "14px"
};

const weakProgressTrackStyle = {
width: "100%",
height: "6px",
background: "#FECACA",
borderRadius: "10px",
overflow: "hidden",
marginTop: "13px"
};

const weakProgressFillStyle = {
height: "100%",
background: "#EF4444",
borderRadius: "10px"
};

const attemptsTextStyle = {
margin: "9px 0 0",
color: "#6b7280",
fontSize: "12px"
};

/* ============================================
RECOMMENDATIONS
============================================ */

const recommendationStyle = {
display: "flex",
alignItems: "flex-start",
gap: "12px",
padding: "14px",
background: "#F8FAFC",
border:
"1px solid #E5E7EB",
borderRadius: "11px",
marginBottom: "9px"
};

const recommendationIconStyle = {
width: "34px",
height: "34px",
flexShrink: 0,
borderRadius: "9px",
background: "#FFF7ED",
display: "flex",
alignItems: "center",
justifyContent: "center",
fontSize: "16px"
};

const recommendationTopStyle = {
display: "flex",
alignItems: "center",
gap: "7px",
flexWrap: "wrap",
marginBottom: "5px"
};

const recommendationTypeStyle = {
padding: "4px 8px",
borderRadius: "999px",
background: "#EEF2FF",
color: "#4F46E5",
fontSize: "10px",
fontWeight: "800"
};

const recommendationPriorityStyle = {
padding: "4px 8px",
borderRadius: "999px",
fontSize: "10px",
fontWeight: "800"
};

const recommendationMessageStyle = {
color: "#374151",
fontSize: "13px",
lineHeight: "1.5"
};

/* ============================================
HISTORY
============================================ */

const historyHeaderStyle = {
padding: "13px 14px",
textAlign: "left",
color: "#6b7280",
fontSize: "11px",
fontWeight: "750",
textTransform: "uppercase",
letterSpacing: "0.04em",
whiteSpace: "nowrap"
};

const historyCellStyle = {
padding: "13px 14px",
fontSize: "13px",
color: "#374151",
whiteSpace: "nowrap"
};

const historyRowStyle = {
borderBottom:
"1px solid #f0f2f5"
};

const expectedLetterStyle = {
display: "inline-flex",
width: "32px",
height: "32px",
alignItems: "center",
justifyContent: "center",
borderRadius: "8px",
background: "#EEF2FF",
color: "#4F46E5",
fontWeight: "750"
};

const predictedLetterStyle = {
display: "inline-flex",
width: "32px",
height: "32px",
alignItems: "center",
justifyContent: "center",
borderRadius: "8px",
background: "#F8FAFC",
color: "#374151",
border: "1px solid #E5E7EB",
fontWeight: "750"
};

const resultBadgeStyle = {
display: "inline-flex",
alignItems: "center",
padding: "5px 9px",
borderRadius: "20px",
fontSize: "12px",
fontWeight: "750"
};

const confidenceContainerStyle = {
display: "flex",
alignItems: "center"
};

const confidenceValueStyle = {
fontWeight: "650",
color: "#374151"
};

const emptyHistoryStyle = {
padding: "35px 20px",
textAlign: "center",
color: "#9ca3af",
background: "#F8FAFC",
borderRadius: "10px",
fontSize: "13px"
};
