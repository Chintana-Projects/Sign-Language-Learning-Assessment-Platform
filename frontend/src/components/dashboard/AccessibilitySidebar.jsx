import React from "react";
import {
    useNavigate,
    useLocation
} from "react-router-dom";

import {
    FaHome,
    FaSignOutAlt
} from "react-icons/fa";

import { useAuth } from "../../context/AuthContext";

import "../../styles/Sidebar.css";

export default function AccessibilitySidebar() {

    const navigate = useNavigate();
    const location = useLocation();

    const { logout } = useAuth();


    const handleLogout = () => {

        logout();

        navigate("/", {
            replace: true
        });

    };


    const menuItems = [
        {
            label: "Dashboard",
            icon: <FaHome />,
            path: "/accessibility-trainer"
        }
    ];


    return (

        <aside className="sidebar">

            {/* ========================================
                LOGO
            ======================================== */}

            <div className="sidebar-logo">

                <div className="sidebar-logo-mark">
                    ✋
                </div>

                <div className="sidebar-logo-text">

                    <h2>
                        SignSync
                    </h2>

                    <span>
                        Learn • Practice • Sign
                    </span>

                </div>

            </div>


            {/* ========================================
                NAVIGATION
            ======================================== */}

            <nav className="sidebar-menu">

                <p className="sidebar-section-title">
                    MAIN MENU
                </p>


                {menuItems.map((item) => (

                    <div
                        key={item.label}
                        className={`sidebar-item ${
                            location.pathname === item.path
                                ? "active"
                                : ""
                        }`}
                        onClick={() =>
                            navigate(item.path)
                        }
                        role="button"
                        tabIndex={0}
                        onKeyDown={(e) => {

                            if (e.key === "Enter") {
                                navigate(item.path);
                            }

                        }}
                    >

                        <span className="sidebar-icon">
                            {item.icon}
                        </span>

                        <span className="sidebar-label">
                            {item.label}
                        </span>

                    </div>

                ))}

            </nav>


            {/* ========================================
                FOOTER
            ======================================== */}

            <div className="sidebar-footer">

                <div className="sidebar-footer-divider" />

                <div
                    className="sidebar-item sidebar-logout"
                    onClick={handleLogout}
                    role="button"
                    tabIndex={0}
                    onKeyDown={(e) => {

                        if (e.key === "Enter") {
                            handleLogout();
                        }

                    }}
                >

                    <span className="sidebar-icon">
                        <FaSignOutAlt />
                    </span>

                    <span className="sidebar-label">
                        Logout
                    </span>

                </div>

            </div>

        </aside>

    );
}