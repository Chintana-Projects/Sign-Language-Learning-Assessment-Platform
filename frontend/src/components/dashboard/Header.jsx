import { useAuth } from "../../context/AuthContext";
import "./../../styles/Header.css";

export default function Header() {
    const { user } = useAuth();

    const userName = user?.full_name || "User";
    const userRole = user?.role || "Learner";

    return (
        <header className="dashboard-header">

            <div className="dashboard-header-left">

                <div className="dashboard-title-icon">
                    👋
                </div>

                <div>
                    <h1>
                        Student Dashboard
                    </h1>

                    <p>
                        Welcome back to SignSync
                    </p>
                </div>

            </div>

            <div className="header-right">

                

                <div className="profile">

                    <img
                        src={`https://ui-avatars.com/api/?name=${encodeURIComponent(
                            userName
                        )}&background=EEF2FF&color=4F46E5&bold=true`}
                        alt={`${userName} profile`}
                    />

                    <div className="profile-info">

                        <strong>
                            {userName}
                        </strong>

                        <span>
                            {formatRole(userRole)}
                        </span>

                    </div>

                </div>

            </div>

        </header>
    );
}


/* ============================================
   ROLE FORMATTER
============================================ */

function formatRole(role) {
    return String(role)
        .replace(/_/g, " ")
        .replace(/\b\w/g, (letter) =>
            letter.toUpperCase()
        );
}