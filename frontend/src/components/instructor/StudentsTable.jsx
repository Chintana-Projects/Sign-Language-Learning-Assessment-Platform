export default function StudentsTable({ students = [] }) {
    return (
        <div
            style={{
                background: "#ffffff",
                borderRadius: "16px",
                border: "1px solid #e5e7eb",
                boxShadow: "0 4px 14px rgba(15, 23, 42, 0.06)",
                overflow: "hidden"
            }}
        >
            {/* Header */}
            <div
                style={{
                    padding: "22px 24px",
                    borderBottom: "1px solid #eef0f4",
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    gap: "15px",
                    flexWrap: "wrap"
                }}
            >
                <div>
                    <h2
                        style={{
                            margin: 0,
                            fontSize: "20px",
                            color: "#111827",
                            fontWeight: "700"
                        }}
                    >
                        Student Progress
                    </h2>

                    <p
                        style={{
                            margin: "5px 0 0",
                            fontSize: "13px",
                            color: "#9ca3af"
                        }}
                    >
                        Monitor individual learner performance
                    </p>
                </div>

                <div
                    style={{
                        background: "#EEF2FF",
                        color: "#4F46E5",
                        padding: "7px 12px",
                        borderRadius: "20px",
                        fontSize: "13px",
                        fontWeight: "600"
                    }}
                >
                    {students.length} Students
                </div>
            </div>

            {/* Table */}
            {students.length === 0 ? (
                <div
                    style={{
                        padding: "50px 20px",
                        textAlign: "center",
                        color: "#9ca3af"
                    }}
                >
                    <div
                        style={{
                            fontSize: "40px",
                            marginBottom: "10px"
                        }}
                    >
                        👥
                    </div>

                    <p
                        style={{
                            margin: 0,
                            fontSize: "15px"
                        }}
                    >
                        No student progress available.
                    </p>
                </div>
            ) : (
                <div
                    style={{
                        overflowX: "auto"
                    }}
                >
                    <table
                        style={{
                            width: "100%",
                            borderCollapse: "collapse",
                            minWidth: "850px"
                        }}
                    >
                        <thead>
                            <tr
                                style={{
                                    background: "#F8FAFC"
                                }}
                            >
                                <th style={headerStyle}>
                                    Student
                                </th>

                                <th style={headerStyle}>
                                    Current Letter
                                </th>

                                <th style={headerStyle}>
                                    Progress
                                </th>

                                <th style={headerStyle}>
                                    Accuracy
                                </th>

                                <th style={headerStyle}>
                                    Sessions
                                </th>

                                <th style={headerStyle}>
                                    Last Updated
                                </th>
                            </tr>
                        </thead>

                        <tbody>
                            {students.map((student, index) => {
                                const accuracy =
                                    Number(
                                        student.accuracy ?? 0
                                    );

                                const completed =
                                    Number(
                                        student.completed_letters ?? 0
                                    );

                                const progress =
                                    Math.min(
                                        (completed / 26) * 100,
                                        100
                                    );

                                return (
                                    <tr
                                        key={
                                            student.student_id ||
                                            `student-${index}`
                                        }
                                        style={{
                                            borderBottom:
                                                "1px solid #f0f2f5"
                                        }}
                                    >
                                        {/* Student */}
                                        <td
                                            style={cellStyle}
                                        >
                                            <div
                                                style={{
                                                    display: "flex",
                                                    alignItems:
                                                        "center",
                                                    gap: "12px"
                                                }}
                                            >
                                                <div
                                                    style={{
                                                        width: "38px",
                                                        height: "38px",
                                                        borderRadius:
                                                            "50%",
                                                        background:
                                                            getAvatarBackground(
                                                                index
                                                            ),
                                                        display:
                                                            "flex",
                                                        alignItems:
                                                            "center",
                                                        justifyContent:
                                                            "center",
                                                        fontWeight:
                                                            "700",
                                                        color: "#4F46E5",
                                                        fontSize:
                                                            "14px"
                                                    }}
                                                >
                                                    {getInitial(
                                                        student,
                                                        index
                                                    )}
                                                </div>

                                                <div>
                                                    <div
                                                        style={{
                                                            fontWeight:
                                                                "600",
                                                            color:
                                                                "#1f2937"
                                                        }}
                                                    >
                                                        {student.student_id ||
                                                            `Student ${
                                                                index + 1
                                                            }`}
                                                    </div>

                                                    <div
                                                        style={{
                                                            fontSize:
                                                                "12px",
                                                            color:
                                                                "#9ca3af"
                                                        }}
                                                    >
                                                        Learner
                                                    </div>
                                                </div>
                                            </div>
                                        </td>

                                        {/* Current Letter */}
                                        <td
                                            style={cellStyle}
                                        >
                                            <span
                                                style={{
                                                    display:
                                                        "inline-flex",
                                                    width: "38px",
                                                    height: "38px",
                                                    alignItems:
                                                        "center",
                                                    justifyContent:
                                                        "center",
                                                    borderRadius:
                                                        "10px",
                                                    background:
                                                        "#EEF2FF",
                                                    color:
                                                        "#4F46E5",
                                                    fontWeight:
                                                        "700",
                                                    fontSize:
                                                        "16px"
                                                }}
                                            >
                                                {student.current_letter ||
                                                    "-"}
                                            </span>
                                        </td>

                                        {/* Progress */}
                                        <td
                                            style={{
                                                ...cellStyle,
                                                minWidth:
                                                    "170px"
                                            }}
                                        >
                                            <div
                                                style={{
                                                    display:
                                                        "flex",
                                                    justifyContent:
                                                        "space-between",
                                                    marginBottom:
                                                        "6px",
                                                    fontSize:
                                                        "12px"
                                                }}
                                            >
                                                <span
                                                    style={{
                                                        color:
                                                            "#6b7280"
                                                    }}
                                                >
                                                    {completed}/26
                                                    letters
                                                </span>

                                                <span
                                                    style={{
                                                        fontWeight:
                                                            "600",
                                                        color:
                                                            "#374151"
                                                    }}
                                                >
                                                    {Math.round(
                                                        progress
                                                    )}
                                                    %
                                                </span>
                                            </div>

                                            <div
                                                style={{
                                                    width:
                                                        "100%",
                                                    height:
                                                        "7px",
                                                    background:
                                                        "#E5E7EB",
                                                    borderRadius:
                                                        "10px",
                                                    overflow:
                                                        "hidden"
                                                }}
                                            >
                                                <div
                                                    style={{
                                                        width: `${progress}%`,
                                                        height:
                                                            "100%",
                                                        background:
                                                            "linear-gradient(90deg, #4F46E5, #7C3AED)",
                                                        borderRadius:
                                                            "10px",
                                                        transition:
                                                            "width 0.3s ease"
                                                    }}
                                                />
                                            </div>
                                        </td>

                                        {/* Accuracy */}
                                        <td
                                            style={cellStyle}
                                        >
                                            <AccuracyBadge
                                                accuracy={
                                                    accuracy
                                                }
                                            />
                                        </td>

                                        {/* Sessions */}
                                        <td
                                            style={{
                                                ...cellStyle,
                                                color:
                                                    "#4b5563",
                                                fontWeight:
                                                    "500"
                                            }}
                                        >
                                            {student.total_sessions ??
                                                0}
                                        </td>

                                        {/* Last Updated */}
                                        <td
                                            style={{
                                                ...cellStyle,
                                                color:
                                                    "#6b7280",
                                                fontSize:
                                                    "13px"
                                            }}
                                        >
                                            {formatDate(
                                                student.last_updated
                                            )}
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}

/* ============================================
   ACCURACY BADGE
============================================ */

function AccuracyBadge({ accuracy }) {
    let background;
    let color;

    if (accuracy >= 80) {
        background = "#ECFDF5";
        color = "#15803D";
    } else if (accuracy >= 50) {
        background = "#FFF7ED";
        color = "#C2410C";
    } else {
        background = "#FEF2F2";
        color = "#DC2626";
    }

    return (
        <span
            style={{
                display: "inline-flex",
                alignItems: "center",
                padding: "6px 10px",
                borderRadius: "20px",
                background,
                color,
                fontSize: "13px",
                fontWeight: "700"
            }}
        >
            {accuracy}%
        </span>
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

    if (Number.isNaN(date.getTime())) {
        return value;
    }

    return date.toLocaleString("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit"
    });
}

/* ============================================
   STUDENT INITIAL
============================================ */

function getInitial(student, index) {
    const name =
        student.student_id ||
        `Student ${index + 1}`;

    return String(name).charAt(0).toUpperCase();
}

/* ============================================
   AVATAR BACKGROUND
============================================ */

function getAvatarBackground(index) {
    const backgrounds = [
        "#EEF2FF",
        "#ECFDF5",
        "#FFF7ED",
        "#F5F3FF",
        "#EFF6FF"
    ];

    return backgrounds[index % backgrounds.length];
}

/* ============================================
   TABLE STYLES
============================================ */

const headerStyle = {
    padding: "14px 16px",
    color: "#6b7280",
    fontSize: "12px",
    fontWeight: "700",
    textTransform: "uppercase",
    letterSpacing: "0.04em",
    textAlign: "left",
    whiteSpace: "nowrap"
};

const cellStyle = {
    padding: "17px 16px",
    fontSize: "14px",
    whiteSpace: "nowrap",
    textAlign: "left"
};