export default function RecentPracticeHistory({ history = [] }) {
    const recentHistory = [...history]
        .sort(
            (a, b) =>
                new Date(b.timestamp) - new Date(a.timestamp)
        )
        .slice(0, 5);

    return (
        <div style={containerStyle}>
            {/* Header */}
            <div style={headerStyle}>
                <div>
                    <h2 style={titleStyle}>
                        Recent Practice
                    </h2>

                    <p style={subtitleStyle}>
                        Your latest sign language practice attempts
                    </p>
                </div>

                <div style={countBadgeStyle}>
                    {recentHistory.length} Recent
                </div>
            </div>

            {/* Empty State */}
            {recentHistory.length === 0 ? (
                <div style={emptyStyle}>
                    <div style={emptyIconStyle}>📝</div>

                    <h3 style={emptyTitleStyle}>
                        No recent practice
                    </h3>

                    <p style={emptyTextStyle}>
                        Start practicing to see your activity here.
                    </p>
                </div>
            ) : (
                <div style={listStyle}>
                    {recentHistory.map((attempt, index) => {
                        const expected =
    String(attempt.expected || "-").toUpperCase();

                        const predicted =
                            String(attempt.predicted || "-").toUpperCase();

                        const confidence =
    Math.round(
        Number(attempt.confidence ?? 0)
    );

                        const correct = Boolean(attempt.correct);

                        return (
                            <div
                                key={`${attempt.timestamp}-${index}`}
                                style={{
                                    ...activityCardStyle,
                                    borderLeft: correct
                                        ? "3px solid #22C55E"
                                        : "3px solid #EF4444"
                                }}
                            >
                                {/* Status */}
                                <div
                                    style={{
                                        ...statusIconStyle,
                                        background: correct
                                            ? "#ECFDF5"
                                            : "#FEF2F2",
                                        color: correct
                                            ? "#16A34A"
                                            : "#DC2626"
                                    }}
                                >
                                    {correct ? "✓" : "✕"}
                                </div>

                                {/* Main */}
                                <div style={mainContentStyle}>
                                    <div style={attemptTopRowStyle}>
                                        <div>
                                            <span style={labelStyle}>
                                                Expected
                                            </span>

                                            <strong style={letterStyle}>
                                                {expected}
                                            </strong>
                                        </div>

                                        <div style={arrowStyle}>
                                            →
                                        </div>

                                        <div>
                                            <span style={labelStyle}>
                                                Predicted
                                            </span>

                                            <strong
                                                style={{
                                                    ...letterStyle,
                                                    color: correct
                                                        ? "#16A34A"
                                                        : "#DC2626"
                                                }}
                                            >
                                                {predicted}
                                            </strong>
                                        </div>
                                    </div>

                                    {/* Confidence */}
                                    <div style={confidenceSectionStyle}>
                                        <div style={confidenceHeaderStyle}>
                                            <span>
                                                Confidence
                                            </span>

                                            <strong>
                                                {confidence}%
                                            </strong>
                                        </div>

                                        <div style={confidenceTrackStyle}>
                                            <div
                                                style={{
                                                    ...confidenceFillStyle,
                                                    width: `${Math.min(
                                                        confidence,
                                                        100
                                                    )}%`,
                                                    background: correct
                                                        ? "linear-gradient(90deg, #22C55E, #16A34A)"
                                                        : "linear-gradient(90deg, #F97316, #EF4444)"
                                                }}
                                            />
                                        </div>
                                    </div>

                                    {/* Date */}
                                    <div style={dateStyle}>
                                        {formatDate(attempt.timestamp)}
                                    </div>
                                </div>

                                {/* Result Badge */}
                                <div
                                    style={{
                                        ...resultBadgeStyle,
                                        background: correct
                                            ? "#ECFDF5"
                                            : "#FEF2F2",
                                        color: correct
                                            ? "#15803D"
                                            : "#B91C1C"
                                    }}
                                >
                                    {correct ? "Correct" : "Needs Practice"}
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
}


/* ============================================
   CONTAINER
============================================ */

const containerStyle = {
    background: "#FFFFFF",
    border: "1px solid #E5E7EB",
    borderRadius: "16px",
    padding: "18px",
    marginTop: "20px",
    boxShadow: "0 5px 18px rgba(15, 23, 42, 0.05)"
};


/* ============================================
   HEADER
============================================ */

const headerStyle = {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "12px",
    marginBottom: "15px"
};

const titleStyle = {
    margin: 0,
    fontSize: "17px",
    fontWeight: "700",
    color: "#111827"
};

const subtitleStyle = {
    margin: "3px 0 0",
    fontSize: "11px",
    color: "#9CA3AF"
};

const countBadgeStyle = {
    background: "#EEF2FF",
    color: "#4F46E5",
    padding: "6px 10px",
    borderRadius: "16px",
    fontSize: "10px",
    fontWeight: "700"
};


/* ============================================
   ACTIVITY LIST
============================================ */

const listStyle = {
    display: "flex",
    flexDirection: "column",
    gap: "8px"
};

const activityCardStyle = {
    display: "flex",
    alignItems: "center",
    gap: "11px",
    padding: "11px 12px",
    background: "#F8FAFC",
    borderRadius: "11px",
    transition: "transform 0.2s ease, box-shadow 0.2s ease"
};


/* ============================================
   STATUS
============================================ */

const statusIconStyle = {
    width: "32px",
    height: "32px",
    borderRadius: "9px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "15px",
    fontWeight: "800",
    flexShrink: 0
};


/* ============================================
   MAIN CONTENT
============================================ */

const mainContentStyle = {
    flex: 1,
    minWidth: 0
};

const attemptTopRowStyle = {
    display: "flex",
    alignItems: "center",
    gap: "9px"
};

const labelStyle = {
    display: "block",
    fontSize: "9px",
    color: "#9CA3AF",
    textTransform: "uppercase",
    letterSpacing: "0.05em",
    fontWeight: "700",
    marginBottom: "1px"
};

const letterStyle = {
    fontSize: "15px",
    fontWeight: "800",
    color: "#1F2937"
};

const arrowStyle = {
    color: "#CBD5E1",
    fontSize: "15px",
    marginTop: "8px"
};


/* ============================================
   CONFIDENCE
============================================ */

const confidenceSectionStyle = {
    marginTop: "6px",
    maxWidth: "330px"
};

const confidenceHeaderStyle = {
    display: "flex",
    justifyContent: "space-between",
    fontSize: "10px",
    color: "#6B7280",
    marginBottom: "3px"
};

const confidenceTrackStyle = {
    height: "4px",
    background: "#E5E7EB",
    borderRadius: "10px",
    overflow: "hidden"
};

const confidenceFillStyle = {
    height: "100%",
    borderRadius: "10px",
    transition: "width 0.3s ease"
};


/* ============================================
   DATE
============================================ */

const dateStyle = {
    marginTop: "5px",
    fontSize: "10px",
    color: "#9CA3AF"
};


/* ============================================
   RESULT BADGE
============================================ */

const resultBadgeStyle = {
    padding: "5px 8px",
    borderRadius: "16px",
    fontSize: "10px",
    fontWeight: "700",
    whiteSpace: "nowrap"
};


/* ============================================
   EMPTY STATE
============================================ */

const emptyStyle = {
    padding: "30px 15px",
    textAlign: "center"
};

const emptyIconStyle = {
    width: "44px",
    height: "44px",
    margin: "0 auto 10px",
    borderRadius: "12px",
    background: "#EEF2FF",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "21px"
};

const emptyTitleStyle = {
    margin: "0 0 4px",
    color: "#374151",
    fontSize: "14px"
};

const emptyTextStyle = {
    margin: 0,
    color: "#9CA3AF",
    fontSize: "11px"
};


/* ============================================
   DATE FORMAT
============================================ */

function formatDate(value) {
    if (!value) return "-";

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
        return value;
    }

    return date.toLocaleString("en-IN", {
        day: "numeric",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit"
    });
}