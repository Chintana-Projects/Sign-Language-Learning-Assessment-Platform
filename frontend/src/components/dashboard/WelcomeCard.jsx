import { useAuth } from "../../../context/AuthContext";
import "./../../../styles/dashboard/WelcomeCard.css";

export default function WelcomeCard({
    learningState = {},
    profile = {}
}) {

    const { user } = useAuth();

    const streak =
        learningState?.metrics?.streak ??
        learningState?.daily_practice_streak ??
        0;

    const level =
        learningState?.level ||
        "Beginner";

    const nextLetter =
        profile?.next_letter ||
        "A";

    const today =
        new Date().toLocaleDateString(
            "en-US",
            {
                weekday: "long",
                day: "numeric",
                month: "long",
                year: "numeric"
            }
        );

    return (

        <div className="welcome-card">

            <div className="welcome-content">

                <p className="welcome-label">
                    Welcome back 👋
                </p>

                <h2>
                    Good Morning,{" "}
                    {user?.full_name || "Learner"}
                </h2>

                <p>
                    {today}
                </p>

                <p>
                    Ready to improve your
                    sign language skills today?
                </p>

                <p>
                    Current Level:{" "}
                    <strong>{level}</strong>
                </p>

                <p>
                    Next Alphabet:{" "}
                    <strong>{nextLetter}</strong>
                </p>

                <p>
                    🔥{" "}
                    <strong>{streak}</strong>{" "}
                    Day Streak
                </p>

            </div>

        </div>

    );

}