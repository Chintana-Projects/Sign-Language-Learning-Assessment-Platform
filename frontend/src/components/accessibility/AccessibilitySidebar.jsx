
import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./AccessibilitySidebar.css";

export default function AccessibilitySidebar() {

    const navigate = useNavigate();
    const location = useLocation();

    const isActive = (path) => {
        return location.pathname === path;
    };

    const handleLogout = () => {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        localStorage.removeItem("role");

        navigate("/");
    };

    return (
        <aside className="accessibility-sidebar">

            {/* LOGO */}
            <div className="accessibility-logo">

                <div className="logo-hand">
                    ✋
                </div>

                <div>
                    <h2>SignSync</h2>
                    <span>Learn • Practice • Sign</span>
                </div>

            </div>


            {/* NAVIGATION */}
            <nav className="accessibility-nav">

                <p className="nav-title">
                    MAIN MENU
                </p>


                {/* DASHBOARD */}
                <button
                    className={
                        `accessibility-nav-item ${
                            isActive("/accessibility-trainer")
                                ? "active"
                                : ""
                        }`
                    }
                    onClick={() =>
                        navigate("/accessibility-trainer")
                    }
                >
                    <span className="nav-icon">
                        🏠
                    </span>

                    <span>
                        Dashboard
                    </span>
                </button>


                {/* LEARNERS */}
                <button
                    className={
                        `accessibility-nav-item ${
                            isActive(
                                "/accessibility-trainer/learners"
                            )
                                ? "active"
                                : ""
                        }`
                    }
                    onClick={() =>
                        navigate(
                            "/accessibility-trainer/learners"
                        )
                    }
                >
                    <span className="nav-icon">
                        👥
                    </span>

                    <span>
                        Learners
                    </span>
                </button>


                {/* ANALYTICS */}
                <button
                    className={
                        `accessibility-nav-item ${
                            isActive(
                                "/accessibility-trainer/analytics"
                            )
                                ? "active"
                                : ""
                        }`
                    }
                    onClick={() =>
                        navigate(
                            "/accessibility-trainer/analytics"
                        )
                    }
                >
                    <span className="nav-icon">
                        📊
                    </span>

                    <span>
                        Analytics
                    </span>
                </button>

            </nav>


            {/* BOTTOM */}
            <div className="accessibility-sidebar-bottom">

                <button
                    className="accessibility-nav-item logout-item"
                    onClick={handleLogout}
                >
                    <span className="nav-icon">
                        🚪
                    </span>

                    <span>
                        Logout
                    </span>
                </button>

            </div>

        </aside>
    );
}

