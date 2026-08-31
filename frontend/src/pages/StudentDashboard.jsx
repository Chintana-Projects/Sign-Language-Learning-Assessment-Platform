import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import WelcomeCard from "./WelcomeCard";
import LearningStateCard from "./LearningStateCard";
import RecommendationCard from "./RecommendationCard";

import ProgressOverview from "./ProgressOverview";
import WeeklyProgress from "./WeeklyProgress";
import AlphabetMasteryTable from "./AlphabetMasteryTable";
import RecentPracticeHistory from "./RecentPracticeHistory";

import { getDashboard } from "../../services/dashboard";

export default function StudentDashboard() {

    const navigate = useNavigate();

    const [dashboardData, setDashboardData] =
        useState(null);


    // ==========================================
    // LOAD DASHBOARD
    // ==========================================

    useEffect(() => {

        async function loadDashboard() {

            try {

                const data = await getDashboard();

                console.log(
                    "Dashboard data:",
                    data
                );

                setDashboardData(data);

            } catch (error) {

                console.error(
                    "Failed to load dashboard:",
                    error
                );

            }

        }

        loadDashboard();

    }, []);


    // ==========================================
    // LOADING
    // ==========================================

    if (!dashboardData) {

        return (
            <div className="dashboard-loading">
                Loading dashboard...
            </div>
        );

    }


    // ==========================================
    // SAFE DATA
    // ==========================================

    const profile =
        dashboardData.profile || {};

    const learningState =
        dashboardData.learning_state || {};

    const recommendations =
        dashboardData.recommendations || [];

    const nextPractice =
        dashboardData.next_practice || null;

    const history =
        dashboardData.history || [];

    const recentPractice =
        dashboardData.recent_practice || [];

    const weeklyActivity =
        dashboardData.weekly_activity || [];

    const alphabetMastery =
        profile.alphabet_mastery || {};


    // ==========================================
    // DASHBOARD
    // ==========================================

    return (

        <div className="dashboard-grid">


            {/* ==================================
                WELCOME
            ================================== */}

            <WelcomeCard
                profile={profile}
            />


            {/* ==================================
                LEARNING STATE
            ================================== */}

            <LearningStateCard
                learningState={learningState}
            />


            {/* ==================================
                AI RECOMMENDATION
            ================================== */}

            <RecommendationCard
                nextPractice={nextPractice}
                recommendations={recommendations}
                onStartPractice={() =>
                    navigate(
                        "/dashboard/practice"
                    )
                }
            />


            {/* ==================================
                PROGRESS OVERVIEW
            ================================== */}

            <ProgressOverview
                profile={profile}
                learningState={learningState}
            />


            {/* ==================================
                WEEKLY PROGRESS
            ================================== */}

            <WeeklyProgress
                history={history}
            />


            {/* ==================================
                ALPHABET MASTERY
            ================================== */}

            <AlphabetMasteryTable
                alphabetMastery={alphabetMastery}
            />


            {/* ==================================
                RECENT PRACTICE
            ================================== */}

            <RecentPracticeHistory
                history={recentPractice}
            />

        </div>

    );

}