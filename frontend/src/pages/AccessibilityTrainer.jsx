import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import AccessibilitySidebar
    from "../components/dashboard/AccessibilitySidebar";

import "../styles/accessibilityTrainer.css";


export default function AccessibilityTrainer() {

    const navigate = useNavigate();

    const [dashboard, setDashboard] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");


    // =====================================================
    // LOAD INSTRUCTOR DASHBOARD
    // =====================================================

    useEffect(() => {

        const loadDashboard = async () => {

            try {

                setLoading(true);
                setError("");

                const response = await fetch(
                    "http://localhost:8000/instructor/dashboard"
                );

                if (!response.ok) {

                    throw new Error(
                        "Failed to load trainer dashboard."
                    );

                }

                const data = await response.json();

                console.log(
                    "Instructor Dashboard:",
                    data
                );

                setDashboard(data);

            }

            catch (err) {

                console.error(
                    "Dashboard Error:",
                    err
                );

                setError(
                    "Unable to load dashboard data."
                );

            }

            finally {

                setLoading(false);

            }

        };


        loadDashboard();

    }, []);


    // =====================================================
    // OPEN LEARNER DETAILS
    // =====================================================

    const openLearner = (learnerId) => {

        console.log(
            "Opening learner:",
            learnerId
        );

        navigate(
            `/accessibility-trainer/learner/${learnerId}`
        );

    };


    // =====================================================
    // LOADING STATE
    // =====================================================

    if (loading) {

        return (

            <div className="trainer-layout">

                <AccessibilitySidebar />

                <main className="trainer-page">

                    <h2>
                        Loading dashboard...
                    </h2>

                </main>

            </div>

        );

    }


    // =====================================================
    // ERROR STATE
    // =====================================================

    if (error) {

        return (

            <div className="trainer-layout">

                <AccessibilitySidebar />

                <main className="trainer-page">

                    <h2>
                        {error}
                    </h2>

                </main>

            </div>

        );

    }


    // =====================================================
    // SAFETY CHECK
    // =====================================================

    if (!dashboard) {

        return (

            <div className="trainer-layout">

                <AccessibilitySidebar />

                <main className="trainer-page">

                    <h2>
                        No dashboard data available.
                    </h2>

                </main>

            </div>

        );

    }


    // =====================================================
    // MAIN PAGE
    // =====================================================

    return (

        <div className="trainer-layout">


            {/* =================================================
                SIDEBAR
            ================================================= */}

            <AccessibilitySidebar />


            {/* =================================================
                MAIN CONTENT
            ================================================= */}

            <main className="trainer-page">


                {/* =================================================
                    HEADER
                ================================================= */}

                <header className="trainer-header">

                    <div>

                        <h1>
                            Accessibility Trainer
                        </h1>

                        <p>
                            Help learners practice and improve
                            their sign language skills.
                        </p>

                    </div>


                    <div className="trainer-profile">

                        <div className="profile-avatar">
                            AT
                        </div>

                        <div>

                            <strong>
                                Accessibility Trainer
                            </strong>

                            <span>
                                SignSync
                            </span>

                        </div>

                    </div>

                </header>



                {/* =================================================
                    OVERVIEW STATISTICS
                ================================================= */}

                <section className="trainer-stats">


                    {/* ---------------------------------------------
                        TOTAL LEARNERS
                    --------------------------------------------- */}

                    <div className="trainer-stat-card">

                        <span className="stat-icon">
                            👥
                        </span>

                        <div>

                            <p>
                                Total Learners
                            </p>

                            <h2>
                                {dashboard.total_students}
                            </h2>

                        </div>

                    </div>


                    {/* ---------------------------------------------
                        ACTIVE LEARNERS
                    --------------------------------------------- */}

                    <div className="trainer-stat-card">

                        <span className="stat-icon">
                            🎯
                        </span>

                        <div>

                            <p>
                                Active Learners
                            </p>

                            <h2>
                                {dashboard.active_students}
                            </h2>

                        </div>

                    </div>


                    {/* ---------------------------------------------
                        COMPLETED LEARNERS
                    --------------------------------------------- */}

                    <div className="trainer-stat-card">

                        <span className="stat-icon">
                            📚
                        </span>

                        <div>

                            <p>
                                Lessons Completed
                            </p>

                            <h2>
                                {dashboard.completed_students}
                            </h2>

                        </div>

                    </div>


                    {/* ---------------------------------------------
                        AVERAGE ACCURACY
                    --------------------------------------------- */}

                    <div className="trainer-stat-card">

                        <span className="stat-icon">
                            ⭐
                        </span>

                        <div>

                            <p>
                                Average Accuracy
                            </p>

                            <h2>
                                {dashboard.average_accuracy}%
                            </h2>

                        </div>

                    </div>


                </section>



                {/* =================================================
                    LEARNERS
                ================================================= */}

                <section className="learners-section">


                    {/* ---------------------------------------------
                        SECTION HEADING
                    --------------------------------------------- */}

                    <div className="section-heading">

                        <div>

                            <h2>
                                Learners
                            </h2>

                            <p>
                                View learner practice progress.
                            </p>

                        </div>


                        <button
                            className="view-all-button"
                            type="button"
                            onClick={() =>
                                navigate(
                                    "/accessibility-trainer/learners"
                                )
                            }
                        >
                            View All
                        </button>

                    </div>



                    {/* =================================================
                        LEARNER LIST
                    ================================================= */}

                    <div className="learner-list">


                        {dashboard.students &&
                        dashboard.students.length > 0 ? (

                            dashboard.students.map(
                                (student) => {

                                    const learnerId =
                                        student.student_id;

                                    const learnerName =
                                        learnerId
                                            ? learnerId
                                                .charAt(0)
                                                .toUpperCase() +
                                              learnerId.slice(1)
                                            : "Learner";

                                    const initials =
                                        learnerName
                                            .substring(0, 2)
                                            .toUpperCase();


                                    return (

                                        <div
                                            className="learner-card"
                                            key={learnerId}
                                        >


                                            {/* ---------------------------------
                                                LEARNER INFO
                                            --------------------------------- */}

                                            <div className="learner-info">

                                                <div className="learner-avatar">

                                                    {initials}

                                                </div>


                                                <div>

                                                    <h3>
                                                        {learnerName}
                                                    </h3>

                                                    <p>
                                                        Current lesson:{" "}
                                                        {
                                                            student.current_letter ||
                                                            "A"
                                                        }
                                                    </p>

                                                </div>

                                            </div>



                                            {/* ---------------------------------
                                                PROGRESS
                                            --------------------------------- */}

                                            <div className="learner-progress">

                                                <div className="progress-label">

                                                    <span>
                                                        Progress
                                                    </span>

                                                    <strong>
                                                        {Math.round(
                                                            (
                                                                (
                                                                    student.completed_letters ||
                                                                    0
                                                                ) / 26
                                                            ) * 100
                                                        )}%
                                                    </strong>

                                                </div>


                                                <div className="progress-bar">

                                                    <div
                                                        className="progress-fill"
                                                        style={{
                                                            width: `${Math.min(
                                                                100,
                                                                Math.max(
                                                                    0,
                                                                    (
                                                                        (
                                                                            student.completed_letters ||
                                                                            0
                                                                        ) / 26
                                                                    ) * 100
                                                                )
                                                            )}%`
                                                        }}
                                                    />

                                                </div>

                                            </div>



                                            {/* ---------------------------------
                                                ACCURACY
                                            --------------------------------- */}

                                            <div className="learner-accuracy">

                                                <span>
                                                    Accuracy
                                                </span>

                                                <strong>
                                                    {
                                                        student.accuracy ??
                                                        0
                                                    }%
                                                </strong>

                                            </div>



                                            {/* ---------------------------------
                                                VIEW LEARNER BUTTON
                                            --------------------------------- */}

                                            <button
                                                className="view-button"
                                                type="button"
                                                onClick={() =>
                                                    openLearner(
                                                        learnerId
                                                    )
                                                }
                                            >
                                                View Learner
                                            </button>


                                        </div>

                                    );

                                }

                            )

                        ) : (

                            <div className="no-learners">

                                <p>
                                    No learners found.
                                </p>

                            </div>

                        )}


                    </div>


                </section>


            </main>


        </div>

    );

}