import {
    Routes,
    Route,
    Navigate
} from "react-router-dom";
import AllLearners from "../pages/AllLearners";
import AccessibilityTrainer
    from "../pages/AccessibilityTrainer";
import ContentManagement
    from "../pages/ContentManagement";
import LearnerDetails
    from "../pages/LearnerDetails";
import Reports
    from "../pages/Reports";
import Login
    from "../pages/Login";

import Register
    from "../pages/Register";
import Settings from "../pages/Settings";
import StudentDashboard
    from "../components/dashboard/StudentDashboard";
import LearnerDashboardLayout
    from "../components/dashboard/LearnerDashboardLayout";
import Lessons
    from "../pages/Lessons";

import InstructorDashboard
    from "../components/instructor/InstructorDashboard";

import Assessment
    from "../pages/Assessment";

import ProtectedRoute
    from "./ProtectedRoute";
import AdministratorDashboard
    from "../components/administrator/AdministratorDashboard";

export default function AppRoutes() {

    return (

        <Routes>


            {/* =========================================
                LOGIN
            ========================================= */}

            <Route
                path="/"
                element={<Login />}
            />
            <Route
    path="/accessibility-trainer/learners"
    element={<AllLearners />}
/>


            {/* =========================================
                REGISTER
            ========================================= */}
<Route
    path="/settings"
    element={
        <ProtectedRoute
            allowedRole="learner"
        >
            <Settings />
        </ProtectedRoute>
    }
/>
            <Route
                path="/register"
                element={<Register />}
            />
            {/* =========================================
    REPORTS
========================================= */}

<Route
    path="/reports"
    element={<Reports />}
/>


            {/* =========================================
                ASSESSMENT
            ========================================= */}

            <Route
                path="/assessment"
                element={<Assessment />}
            />


            {/* =========================================
                ACCESSIBILITY TRAINER DASHBOARD
            ========================================= */}

            <Route
                path="/accessibility-trainer"
                element={
                    <AccessibilityTrainer />
                }
            />
            <Route
    path="/admin/dashboard"
    element={
        <ProtectedRoute
            allowedRole="administrator"
        >
            <AdministratorDashboard />
        </ProtectedRoute>
    }
/>


            {/* =========================================
                ACCESSIBILITY TRAINER
                LEARNER DETAILS

                Works for:
                /arjun
                /priya
                /rahul
            ========================================= */}

            <Route
                path="/accessibility-trainer/learner/:learnerId"
                element={
                    <LearnerDetails />
                }
            />


            {/* =========================================
                LEARNER DASHBOARD
            ========================================= */}

            
<Route
    path="/dashboard"
    element={
        <ProtectedRoute allowedRole="learner">
            <LearnerDashboardLayout />
        </ProtectedRoute>
    }
>
    <Route
        index
        element={<StudentDashboard />}
    />

    <Route
        path="practice"
        element={<Lessons />}
    />

    <Route
        path="reports"
        element={<Reports />}
    />

    <Route
        path="settings"
        element={<Settings />}
    />
</Route>

          

            {/* =========================================
                INSTRUCTOR DASHBOARD
            ========================================= */}

            <Route
                path="/instructor/dashboard"
                element={
                    <ProtectedRoute
                        allowedRole="instructor"
                    >
                        <InstructorDashboard />
                    </ProtectedRoute>
                }
            />
            {/* =========================================
    CONTENT MANAGEMENT
========================================= */}

<Route
    path="/content-management"
    element={
        <ProtectedRoute
            allowedRole="administrator"
        >
            <ContentManagement />
        </ProtectedRoute>
    }
/>


            {/* =========================================
                UNKNOWN ROUTES
            ========================================= */}

            <Route
                path="*"
                element={
                    <Navigate
                        to="/"
                        replace
                    />
                }
            />


        </Routes>

    );

}