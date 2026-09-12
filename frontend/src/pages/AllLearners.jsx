import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/allLearners.css";

export default function AllLearners() {
useEffect(() => {

    const loadLearners = async () => {

        try {

            const response = await fetch(
                "http://localhost:8000/instructor/dashboard"
            );

            if (!response.ok) {
                throw new Error();
            }

            const data = await response.json();

            setLearners(
                Array.isArray(data.students)
                    ? data.students
                    : []
            );

        } catch (err) {

            console.error(err);

            setError(
                "Unable to load learners."
            );

        } finally {

            setLoading(false);

        }

    };

    loadLearners();

}, []);
    const navigate = useNavigate();
    const [learners, setLearners] = React.useState([]);
const [loading, setLoading] = React.useState(true);
const [error, setError] = React.useState("");

  if (loading) {

    return (
        <div className="all-learners-page">
            Loading learners...
        </div>
    );

}

if (error) {

    return (
        <div className="all-learners-page">
            {error}
        </div>
    );

}

    return (
        <div className="all-learners-page">

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

            <section className="all-learners-table-wrapper">

                <table className="all-learners-table">

                    <thead>
                        <tr>
                            <th>Learner</th>
                            <th>Current Lesson</th>
                            <th>Progress</th>
                            <th>Accuracy</th>
                            <th>Completed</th>
                            <th>Action</th>
                        </tr>
                    </thead>

                    <tbody>

                        {learners.map((learner) => (

                            <tr key={learner.id}>

                                {/* Learner */}
                                <td>
                                    <div className="table-learner-info">

                                        <div className="table-learner-avatar">
                                            {(learner.student_name || learner.student_id)
    .split(" ")
    .map(word => word[0])
    .join("")
    .substring(0, 2)
    .toUpperCase()}
                                        </div>

                                        <strong>
                                          {learner.student_name ||
 learner.student_id}
                                        </strong>

                                    </div>
                                </td>

                                {/* Current Lesson */}
                                <td>
                                    <span className="lesson-badge">
                                        {learner.current_letter === "COMPLETED"
    ? "✓"
    : learner.current_letter}
                                    </span>
                                </td>

                                {/* Progress */}
                                <td>
                                    <div className="table-progress">

                                        <div className="table-progress-top">
                                            <span>
                                                {Math.round(
    (
        Number(
            learner.completed_letters || 0
        ) / 26
    ) * 100
)}%
                                            </span>
                                        </div>

                                        <div className="table-progress-bar">
                                            <div
                                                className="table-progress-fill"
                                                style={{
                                                    width: `${learner.progress}%`
                                                }}
                                            />
                                        </div>

                                    </div>
                                </td>

                                {/* Accuracy */}
                                <td>
                                    <strong className="accuracy-value">
                                        {learner.accuracy.toFixed(2)}%
                                    </strong>
                                </td>

                                {/* Completed */}
                                <td>
                                    <strong className="completed-value">
                                      {learner.completed_letters || 0}/26
                                    </strong>
                                </td>

                                {/* Action */}
                                <td>
                                    <button
                                        className="view-button"
                                        onClick={() =>
                                            navigate(
                                                `/accessibility-trainer/learner/${learner.student_id}`
                                            )
                                        }
                                    >
                                        View Learner
                                    </button>
                                </td>

                            </tr>

                        ))}

                    </tbody>

                </table>

            </section>

        </div>
    );
}

