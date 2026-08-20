import { FaChartLine, FaBullseye, FaArrowUp } from "react-icons/fa";
import "../../styles/dashboard/LearningState.css";
export default function LearningStateCard({
    learningState = {}
}) {
    const level =
        learningState.level || "Beginner";

    const progress = Math.min(
        Math.max(Number(learningState.progress ?? 0), 0),
        100
    );

    const message =
        learningState.message ||
        "Start practicing to build your learning progress.";

    const nextGoal =
        learningState.next_goal ||
        "Continue practicing to improve your accuracy.";

    const goal = 80;
    const remaining = Math.max(goal - progress, 0);

    let levelClass = "learning-beginner";

    if (level.toLowerCase() === "mastered") {
        levelClass = "learning-mastered";
    } else if (level.toLowerCase() === "good") {
        levelClass = "learning-good";
    } else if (level.toLowerCase() === "improving") {
        levelClass = "learning-improving";
    }

    return (
        <div className="learning-state-card">

            {/* ================= HEADER ================= */}

            <div className="learning-state-header">

                <div>
                    <div className="learning-state-title-row">
                        <div className="learning-state-icon">
                            <FaChartLine />
                        </div>

                        <div>
                            <h2>Learning State</h2>

                            <p>
                                Your current learning performance
                            </p>
                        </div>
                    </div>
                </div>

                <div className={`learning-level-badge ${levelClass}`}>
                    <FaArrowUp />
                    {level}
                </div>

            </div>


            {/* ================= MAIN CONTENT ================= */}

            <div className="learning-state-content">

                {/* Performance Circle */}

                <div className="performance-section">

                    <div
                        className="performance-circle"
                        style={{
                            "--progress": `${progress * 3.6}deg`
                        }}
                    >
                        <div className="performance-circle-inner">

                            <strong>
                                {Math.round(progress)}%
                            </strong>

                            <span>
                                Performance
                            </span>

                        </div>
                    </div>

                </div>


                {/* Performance Information */}

                <div className="performance-info">

                    <div className="performance-heading">

                        <div>
                            <span>
                                Learning Performance
                            </span>

                            <h3>
                                {Math.round(progress)}%
                            </h3>
                        </div>

                        <div className="target-badge">
                            Goal {goal}%
                        </div>

                    </div>


                    {/* Progress Bar */}

                    <div className="goal-progress">

                        <div className="goal-progress-labels">

                            <span>
                                Current
                            </span>

                            <span>
                                {remaining > 0
                                    ? `${Math.round(remaining)}% to goal`
                                    : "Goal reached 🎉"}
                            </span>

                        </div>

                        <div className="goal-progress-track">

                            <div
                                className="goal-progress-fill"
                                style={{
                                    width: `${progress}%`
                                }}
                            />

                            <div
                                className="goal-marker"
                                style={{
                                    left: `${goal}%`
                                }}
                            />

                        </div>

                        <div className="goal-scale">

                            <span>0%</span>
                            <span>80%</span>
                            <span>100%</span>

                        </div>

                    </div>


                    {/* Message */}

                    <div className="learning-message">

                        <div className="message-icon">
                            💡
                        </div>

                        <div>
                            <strong>
                                Keep going!
                            </strong>

                            <p>
                                {message}
                            </p>
                        </div>

                    </div>

                </div>

            </div>


            {/* ================= NEXT GOAL ================= */}

            <div className="next-goal">

                <div className="next-goal-icon">
                    <FaBullseye />
                </div>

                <div className="next-goal-content">

                    <span>
                        NEXT GOAL
                    </span>

                    <p>
                        {nextGoal}
                    </p>

                </div>

                <div className="goal-arrow">
                    →
                </div>

            </div>

        </div>
    );
}