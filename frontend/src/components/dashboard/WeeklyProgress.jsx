import "../../styles/dashboard/WeeklyProgress.css";

export default function WeeklyProgress({
    weeklyActivity = []
}) {

    // ==========================================
    // DAY NAMES
    // ==========================================

    const dayNames = [
        "Sun",
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat"
    ];


    // ==========================================
    // NORMALIZE BACKEND DATA
    // ==========================================

    const activity = Array.isArray(weeklyActivity)
        ? weeklyActivity
        : [];


    // ==========================================
    // TOTAL PRACTICE ATTEMPTS
    // ==========================================

    const totalAttempts = activity.reduce(
        (total, day) => {
            return total + Number(
                day.attempts || 0
            );
        },
        0
    );


    // ==========================================
    // TOTAL ACTIVE DAYS
    // ==========================================

    const daysPracticed = activity.filter(
        (day) =>
            Number(day.attempts || 0) > 0
    ).length;


    // ==========================================
    // WEEKLY CONSISTENCY
    // ==========================================

    const consistency = Math.round(
        (daysPracticed / 7) * 100
    );


    // ==========================================
    // MAP BACKEND DATES TO WEEK DAYS
    // ==========================================

    const practicedDays = Array(7).fill(false);

    activity.forEach((day) => {

        if (
            !day.date ||
            Number(day.attempts || 0) <= 0
        ) {
            return;
        }

        const date = new Date(
            `${day.date}T00:00:00`
        );

        if (Number.isNaN(date.getTime())) {
            return;
        }

        const dayIndex = date.getDay();

        practicedDays[dayIndex] = true;

    });


    // ==========================================
    // STATUS
    // ==========================================

    let status = "Keep going";

    if (consistency >= 70) {
        status = "Excellent";
    } else if (consistency >= 40) {
        status = "Good progress";
    }


    // ==========================================
    // MESSAGE
    // ==========================================

    let message =
        "Practice a little each day to build consistency.";

    if (consistency === 100) {

        message =
            "Amazing consistency! You practiced every day.";

    } else if (consistency >= 70) {

        message =
            "Great work! Keep your practice streak going.";

    }


    // ==========================================
    // RENDER
    // ==========================================

    return (

        <div className="weekly-progress-card">


            {/* ==================================
                HEADER
            ================================== */}

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
                    {status}
                </div>

            </div>


            {/* ==================================
                MAIN STATS
            ================================== */}

            <div className="weekly-main">


                {/* ==================================
                    PROGRESS CIRCLE
                ================================== */}

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


                {/* ==================================
                    STATISTICS
                ================================== */}

                <div className="weekly-details">


                    {/* ==================================
                        TOTAL ATTEMPTS
                    ================================== */}

                    <div className="weekly-attempt-stat">

                        <span className="weekly-stat-icon">
                            ✋
                        </span>

                        <div>

                            <strong>
                                {totalAttempts}
                            </strong>

                            <span>
                                Practice attempt
                                {totalAttempts !== 1
                                    ? "s"
                                    : ""}
                            </span>

                        </div>

                    </div>


                    {/* ==================================
                        ACTIVE DAYS
                    ================================== */}

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


                    {/* ==================================
                        MESSAGE
                    ================================== */}

                    <div className="weekly-message">

                        <span>
                            💡
                        </span>

                        <p>
                            {message}
                        </p>

                    </div>

                </div>

            </div>


            {/* ==================================
                WEEKLY ACTIVITY
            ================================== */}

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

                    {dayNames.map(
                        (day, index) => (

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

                        )
                    )}

                </div>

            </div>


            {/* ==================================
                FOOTER
            ================================== */}

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