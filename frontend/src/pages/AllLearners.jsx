import React from "react";
import { useNavigate } from "react-router-dom";

import AccessibilitySidebar
    from "../components/dashboard/AccessibilitySidebar";

import "../styles/allLearners.css";

export default function AllLearners() {

    const navigate = useNavigate();

    const learners = [
        {
            id: "arjun",
            name: "Arjun S",
            initials: "AS",
            lesson: "C",
            progress: 72,
            accuracy: 82,
            completed: 18
        },
        {
            id: "priya",
            name: "Priya R",
            initials: "PR",
            lesson: "H",
            progress: 58,
            accuracy: 76,
            completed: 14
        },
        {
            id: "rahul",
            name: "Rahul K",
            initials: "RK",
            lesson: "M",
            progress: 86,
            accuracy: 91,
            completed: 22
        }
    ];

    return (
        <div className="trainer-layout">

            <AccessibilitySidebar />

            <main className="all-learners-page">

                <button
                    className="back-button"
                    onClick={() =>
                        navigate("/accessibility-trainer")
                    }
                >
                    ← Back to Dashboard
                </button>

                <header className="all-learners-header">
                    <h1>All Learners</h1>

                    <p>
                        View and monitor learner practice progress.
                    </p>
                </header>

                <section className="all-learners-list">

                    {learners.map((learner) => (

                        <div
                            className="all-learner-card"
                            key={learner.id}
                        >

                            <div className="all-learner-info">

                                <div className="all-learner-avatar">
                                    {learner.initials}
                                </div>

                                <div>
                                    <h2>{learner.name}</h2>

                                    <p>
                                        Current lesson:{" "}
                                        {learner.lesson}
                                    </p>
                                </div>

                            </div>

                            <div className="all-learner-stats">

                                <div>
                                    <span>Progress</span>
                                    <strong>
                                        {learner.progress}%
                                    </strong>
                                </div>

                                <div>
                                    <span>Accuracy</span>
                                    <strong>
                                        {learner.accuracy}%
                                    </strong>
                                </div>

                                <div>
                                    <span>Completed</span>
                                    <strong>
                                        {learner.completed}
                                    </strong>
                                </div>

                            </div>

                            <div className="all-learner-progress">

                                <div className="progress-bar">
                                    <div
                                        className="progress-fill"
                                        style={{
                                            width:
                                                `${learner.progress}%`
                                        }}
                                    />
                                </div>

                            </div>

                            <button
                                className="view-button"
                                onClick={() =>
                                    navigate(
                                        `/accessibility-trainer/learner/${learner.id}`
                                    )
                                }
                            >
                                View Learner
                            </button>

                        </div>

                    ))}

                </section>

            </main>

        </div>
    );
}