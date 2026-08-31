
import { useEffect, useState } from "react";

import "../../styles/theme.css";

import LearningStateCard from "./LearningStateCard";
import WeeklyProgress from "./WeeklyProgress";
import WelcomeCard from "./cards/WelcomeCard";
import StatCard from "./cards/StatCard";
import ActivityChart from "./cards/ActivityChart";
import AlphabetMasteryTable from "./AlphabetMasteryTable";
import RecentPracticeHistory from "./RecentPracticeHistory";
import RecommendationCard from "./RecommendationCard";

import "../../styles/Cards.css";

import {
    FaBullseye,
    FaBook,
    FaHandsHelping
} from "react-icons/fa";

import {
    getDashboard
} from "../../services/dashboardService";


export default function StudentDashboard() {

    const [dashboard, setDashboard] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");


    /* ============================================
       FETCH DASHBOARD
    ============================================ */

    useEffect(() => {

        const fetchDashboard = async () => {

            try {

                setLoading(true);
                setError("");

                const data = await getDashboard();

                setDashboard(data);

                console.log("Dashboard:", data);

            } catch (err) {

                console.error(
                    "Failed to load dashboard:",
                    err
                );

                setError(
                    "Unable to load dashboard data."
                );

            } finally {

                setLoading(false);

            }

        };

        fetchDashboard();

    }, []);


    /* ============================================
       LOADING STATE
    ============================================ */

    if (loading) {

        return (

            <div style={pageStyle}>

                <div style={messageContainer}>

                    <div style={messageIcon}>
                        ⟳
                    </div>

                    <h2 style={messageTitle}>
                        Loading your dashboard
                    </h2>

                    <p style={messageText}>
                        Preparing your learning progress...
                    </p>

                </div>

            </div>

        );

    }


    /* ============================================
       ERROR STATE
    ============================================ */

    if (error) {

        return (

            <div style={pageStyle}>

                <div style={messageContainer}>

                    <div style={messageIcon}>
                        ⚠️
                    </div>

                    <h2 style={messageTitle}>
                        Something went wrong
                    </h2>

                    <p style={messageText}>
                        {error}
                    </p>

                </div>

            </div>

        );

    }


    /* ============================================
       EMPTY STATE
    ============================================ */

    if (!dashboard) {

        return (

            <div style={pageStyle}>

                <div style={messageContainer}>

                    <div style={messageIcon}>
                        📊
                    </div>

                    <h2 style={messageTitle}>
                        No dashboard data
                    </h2>

                    <p style={messageText}>
                        Your learning dashboard is currently
                        unavailable.
                    </p>

                </div>

            </div>

        );

    }


    /* ============================================
       DASHBOARD DATA
    ============================================ */

    const profile =
        dashboard.profile || {};

    const learningState =
        dashboard.learning_state || {};

    const metrics =
        learningState.metrics || {};

    const alphabetMastery =
        profile.alphabet_mastery || {};


    /* ============================================
       ALPHABET PROGRESS
       
       IMPORTANT:
       Do NOT rely only on profile.completed_letters.

       The actual mastery data shows which letters
       have really been practiced/mastered.
    ============================================ */

    const masteredLetters = Object.entries(
        alphabetMastery
    )
        .filter(([letter, data]) => {

            const accuracy = Number(
                data?.accuracy ?? 0
            );

            const attempts = Number(
                data?.attempts ?? 0
            );

            return (
                attempts > 0 &&
                accuracy >= 80
            );

        })
        .map(([letter]) => letter);


    /* ============================================
       PRACTICED LETTERS
       
       Any letter with actual attempts is considered
       practiced.
    ============================================ */

    const practicedLettersList = Object.entries(
        alphabetMastery
    )
        .filter(([letter, data]) => {

            const attempts = Number(
                data?.attempts ?? 0
            );

            return attempts > 0;

        })
        .map(([letter]) => letter);


    /* ============================================
       FINAL COUNTS
    ============================================ */

    const completedLetters =
        masteredLetters.length;

    const practicedLetters =
        practicedLettersList.length;


    /* ============================================
       ALPHABET COMPLETION
       
       Based on mastered letters out of 26.
       
       Example:
       4 / 26 = 15.38%
       Displayed as 15%
    ============================================ */

    const alphabetCompletion =
        Math.round(
            (
                completedLetters /
                26
            ) * 100
        );


    /* ============================================
       PRACTICE COMPLETION
    ============================================ */

    const practiceCompletion =
        Math.round(
            (
                practicedLetters /
                26
            ) * 100
        );


    /* ============================================
       PRACTICE DATA
    ============================================ */

    const practiceHistory =
        dashboard.history || [];

    const recentPractice =
        dashboard.recent_practice || [];

    const weeklyActivity =
        dashboard.weekly_activity || [];


    /* ============================================
       DEBUG DATA
    ============================================ */

    console.log(
        "Profile:",
        profile
    );

    console.log(
        "Alphabet Mastery:",
        alphabetMastery
    );

    console.log(
        "Mastered Letters:",
        masteredLetters
    );

    console.log(
        "Practiced Letters:",
        practicedLettersList
    );

    console.log(
        "Completed Letter Count:",
        completedLetters
    );

    console.log(
        "Alphabet Completion:",
        alphabetCompletion
    );


    /* ============================================
       MAIN DASHBOARD
    ============================================ */

    return (

        <main style={mainStyle}>

            <div style={contentContainer}>


                {/* ==================================
                    WELCOME
                ================================== */}

                <section style={sectionStyle}>

                    <WelcomeCard
                        profile={profile}
                        learningState={learningState}
                    />

                </section>


                {/* ==================================
                    STATISTICS
                ================================== */}

                <section
                    style={{
                        ...sectionStyle,
                        marginBottom: "28px"
                    }}
                >

                    <div className="stats-grid">

                        {/* ==========================
                            ACCURACY
                        ========================== */}

                        <StatCard
                            title="Accuracy"
                            value={`${metrics.accuracy ?? 0}%`}
                            icon={<FaBullseye />}
                            color="#22C55E"
                        />


                        {/* ==========================
                            LESSONS
                            
                            Based on mastered letters
                            instead of stale
                            profile.completed_letters
                        ========================== */}

                        <StatCard
                            title="Lessons"
                            value={completedLetters}
                            icon={<FaBook />}
                            color="#3B82F6"
                        />


                        {/* ==========================
                            PRACTICE SESSIONS
                        ========================== */}

                        <StatCard
                            title="Practice Sessions"
                            value={
                                profile.total_sessions ?? 0
                            }
                            icon={<FaHandsHelping />}
                            color="#F97316"
                        />


                        {/* ==========================
                            ALPHABET COMPLETION
                        ========================== */}

                        <StatCard
                            title="Alphabet Completion"
                            value={`${alphabetCompletion}%`}
                            icon={<FaBook />}
                            color="#8B5CF6"
                        />

                    </div>

                </section>


                {/* ==================================
                    ACTIVITY
                ================================== */}

                <section style={sectionStyle}>

                    <ActivityChart
                        history={practiceHistory}
                    />

                </section>


                {/* ==================================
                    WEEKLY PROGRESS
                ================================== */}

                <section style={sectionStyle}>

                    <WeeklyProgress
                        weeklyActivity={
                            weeklyActivity
                        }
                    />

                </section>


                {/* ==================================
                    LEARNING STATE
                ================================== */}

                <section style={sectionStyle}>

                    <LearningStateCard
                        learningState={
                            learningState
                        }
                    />

                </section>


                {/* ==================================
                    ALPHABET MASTERY
                ================================== */}

                <section style={sectionStyle}>

                    <AlphabetMasteryTable
                        alphabetMastery={
                            alphabetMastery
                        }
                    />

                </section>


                {/* ==================================
                    RECENT PRACTICE
                ================================== */}

                <section style={sectionStyle}>

                    <RecentPracticeHistory
                        history={
                            recentPractice
                        }
                    />

                </section>


                {/* ==================================
                    AI RECOMMENDATION
                ================================== */}

                <section style={sectionStyle}>

                    <RecommendationCard
                        recommendations={
                            dashboard.recommendations || []
                        }
                    />

                </section>


                {/* ==================================
                    END SPACING
                ================================== */}

                <section
                    style={{
                        ...sectionStyle,
                        marginBottom: "10px"
                    }}
                />

            </div>

        </main>

    );

}


