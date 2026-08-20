import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import "../../styles/AdministratorDashboard.css";
import ContentManagement from "../../pages/ContentManagement";
import Reports from "../../pages/Reports";
import {
    getAllUsers,
    registerUser,
    updateUser,
    updateUserStatus
} from "../../services/authService";

export default function AdministratorDashboard() {

    const navigate = useNavigate();

    const { user, logout } = useAuth();


    // =====================================================
    // ACTIVE SECTION
    // =====================================================

    const [activeSection, setActiveSection] = useState(
        "overview"
    );


    // =====================================================
    // USERS
    // =====================================================

    const [users, setUsers] = useState([]);

    const [usersLoading, setUsersLoading] = useState(false);

    const [usersError, setUsersError] = useState("");


    // =====================================================
    // SEARCH / FILTER
    // =====================================================

    const [searchTerm, setSearchTerm] = useState("");

    const [roleFilter, setRoleFilter] = useState("all");


    // =====================================================
    // ADD USER MODAL
    // =====================================================

    const [showAddUser, setShowAddUser] = useState(false);

    const [newUser, setNewUser] = useState({
        full_name: "",
        email: "",
        password: "",
        role: "learner"
    });

    const [addUserLoading, setAddUserLoading] =
        useState(false);

    const [addUserError, setAddUserError] =
        useState("");
        const [showEditUser, setShowEditUser] = useState(false);

const [editingUser, setEditingUser] = useState(null);

const [editUserLoading, setEditUserLoading] = useState(false);

const [editUserError, setEditUserError] = useState("");


    // =====================================================
    // LOAD USERS
    // =====================================================

    const loadUsers = async () => {

        try {

            setUsersLoading(true);

            setUsersError("");

            const data = await getAllUsers();

            setUsers(data);

        } catch (error) {

            console.error(
                "Failed to load users:",
                error
            );

            setUsersError(
                error.response?.data?.detail ||
                "Unable to load users."
            );

        } finally {

            setUsersLoading(false);

        }

    };


    // =====================================================
    // LOAD USERS WHEN ADMIN DASHBOARD OPENS
    // =====================================================

    useEffect(() => {

        loadUsers();

    }, []);


    // =====================================================
    // ADD USER
    // =====================================================

    const handleAddUser = async (e) => {

        e.preventDefault();

        try {

            setAddUserLoading(true);

            setAddUserError("");


            await registerUser(newUser);


            // Close modal

            setShowAddUser(false);


            // Reset form

            setNewUser({
                full_name: "",
                email: "",
                password: "",
                role: "learner"
            });


            // Reload users

            await loadUsers();


        } catch (error) {

            console.error(
                "Failed to create user:",
                error
            );

            setAddUserError(
                error.response?.data?.detail ||
                "Unable to create user."
            );

        } finally {

            setAddUserLoading(false);

        }

    };
    // =========================================
// EDIT USER
// =========================================

const handleEditUser = async (e) => {

    e.preventDefault();

    if (!editingUser) {
        return;
    }

    try {

        setEditUserLoading(true);
        setEditUserError("");

        await updateUser(
            editingUser.id,
            {
                full_name: editingUser.full_name,
                email: editingUser.email,
                role: editingUser.role
            }
        );

        setShowEditUser(false);
        setEditingUser(null);

        const updatedUsers = await getAllUsers();

        setUsers(updatedUsers);

    } catch (error) {

        console.error(
            "Failed to update user:",
            error
        );

        setEditUserError(
            error.response?.data?.detail ||
            "Unable to update user."
        );

    } finally {

        setEditUserLoading(false);

    }
};
// =========================================
// ACTIVATE / DEACTIVATE USER
// =========================================

const handleToggleUserStatus = async (currentUser) => {

    const action = currentUser.is_active
        ? "deactivate"
        : "activate";

    const confirmed = window.confirm(
        `Are you sure you want to ${action} ${currentUser.full_name}?`
    );

    if (!confirmed) {
        return;
    }

    try {

        await updateUserStatus(
            currentUser.id,
            !currentUser.is_active
        );

        const updatedUsers = await getAllUsers();

        setUsers(updatedUsers);

    } catch (error) {

        console.error(
            "Failed to update user status:",
            error
        );

        alert(
            error.response?.data?.detail ||
            "Unable to update user status."
        );
    }
};


    // =====================================================
    // FILTER USERS
    // =====================================================

    const filteredUsers = users.filter(
        (currentUser) => {

            const search =
                searchTerm.toLowerCase();


            const matchesSearch =
                currentUser.full_name
                    ?.toLowerCase()
                    .includes(search) ||

                currentUser.email
                    ?.toLowerCase()
                    .includes(search);


            const matchesRole =
                roleFilter === "all" ||
                currentUser.role === roleFilter;


            return (
                matchesSearch &&
                matchesRole
            );

        }
    );


    // =====================================================
    // USER COUNTS
    // =====================================================

    const totalUsers =
        users.length;
        const activeUserCount =
    users.filter(
        (currentUser) =>
            currentUser.is_active
    ).length;


    const learnerCount =
        users.filter(
            (currentUser) =>
                currentUser.role === "learner"
        ).length;


    const instructorCount =
        users.filter(
            (currentUser) =>
                currentUser.role === "instructor"
        ).length;


    const trainerCount =
        users.filter(
            (currentUser) =>
                currentUser.role ===
                "accessibility_trainer"
        ).length;


    const administratorCount =
        users.filter(
            (currentUser) =>
                currentUser.role ===
                "administrator"
        ).length;


    // =====================================================
    // LOGOUT
    // =====================================================

    const handleLogout = () => {

        logout();

        navigate("/");

    };


    // =====================================================
    // ROLE DISPLAY
    // =====================================================

    const formatRole = (role) => {

        if (role === "accessibility_trainer") {

            return "Accessibility Trainer";

        }

        if (role === "administrator") {

            return "Administrator";

        }

        if (role === "instructor") {

            return "Instructor";

        }

        if (role === "learner") {

            return "Learner";

        }

        return role;

    };


    // =====================================================
    // RENDER
    // =====================================================

    return (

        <div className="admin-dashboard">


            {/* =================================================
                SIDEBAR
            ================================================= */}

            <aside className="admin-sidebar">


                {/* BRAND */}

                <div className="admin-brand">

                    <div className="admin-brand-icon">
                        ✋
                    </div>

                    <div>

                        <h2>
                            SignSync
                        </h2>

                        <span>
                            Administrator
                        </span>

                    </div>

                </div>


                {/* NAVIGATION */}

                <nav className="admin-nav">


                    {/* OVERVIEW */}

                    <button
                        className={`admin-nav-item ${
                            activeSection === "overview"
                                ? "active"
                                : ""
                        }`}
                        onClick={() =>
                            setActiveSection("overview")
                        }
                    >

                        <span>
                            📊
                        </span>

                        Overview

                    </button>


                    {/* USERS */}

                    <button
                        className={`admin-nav-item ${
                            activeSection === "users"
                                ? "active"
                                : ""
                        }`}
                        onClick={() =>
                            setActiveSection("users")
                        }
                    >

                        <span>
                            👥
                        </span>

                        User Management

                    </button>


                    {/* CONTENT */}

                    <button
                        className={`admin-nav-item ${
                            activeSection === "content"
                                ? "active"
                                : ""
                        }`}
                        onClick={() =>
                            setActiveSection("content")
                        }
                    >

                        <span>
                            📚
                        </span>

                        Content Management

                    </button>


                   

                    {/* REPORTS */}

                    <button
                        className={`admin-nav-item ${
                            activeSection === "reports"
                                ? "active"
                                : ""
                        }`}
                        onClick={() =>
                            setActiveSection("reports")
                        }
                    >

                        <span>
                            📈
                        </span>

                        Reports

                    </button>


                    {/* SETTINGS */}

                    <button
                        className={`admin-nav-item ${
                            activeSection === "settings"
                                ? "active"
                                : ""
                        }`}
                        onClick={() =>
                            setActiveSection("settings")
                        }
                    >

                        <span>
                            ⚙️
                        </span>

                        Settings

                    </button>


                </nav>


                {/* LOGOUT */}

                <div className="admin-sidebar-footer">

                    <button
                        className="admin-logout-button"
                        onClick={handleLogout}
                    >

                        <span>
                            🚪
                        </span>

                        Logout

                    </button>

                </div>


            </aside>



            {/* =================================================
                MAIN CONTENT
            ================================================= */}

            <main className="admin-main">


                {/* =================================================
                    HEADER
                ================================================= */}

                <header className="admin-header">

                    <div>

                        <h1>
                            Administrator Dashboard
                        </h1>

                        <p>
                            Manage and monitor the
                            SignSync platform.
                        </p>

                    </div>


                    <div className="admin-profile">

                        <div className="admin-avatar">

                            {user?.full_name
                                ?.charAt(0)
                                .toUpperCase() || "A"}

                        </div>


                        <div>

                            <strong>

                                {user?.full_name ||
                                    "Administrator"}

                            </strong>

                            <span>
                                Administrator
                            </span>

                        </div>

                    </div>

                </header>



                {/* =================================================
                    OVERVIEW
                ================================================= */}

                {activeSection === "overview" && (

                    <section className="admin-section">


                        {/* WELCOME */}

                        <div className="admin-welcome-card">

                            <div>

                                <span className="admin-eyebrow">
                                    SYSTEM OVERVIEW
                                </span>

                                <h2>

                                    Welcome back,{" "}

                                    {user?.full_name ||
                                        "Administrator"}

                                    {" "}👋

                                </h2>

                                <p>
                                    Here's a quick overview
                                    of your SignSync platform.
                                </p>

                            </div>


                            <div className="admin-welcome-icon">
                                🛡️
                            </div>

                        </div>



                        {/* =================================================
                            STATISTICS
                        ================================================= */}

                        <div className="admin-stat-grid">


                            {/* TOTAL USERS */}

                            <div className="admin-stat-card">

                                <div className="stat-icon">
                                    👥
                                </div>

                                <div>

                                    <span>
                                        Total Users
                                    </span>

                                    <strong>
                                        {totalUsers}
                                    </strong>

                                </div>

                            </div>


                            {/* LEARNERS */}

                            <div className="admin-stat-card">

                                <div className="stat-icon">
                                    👨‍🎓
                                </div>

                                <div>

                                    <span>
                                        Total Learners
                                    </span>

                                    <strong>
                                        {learnerCount}
                                    </strong>

                                </div>

                            </div>


                            {/* INSTRUCTORS */}

                            <div className="admin-stat-card">

                                <div className="stat-icon">
                                    👨‍🏫
                                </div>

                                <div>

                                    <span>
                                        Instructors
                                    </span>

                                    <strong>
                                        {instructorCount}
                                    </strong>

                                </div>

                            </div>


                            {/* TRAINERS */}

                            <div className="admin-stat-card">

                                <div className="stat-icon">
                                    ♿
                                </div>

                                <div>

                                    <span>
                                        Accessibility Trainers
                                    </span>

                                    <strong>
                                        {trainerCount}
                                    </strong>

                                </div>

                            </div>


                        </div>



                        {/* =================================================
                            SYSTEM + QUICK ACTIONS
                        ================================================= */}

                        <div className="admin-content-grid">


                            {/* SYSTEM STATUS */}

                            <div className="admin-panel">

                                <div className="admin-panel-header">

                                    <div>

                                        <span className="admin-eyebrow">
                                            SYSTEM
                                        </span>

                                        <h3>
                                            System Status
                                        </h3>

                                    </div>


                                    <span className="status-badge online">
                                        ● Online
                                    </span>

                                </div>


                                <div className="system-status-list">


                                    <div className="system-status-item">

                                        <span>
                                            Backend API
                                        </span>

                                        <strong className="status-online">
                                            Operational
                                        </strong>

                                    </div>


                                    <div className="system-status-item">

                                        <span>
                                            Authentication
                                        </span>

                                        <strong className="status-online">
                                            Operational
                                        </strong>

                                    </div>


                                    <div className="system-status-item">

                                        <span>
                                            AI Recognition
                                        </span>

                                        <strong className="status-online">
                                            Operational
                                        </strong>

                                    </div>


                                    <div className="system-status-item">

                                        <span>
                                            Database
                                        </span>

                                        <strong className="status-online">
                                            Operational
                                        </strong>

                                    </div>


                                </div>

                            </div>



                            {/* QUICK ACTIONS */}

                            <div className="admin-panel">

                                <div className="admin-panel-header">

                                    <div>

                                        <span className="admin-eyebrow">
                                            ACTIONS
                                        </span>

                                        <h3>
                                            Quick Actions
                                        </h3>

                                    </div>

                                </div>


                                <div className="quick-actions">


                                    <button
                                        onClick={() =>
                                            setActiveSection(
                                                "users"
                                            )
                                        }
                                    >

                                        <span>
                                            👥
                                        </span>

                                        Manage Users

                                    </button>


                                    <button
                                        onClick={() =>
                                            setActiveSection(
                                                "content"
                                            )
                                        }
                                    >

                                        <span>
                                            📚
                                        </span>

                                        Manage Content

                                    </button>


                                   


                                    <button
                                        onClick={() =>
                                            setActiveSection(
                                                "reports"
                                            )
                                        }
                                    >

                                        <span>
                                            📈
                                        </span>

                                        View Reports

                                    </button>


                                </div>

                            </div>


                        </div>


                    </section>

                )}



                {/* =================================================
                    USER MANAGEMENT
                ================================================= */}

                {activeSection === "users" && (

                    <section className="admin-section">


                        {/* HEADING */}

                        <div className="section-heading">

                            <span className="admin-eyebrow">
                                ADMINISTRATION
                            </span>

                            <h2>
                                User Management
                            </h2>

                            <p>
                                Manage learners, instructors
                                and accessibility trainers.
                            </p>

                        </div>



                        {/* USER STATISTICS */}

                        <div className="admin-stat-grid">


                            <div className="admin-stat-card">

                                <div className="stat-icon">
                                    👥
                                </div>

                                <div>

                                    <span>
                                        Total Users
                                    </span>

                                    <strong>
                                        {totalUsers}
                                    </strong>

                                </div>

                            </div>


                            <div className="admin-stat-card">

                                <div className="stat-icon">
                                    👨‍🎓
                                </div>

                                <div>

                                    <span>
                                        Learners
                                    </span>

                                    <strong>
                                        {learnerCount}
                                    </strong>

                                </div>

                            </div>


                            <div className="admin-stat-card">

                                <div className="stat-icon">
                                    👨‍🏫
                                </div>

                                <div>

                                    <span>
                                        Instructors
                                    </span>

                                    <strong>
                                        {instructorCount}
                                    </strong>

                                </div>

                            </div>


                            <div className="admin-stat-card">

                                <div className="stat-icon">
                                    ♿
                                </div>

                                <div>

                                    <span>
                                        Accessibility Trainers
                                    </span>

                                    <strong>
                                        {trainerCount}
                                    </strong>

                                </div>

                            </div>


                        </div>



                        {/* =================================================
                            USER TABLE
                        ================================================= */}

                        <div className="admin-panel user-management-panel">


                            {/* HEADER */}

                            <div className="admin-panel-header">

                                <div>

                                    <span className="admin-eyebrow">
                                        USERS
                                    </span>

                                    <h3>
                                        All Users
                                    </h3>

                                </div>


                                <div className="user-header-actions">

                                    <span className="user-count-badge">

                                        {filteredUsers.length}
                                        {" "}users

                                    </span>


                                    <button
                                        className="add-user-button"
                                        onClick={() => {

                                            setAddUserError("");

                                            setShowAddUser(true);

                                        }}
                                    >

                                        + Add User

                                    </button>

                                </div>


                            </div>



                            {/* SEARCH + FILTER */}

                            <div className="user-management-controls">


                                <div className="user-search">

                                    <span>
                                        🔍
                                    </span>

                                    <input
                                        type="text"
                                        placeholder="Search by name or email..."
                                        value={searchTerm}
                                        onChange={(e) =>
                                            setSearchTerm(
                                                e.target.value
                                            )
                                        }
                                    />

                                </div>


                                <select
                                    value={roleFilter}
                                    onChange={(e) =>
                                        setRoleFilter(
                                            e.target.value
                                        )
                                    }
                                >

                                    <option value="all">
                                        All Roles
                                    </option>

                                    <option value="learner">
                                        Learners
                                    </option>

                                    <option value="instructor">
                                        Instructors
                                    </option>

                                    <option value="accessibility_trainer">
                                        Accessibility Trainers
                                    </option>

                                    <option value="administrator">
                                        Administrators
                                    </option>

                                </select>


                            </div>



                            {/* LOADING */}

                            {usersLoading && (

                                <div className="user-message">

                                    Loading users...

                                </div>

                            )}



                            {/* ERROR */}

                            {usersError && (

                                <div className="user-error">

                                    ⚠️ {usersError}

                                </div>

                            )}



                            {/* TABLE */}

                            {!usersLoading &&
                                !usersError && (

                                    <div className="users-table-wrapper">

                                        <table className="users-table">


                                            <thead>

                                                <tr>

                                                    <th>
                                                        User
                                                    </th>

                                                    <th>
                                                        Email
                                                    </th>

                                                    <th>
                                                        Role
                                                    </th>

                                                  <th>
    User ID
</th>

<th>
    Status
</th>

<th>
    Actions
</th>

                                                </tr>

                                            </thead>



                                            <tbody>


                                                {filteredUsers.length > 0 ? (

                                                    filteredUsers.map(
                                                        (currentUser) => (

                                                            <tr
                                                                key={
                                                                    currentUser.id
                                                                }
                                                            >


                                                                {/* NAME */}

                                                                <td>

                                                                    <div className="user-table-name">

                                                                        <div className="user-table-avatar">

                                                                            {currentUser.full_name
                                                                                ?.charAt(0)
                                                                                .toUpperCase()}

                                                                        </div>

                                                                        <strong>

                                                                            {
                                                                                currentUser.full_name
                                                                            }

                                                                        </strong>

                                                                    </div>

                                                                </td>


                                                                {/* EMAIL */}

                                                                <td>

                                                                    {
                                                                        currentUser.email
                                                                    }

                                                                </td>


                                                                {/* ROLE */}

                                                                <td>

                                                                    <span
                                                                        className={`role-badge role-${currentUser.role}`}
                                                                    >

                                                                        {
                                                                            formatRole(
                                                                                currentUser.role
                                                                            )
                                                                        }

                                                                    </span>

                                                                </td>


                                                                {/* ID */}

                                                                <td>

                                                                    #
                                                                    {
                                                                        currentUser.id
                                                                    }

                                                                </td>
                                                                <td>

    <span
        className={
            currentUser.is_active
                ? "user-status active"
                : "user-status inactive"
        }
    >

        ●

        {currentUser.is_active
            ? " Active"
            : " Inactive"}

    </span>

</td>


<td>

    <div className="user-actions">

        <button
            className="edit-user-button"
            onClick={() => {

                setEditUserError("");

                setEditingUser({
                    id: currentUser.id,
                    full_name: currentUser.full_name,
                    email: currentUser.email,
                    role: currentUser.role
                });

                setShowEditUser(true);

            }}
        >
            ✏️ Edit
        </button>


        <button
            className={
                currentUser.is_active
                    ? "deactivate-user-button"
                    : "activate-user-button"
            }
            onClick={() =>
                handleToggleUserStatus(
                    currentUser
                )
            }
        >

            {currentUser.is_active
                ? "🔴 Deactivate"
                : "🟢 Activate"}

        </button>

    </div>

</td>


                                                            </tr>

                                                        )
                                                    )

                                                ) : (

                                                    <tr>

                                                        <td
                                                           colSpan="6"
                                                            className="no-users"
                                                        >

                                                            No users found.

                                                        </td>

                                                    </tr>

                                                )}


                                            </tbody>


                                        </table>

                                    </div>

                                )}


                        </div>


                    </section>

                )}



                {/* =================================================
                    CONTENT MANAGEMENT
                ================================================= */}
{activeSection === "content" && (

    <section className="admin-section content-management-section">

        <ContentManagement />

    </section>

)}




{/* =================================================
    REPORTS
================================================= */}

{activeSection === "reports" && (

    <section className="admin-section reports-container">

        <Reports />

    </section>

)}{/* =================================================
    SETTINGS
================================================= */}

{activeSection === "settings" && (

    <section className="admin-section">

        {/* PAGE HEADING */}
        <div className="section-heading">

            <span className="admin-eyebrow">
                CONFIGURATION
            </span>

            <h2>
                Settings
            </h2>

            <p>
                Manage your SignSync administrator preferences.
            </p>

        </div>


        {/* SETTINGS GRID */}
        <div className="admin-content-grid">


            {/* PLATFORM INFORMATION */}
            <div className="admin-panel">

                <div className="admin-panel-header">

                    <div>

                        <span className="admin-eyebrow">
                            PLATFORM
                        </span>

                        <h3>
                            Platform Information
                        </h3>

                    </div>

                </div>


                <div className="system-status-list">

                    <div className="system-status-item">

                        <span>
                            Application
                        </span>

                        <strong>
                            SignSync
                        </strong>

                    </div>


                    <div className="system-status-item">

                        <span>
                            Version
                        </span>

                        <strong>
                            1.0.0
                        </strong>

                    </div>


                    <div className="system-status-item">

                        <span>
                            Backend API
                        </span>

                        <strong className="status-online">
                            ● Operational
                        </strong>

                    </div>


                    <div className="system-status-item">

                        <span>
                            AI Recognition
                        </span>

                        <strong className="status-online">
                            ● Operational
                        </strong>

                    </div>

                </div>

            </div>


            {/* ADMINISTRATOR PREFERENCES */}
            <div className="admin-panel">

                <div className="admin-panel-header">

                    <div>

                        <span className="admin-eyebrow">
                            PREFERENCES
                        </span>

                        <h3>
                            Administrator Preferences
                        </h3>

                    </div>

                </div>


                <div className="settings-options">


                    {/* NOTIFICATIONS */}
                    <div className="settings-option">

                        <div>

                            <strong>
                                Notifications
                            </strong>

                            <p>
                                Receive important platform notifications.
                            </p>

                        </div>

                        <label className="settings-toggle">

                            <input
                                type="checkbox"
                                defaultChecked
                            />

                            <span className="settings-slider"></span>

                        </label>

                    </div>


                    {/* REPORT UPDATES */}
                    <div className="settings-option">

                        <div>

                            <strong>
                                Report Updates
                            </strong>

                            <p>
                                Keep learning reports updated automatically.
                            </p>

                        </div>

                        <label className="settings-toggle">

                            <input
                                type="checkbox"
                                defaultChecked
                            />

                            <span className="settings-slider"></span>

                        </label>

                    </div>


                </div>

            </div>

        </div>


        {/* SYSTEM ACTIONS */}
        <div className="admin-panel settings-actions-panel">

            <div className="admin-panel-header">

                <div>

                    <span className="admin-eyebrow">
                        SYSTEM
                    </span>

                    <h3>
                        System Actions
                    </h3>

                </div>

            </div>


            <div className="quick-actions">

                <button
                    onClick={() => window.location.reload()}
                >

                    <span>
                        🔄
                    </span>

                    Refresh System

                </button>


                <button
                    onClick={() =>
                        setActiveSection("overview")
                    }
                >

                    <span>
                        ←
                    </span>

                    Back to Overview

                </button>

            </div>

        </div>

    </section>

)}
                {/* =========================================
    EDIT USER MODAL
========================================= */}

{showEditUser && editingUser && (

    <div className="admin-modal-overlay">

        <div className="admin-modal">

            <div className="admin-modal-header">

                <div>

                    <span className="admin-eyebrow">
                        USER MANAGEMENT
                    </span>

                    <h2>
                        Edit User
                    </h2>

                </div>

                <button
                    className="modal-close-button"
                    onClick={() => {
                        setShowEditUser(false);
                        setEditingUser(null);
                    }}
                >
                    ✕
                </button>

            </div>


            <form
                onSubmit={handleEditUser}
                className="admin-user-form"
            >

                <div className="input-group">

                    <label>
                        Full Name
                    </label>

                    <input
                        type="text"
                        value={editingUser.full_name}
                        onChange={(e) =>
                            setEditingUser({
                                ...editingUser,
                                full_name:
                                    e.target.value
                            })
                        }
                        required
                    />

                </div>


                <div className="input-group">

                    <label>
                        Email
                    </label>

                    <input
                        type="email"
                        value={editingUser.email}
                        onChange={(e) =>
                            setEditingUser({
                                ...editingUser,
                                email:
                                    e.target.value
                            })
                        }
                        required
                    />

                </div>


                <div className="input-group">

                    <label>
                        Role
                    </label>

                    <select
                        value={editingUser.role}
                        onChange={(e) =>
                            setEditingUser({
                                ...editingUser,
                                role:
                                    e.target.value
                            })
                        }
                    >

                        <option value="learner">
                            Learner
                        </option>

                        <option value="instructor">
                            Instructor
                        </option>

                        <option value="accessibility_trainer">
                            Accessibility Trainer
                        </option>

                        <option value="administrator">
                            Administrator
                        </option>

                    </select>

                </div>


                {editUserError && (

                    <div className="user-error">

                        ⚠️ {editUserError}

                    </div>

                )}


                <div className="admin-modal-actions">

                    <button
                        type="button"
                        className="modal-cancel-button"
                        onClick={() => {

                            setShowEditUser(false);
                            setEditingUser(null);

                        }}
                    >
                        Cancel
                    </button>


                    <button
                        type="submit"
                        className="modal-save-button"
                        disabled={editUserLoading}
                    >

                        {editUserLoading
                            ? "Saving..."
                            : "Save Changes"}

                    </button>

                </div>

            </form>

        </div>

    </div>

)}


            </main>



            {/* =====================================================
                ADD USER MODAL
            ===================================================== */}

            {showAddUser && (

                <div className="admin-modal-overlay">


                    <div className="admin-modal">


                        {/* MODAL HEADER */}

                        <div className="admin-modal-header">

                            <div>

                                <span className="admin-eyebrow">
                                    ADMINISTRATION
                                </span>

                                <h2>
                                    Add New User
                                </h2>

                            </div>


                            <button
                                className="modal-close-button"
                                onClick={() =>
                                    setShowAddUser(false)
                                }
                            >
                                ✕
                            </button>

                        </div>



                        {/* FORM */}

                        <form
                            onSubmit={handleAddUser}
                            className="add-user-form"
                        >


                            {/* NAME */}

                            <div className="input-group">

                                <label>
                                    Full Name
                                </label>

                                <input
                                    type="text"
                                    placeholder="Enter full name"
                                    value={
                                        newUser.full_name
                                    }
                                    onChange={(e) =>
                                        setNewUser({
                                            ...newUser,
                                            full_name:
                                                e.target.value
                                        })
                                    }
                                    required
                                />

                            </div>



                            {/* EMAIL */}

                            <div className="input-group">

                                <label>
                                    Email
                                </label>

                                <input
                                    type="email"
                                    placeholder="Enter email"
                                    value={
                                        newUser.email
                                    }
                                    onChange={(e) =>
                                        setNewUser({
                                            ...newUser,
                                            email:
                                                e.target.value
                                        })
                                    }
                                    required
                                />

                            </div>



                            {/* PASSWORD */}

                            <div className="input-group">

                                <label>
                                    Password
                                </label>

                                <input
                                    type="password"
                                    placeholder="Enter password"
                                    value={
                                        newUser.password
                                    }
                                    onChange={(e) =>
                                        setNewUser({
                                            ...newUser,
                                            password:
                                                e.target.value
                                        })
                                    }
                                    required
                                />

                            </div>



                            {/* ROLE */}

                            <div className="input-group">

                                <label>
                                    Role
                                </label>

                                <select
                                    value={
                                        newUser.role
                                    }
                                    onChange={(e) =>
                                        setNewUser({
                                            ...newUser,
                                            role:
                                                e.target.value
                                        })
                                    }
                                >

                                    <option value="learner">
                                        Learner
                                    </option>

                                    <option value="instructor">
                                        Instructor
                                    </option>

                                    <option value="accessibility_trainer">
                                        Accessibility Trainer
                                    </option>

                                    <option value="administrator">
                                        Administrator
                                    </option>

                                </select>

                            </div>



                            {/* ERROR */}

                            {addUserError && (

                                <div className="user-error">

                                    ⚠️ {addUserError}

                                </div>

                            )}



                            {/* BUTTONS */}

                            <div className="modal-actions">


                                <button
                                    type="button"
                                    className="modal-cancel-button"
                                    onClick={() =>
                                        setShowAddUser(false)
                                    }
                                >

                                    Cancel

                                </button>


                                <button
                                    type="submit"
                                    className="modal-submit-button"
                                    disabled={
                                        addUserLoading
                                    }
                                >

                                    {addUserLoading
                                        ? "Creating..."
                                        : "Create User"}

                                </button>


                            </div>


                        </form>


                    </div>

                </div>

            )}


        </div>

    );

}