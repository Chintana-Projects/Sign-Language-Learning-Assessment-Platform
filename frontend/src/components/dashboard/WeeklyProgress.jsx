import "../../styles/dashboard/WeeklyProgress.css";

export default function WeeklyProgress({
    history = []
}) {
    const today = new Date();

    const startOfWeek = new Date(today);
    startOfWeek.setDate(
        today.getDate() - today.getDay()
    );
    startOfWeek.setHours(0, 0, 0, 0);

    const weeklyAttempts = history.filter((attempt) => {
        if (!attempt.timestamp) return false;

        const date = new Date(attempt.timestamp);

        return date >= startOfWeek;
    });

    const daysPracticed = new Set(
        weeklyAttempts.map(
            (attempt) =>
                new Date(attempt.timestamp).getDay()
        )
    ).size;

    const consistency = Math.round(
        (daysPracticed / 7) * 100
    );

    const dayNames = [
        "Sun",
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat"
    ];

    const practicedDays = dayNames.map((day, index) => {
        return daysPracticed > 0 &&
            weeklyAttempts.some(
                (attempt) =>
                    new Date(attempt.timestamp).getDay() === index
            );
    });

    return (
        <div className="weekly-progress-card">

            {/* ================= HEADER ================= */}

            <div className="weekly-header">

                <div className="weekly-title-section">

                    <div className="weekly-icon">
                        📅
                    </div>

                    <div>
                        <h2>
                            Weekly Progress
                        </h2>

                        <p>
                            Your practice consistency this week
                        </p>
                    </div>

                </div>

                <div className="weekly-status">
                    {consistency >= 70
                        ? "Excellent"
                        : consistency >= 40
                            ? "Good progress"
                            : "Keep going"}
                </div>

            </div>


            {/* ================= MAIN STATS ================= */}

            <div className="weekly-main">

                {/* Progress Circle */}

                <div className="weekly-circle-wrapper">

                    <div
                        className="weekly-circle"
                        style={{
                            "--weekly-progress":
                                `${consistency * 3.6}deg`
                        }}
                    >
                        <div className="weekly-circle-inner">

                            <strong>
                                {consistency}%
                            </strong>

                            <span>
                                Consistency
                            </span>

                        </div>
                    </div>

                </div>


                {/* Statistics */}

                <div className="weekly-details">

                    <div className="weekly-attempt-stat">

                        <span className="weekly-stat-icon">
                            ✋
                        </span>

                        <div>
                            <strong>
                                {weeklyAttempts.length}
                            </strong>

                            <span>
                                Practice attempt
                                {weeklyAttempts.length !== 1
                                    ? "s"
                                    : ""}
                            </span>
                        </div>

                    </div>


                    <div className="weekly-attempt-stat">

                        <span className="weekly-stat-icon">
                            🔥
                        </span>

                        <div>
                            <strong>
                                {daysPracticed}
                            </strong>

                            <span>
                                Active day
                                {daysPracticed !== 1
                                    ? "s"
                                    : ""}
                            </span>
                        </div>

                    </div>


                    <div className="weekly-message">

                        <span>💡</span>

                        <p>
                            {consistency === 100
                                ? "Amazing consistency! You practiced every day."
                                : consistency >= 70
                                    ? "Great work! Keep your practice streak going."
                                    : "Practice a little each day to build consistency."}
                        </p>

                    </div>

                </div>

            </div>


            {/* ================= WEEKLY ACTIVITY ================= */}

            <div className="weekly-activity">

                <div className="weekly-activity-header">

                    <span>
                        This Week
                    </span>

                    <span>
                        {daysPracticed}/7 days
                    </span>

                </div>


                <div className="weekly-days">

                    {dayNames.map((day, index) => (

                        <div
                            key={day}
                            className="weekly-day"
                        >

                            <div
                                className={
                                    practicedDays[index]
                                        ? "day-dot active"
                                        : "day-dot"
                                }
                            >
                                {practicedDays[index]
                                    ? "✓"
                                    : ""}
                            </div>

                            <span>
                                {day}
                            </span>

                        </div>

                    ))}

                </div>

            </div>


            {/* ================= BOTTOM ================= */}

            <div className="weekly-footer">

                <span>
                    🎯 Goal: Practice regularly
                </span>

                <span>
                    {7 - daysPracticed > 0
                        ? `${7 - daysPracticed} days remaining`
                        : "Week completed 🎉"}
                </span>

            </div>

        </div>
    );
}