/* ============================================
   MAIN CONTENT
============================================ */

const mainStyle = {

    flex: 1,

    minWidth: 0,

    padding: "28px",

    boxSizing: "border-box"

};


/* ============================================
   CONTENT WIDTH
============================================ */

const contentContainer = {

    width: "100%",

    maxWidth: "1450px",

    margin: "0 auto"

};


/* ============================================
   SECTION SPACING
============================================ */

const sectionStyle = {

    marginBottom: "22px"

};


/* ============================================
   LOADING / ERROR / EMPTY STATES
============================================ */

const pageStyle = {

    minHeight: "100vh",

    display: "flex",

    alignItems: "center",

    justifyContent: "center",

    background:
        "linear-gradient(135deg, #F8FAFC 0%, #EEF2FF 100%)",

    padding: "24px",

    boxSizing: "border-box"

};


/* ============================================
   MESSAGE CONTAINER
============================================ */

const messageContainer = {

    width: "100%",

    maxWidth: "420px",

    textAlign: "center",

    background:
        "var(--card, #FFFFFF)",

    borderRadius: "20px",

    padding: "45px 30px",

    boxShadow:
        "0 12px 35px rgba(15, 23, 42, 0.08)",

    border:
        "1px solid #E5E7EB"

};


/* ============================================
   MESSAGE ICON
============================================ */

const messageIcon = {

    fontSize: "42px",

    marginBottom: "12px"

};


/* ============================================
   MESSAGE TITLE
============================================ */

const messageTitle = {

    margin: "0 0 8px",

    color: "#111827",

    fontSize: "22px",

    fontWeight: "700"

};


/* ============================================
   MESSAGE TEXT
============================================ */

const messageText = {

    margin: 0,

    color: "#6B7280",

    fontSize: "14px",

    lineHeight: "1.6"

};

