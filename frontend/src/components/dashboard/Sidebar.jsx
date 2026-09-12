import { useState } from "react";

import {
    useNavigate,
    useLocation
} from "react-router-dom";

import {
    FaHome,
    FaBookOpen,
    FaChartLine,
    FaCertificate,
    FaCog,
    FaSignOutAlt,
    FaChevronLeft,
    FaChevronRight
} from "react-icons/fa";

import { useAuth } from "../../context/AuthContext";

import "./../../styles/Sidebar.css";

export default function Sidebar() {

    const navigate = useNavigate();
    const location = useLocation();

    const { user, logout } = useAuth();

    const [collapsed, setCollapsed] = useState(false);

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
            path:
                user?.role === "accessibility_trainer"
                    ? "/accessibility-trainer"
                    : "/dashboard"
        },

        {
            label: "Practice",
            icon: <FaBookOpen />,
            path: "/dashboard/practice"
        },

        {
            label: "Reports",
            icon: <FaChartLine />,
            path: "/dashboard/reports"
        },

        {
            label: "Certification",
            icon: <FaCertificate />,
            path: "/dashboard/certification"
        },

        {
            label: "Settings",
            icon: <FaCog />,
            path: "/dashboard/settings"
        }

    ];

    return (

        <aside
            className={`sidebar ${
                collapsed
                    ? "sidebar-collapsed"
                    : ""
            }`}
        >

            {/* LOGO */}

            <div className="sidebar-logo">

                <div className="sidebar-logo-mark">
                    ✋
                </div>

                {!collapsed && (

                    <div className="sidebar-logo-text">

                        <h2>SignSync</h2>

                        <span>
                            Learn • Practice • Sign
                        </span>

                    </div>

                )}

            </div>

           {/* PROFILE */}

<div
    className="sidebar-profile"
    role="button"
    tabIndex={0}
    onClick={() => navigate("/dashboard/profile")}
    onKeyDown={(e) => {
        if (e.key === "Enter") {
            navigate("/dashboard/profile");
        }
    }}
>

    <div className="sidebar-avatar">

        {localStorage.getItem(
            `profile_photo_${user?.id}`
        ) ? (

            <img
                src={localStorage.getItem(
                    `profile_photo_${user?.id}`
                )}
                alt="Profile"
                className="sidebar-avatar-image"
            />

        ) : (

            user?.full_name
                ?.split(" ")
                ?.map(name => name[0])
                ?.join("")
                ?.substring(0, 2)
                ?.toUpperCase() || "US"

        )}

    </div>

    {!collapsed && (

        <div className="sidebar-profile-info">

            <h4>
                {user?.full_name || "Learner"}
            </h4>

            <p>
                Learner
            </p>

        </div>

    )}

</div>

            {/* COLLAPSE */}

            <button
                type="button"
                className="sidebar-toggle"
                onClick={() =>
                    setCollapsed(!collapsed)
                }
            >

                {collapsed
                    ? <FaChevronRight />
                    : <FaChevronLeft />}

            </button>

            {/* MENU */}

            <nav className="sidebar-menu">

                {!collapsed && (

                    <p className="sidebar-section-title">
                        MAIN MENU
                    </p>

                )}

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
                    >

                        <span className="sidebar-icon">
                            {item.icon}
                        </span>

                        {!collapsed && (

                            <span className="sidebar-label">
                                {item.label}
                            </span>

                        )}

                    </div>

                ))}

            </nav>

            {/* FOOTER */}

            <div className="sidebar-footer">

                <div className="sidebar-footer-divider" />

                <div
                    className="sidebar-item sidebar-logout"
                    onClick={handleLogout}
                >

                    <span className="sidebar-icon">
                        <FaSignOutAlt />
                    </span>

                    {!collapsed && (

                        <span className="sidebar-label">
                            Logout
                        </span>

                    )}

                </div>

            </div>

        </aside>

    );

}