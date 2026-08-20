
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

    const [dashboardData, setDashboardData] = useState(null);

    useEffect(() => {

        async function loadDashboard() {

            try {

                const data = await getDashboard();

                console.log("Dashboard data:", data);

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


    if (!dashboardData) {

        return (
            <div className="dashboard-loading">
                Loading dashboard...
            </div>
        );

    }


    return (
        <div className="dashboard-grid">

            <WelcomeCard
                profile={dashboardData.profile}
            />

            <LearningStateCard
                learningState={
                    dashboardData.learning_state
                }
            />

            <RecommendationCard
                recommendations={
                    dashboardData.recommendations
                }

                onStartPractice={() =>
                    navigate("/dashboard/practice")
                }
            />

            <ProgressOverview
                profile={dashboardData.profile}
                learningState={
                    dashboardData.learning_state
                }
            />

            <WeeklyProgress
                history={dashboardData.history}
            />

            <AlphabetMasteryTable
                alphabetMastery={
                    dashboardData.profile.alphabet_mastery
                }
            />

            <RecentPracticeHistory
                history={dashboardData.history}
            />

        </div>
    );
}
