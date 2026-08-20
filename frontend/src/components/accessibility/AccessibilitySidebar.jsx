import AccessibilitySidebar from "../components/accessibility/AccessibilitySidebar";
import "./AccessibilityTrainer.css";

export default function AccessibilityTrainer() {

    return (
        <div className="accessibility-layout">

            {/* Trainer Sidebar */}
            <AccessibilitySidebar />


            {/* Main Content */}
            <main className="accessibility-main">

                {/* Header */}
                <header className="accessibility-header">

                    <div>
                        <h1>Accessibility Trainer</h1>

                        <p>
                            Help learners practice and improve
                            their sign language skills.
                        </p>
                    </div>

                    <div className="trainer-profile">

                        <div className="trainer-avatar">
                            AT
                        </div>

                        <div>
                            <strong>Accessibility Trainer</strong>
                            <span>SignSync</span>
                        </div>

                    </div>

                </header>


                {/* Statistics */}
                <section className="trainer-stats">

                    <div className="trainer-stat-card">

                        <div className="stat-icon">
                            👥
                        </div>

                        <div>
                            <span>Total Learners</span>
                            <h2>12</h2>
                        </div>

                    </div>


                    <div className="trainer-stat-card">

                        <div className="stat-icon">
                            🎯
                        </div>

                        <div>
                            <span>Active Learners</span>
                            <h2>8</h2>
                        </div>

                    </div>


                    <div className="trainer-stat-card">

                        <div className="stat-icon">
                            📚
                        </div>

                        <div>
                            <span>Lessons Completed</span>
                            <h2>46</h2>
                        </div>

                    </div>


                    <div className="trainer-stat-card">

                        <div className="stat-icon">
                            ⭐
                        </div>

                        <div>
                            <span>Average Accuracy</span>
                            <h2>82%</h2>
                        </div>

                    </div>

                </section>


                {/* Learners */}
                <section className="learners-section">

                    <div className="section-header">

                        <div>
                            <h2>Learners</h2>

                            <p>
                                View learner practice progress.
                            </p>
                        </div>

                        <button className="view-all-btn">
                            View All
                        </button>

                    </div>


                    <div className="learners-grid">

                        {/* Arjun */}
                        <div className="learner-card">

                            <div className="learner-top">

                                <div className="learner-avatar">
                                    AS
                                </div>

                                <div>
                                    <h3>Arjun S</h3>
                                    <p>Current lesson: C</p>
                                </div>

                            </div>


                            <div className="progress-info">

                                <span>Progress</span>

                                <strong>72%</strong>

                            </div>


                            <div className="progress-bar">

                                <div
                                    className="progress-fill"
                                    style={{ width: "72%" }}
                                />

                            </div>


                            <button className="learner-button">
                                View Learner
                            </button>

                        </div>


                        {/* Priya */}
                        <div className="learner-card">

                            <div className="learner-top">

                                <div className="learner-avatar">
                                    PR
                                </div>

                                <div>
                                    <h3>Priya R</h3>
                                    <p>Current lesson: H</p>
                                </div>

                            </div>


                            <div className="progress-info">

                                <span>Progress</span>

                                <strong>58%</strong>

                            </div>


                            <div className="progress-bar">

                                <div
                                    className="progress-fill"
                                    style={{ width: "58%" }}
                                />

                            </div>


                            <button className="learner-button">
                                View Learner
                            </button>

                        </div>


                        {/* Rahul */}
                        <div className="learner-card">

                            <div className="learner-top">

                                <div className="learner-avatar">
                                    RK
                                </div>

                                <div>
                                    <h3>Rahul K</h3>
                                    <p>Current lesson: M</p>
                                </div>

                            </div>


                            <div className="progress-info">

                                <span>Progress</span>

                                <strong>86%</strong>

                            </div>


                            <div className="progress-bar">

                                <div
                                    className="progress-fill"
                                    style={{ width: "86%" }}
                                />

                            </div>


                            <button className="learner-button">
                                View Learner
                            </button>

                        </div>

                    </div>

                </section>

            </main>

        </div>
    );
}