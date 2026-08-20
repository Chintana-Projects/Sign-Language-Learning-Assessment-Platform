import "./../../../styles/dashboard/WelcomeCard.css";

export default function WelcomeCard({ profile }) {

    const hour = new Date().getHours();

    let greeting = "Good Evening";

    if (hour < 12) {
        greeting = "Good Morning";
    } else if (hour < 17) {
        greeting = "Good Afternoon";
    }

    const today = new Date().toLocaleDateString("en-IN", {
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric"
    });

    return (

        <div className="welcome-card-new">

            <div className="welcome-left">

                <h2>
                    {greeting}, {profile?.full_name || "Learner"} 👋
                </h2>

                <p>
                    {today}
                </p>

                <p className="welcome-description">
                    Ready to improve your sign language skills today?
                </p>

                <button>
                    Continue Practice →
                </button>

            </div>

            <div className="welcome-right">

                <div className="streak-card">

                    🔥

                    <h1>{profile?.current_streak || 0}</h1>

                    <span>Day Streak</span>

                </div>

            </div>

        </div>

    );

}