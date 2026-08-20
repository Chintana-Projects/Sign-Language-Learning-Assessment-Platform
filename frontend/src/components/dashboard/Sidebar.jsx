
import { useState } from "react";

import {
    useNavigate,
    useLocation
} from "react-router-dom";

import {
    FaHome,
    FaBookOpen,
    FaChartLine,
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


    /* ========================================
       LOGOUT
    ======================================== */

    const handleLogout = () => {

        logout();

        navigate("/", {
            replace: true
        });

    };


    /* ========================================
       MENU ITEMS
    ======================================== */

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
    label: "Settings",
    icon: <FaCog />,
    path: "/dashboard/settings"
}
    ];


    /* ========================================
       SIDEBAR
    ======================================== */

    return (

        <aside
            className={`sidebar ${
                collapsed
                    ? "sidebar-collapsed"
                    : ""
            }`}
        >

            {/* ========================================
                LOGO
            ======================================== */}

            <div className="sidebar-logo">

                <div className="sidebar-logo-mark">
                    ✋
                </div>


                {!collapsed && (

                    <div className="sidebar-logo-text">

                        <h2>
                            SignSync
                        </h2>

                        <span>
                            Learn • Practice • Sign
                        </span>

                    </div>

                )}

            </div>


            {/* ========================================
                COLLAPSE / EXPAND BUTTON
            ======================================== */}

            <button
                type="button"
                className="sidebar-toggle"
                onClick={() =>
                    setCollapsed(!collapsed)
                }
                aria-label={
                    collapsed
                        ? "Expand sidebar"
                        : "Collapse sidebar"
                }
            >

                {collapsed
                    ? <FaChevronRight />
                    : <FaChevronLeft />
                }

            </button>


            {/* ========================================
                NAVIGATION
            ======================================== */}

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

                        role="button"

                        tabIndex={0}

                        title={
                            collapsed
                                ? item.label
                                : ""
                        }

                        onKeyDown={(e) => {

                            if (e.key === "Enter") {

                                navigate(item.path);

                            }

                        }}
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

                    title={
                        collapsed
                            ? "Logout"
                            : ""
                    }

                    onKeyDown={(e) => {

                        if (e.key === "Enter") {

                            handleLogout();

                        }

                    }}
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
