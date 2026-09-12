
import {
    Routes,
    Route,
    Navigate
} from "react-router-dom";
import AdminReports
from "../pages/admin/AdminReports";
import AdminAnalytics from "../pages/AdminReports";
import AdminSystemMonitoring from "../pages/admin/AdminSystemMonitoring";
    import Certification from "../pages/Certification";
import CertificatePage from "../pages/CertificatePage";
import CertificateVerification from "../pages/CertificateVerification";
import Leaderboard from "../pages/Leaderboard";
// =====================================================
// PAGES
// =====================================================
import CertificationSession
    from "../pages/CertificationSession";
import ProfilePage from "../pages/ProfilePage";
import AllLearners
    from "../pages/AllLearners";
import CertificationResult from "../pages/CertificationResult";
import AccessibilityTrainer
    from "../pages/AccessibilityTrainer";

import AccessibilityAnalytics
    from "../pages/AccessibilityAnalytics";

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

import Settings
    from "../pages/Settings";

import Lessons
    from "../pages/Lessons";

import Assessment
    from "../pages/Assessment";


// =====================================================
// ACCESSIBILITY TRAINER LAYOUT
// =====================================================

import AccessibilityLayout from "../layouts/AccessibilityLayout";


// =====================================================
// LEARNER DASHBOARD
// =====================================================

import StudentDashboard
    from "../components/dashboard/StudentDashboard";

import LearnerDashboardLayout
    from "../components/dashboard/LearnerDashboardLayout";


// =====================================================
// INSTRUCTOR
// =====================================================

import InstructorDashboard
    from "../components/instructor/InstructorDashboard";

import InstructorStudents
    from "../components/instructor/InstructorStudents";

import InstructorReports
    from "../components/instructor/InstructorReports";

import StudentDetails
    from "../components/instructor/StudentDetails";


// =====================================================
// ADMINISTRATOR
// =====================================================

import AdministratorDashboard
    from "../components/administrator/AdministratorDashboard";


// =====================================================
// ROUTE PROTECTION
// =====================================================

import ProtectedRoute
    from "./ProtectedRoute";


// =====================================================
// APP ROUTES
// =====================================================

export default function AppRoutes() {

    return (

        <Routes>


            {/* =================================================
                LOGIN
            ================================================= */}

            <Route
                path="/"
                element={<Login />}
            />


            {/* =================================================
                REGISTER
            ================================================= */}
<Route
    path="/verify-certificate"
    element={
        <CertificateVerification />
    }
/>
<Route
    path="/admin/reports"
    element={
        <ProtectedRoute
            allowedRole="administrator"
        >
            <AdminReports />
        </ProtectedRoute>
    }
/>

            <Route
                path="/register"
                element={<Register />}
            />
            <Route
    path="/certificate"
    element={<CertificatePage />}
/>
<Route
    path="/admin/system-monitoring"
    element={<AdminSystemMonitoring />}
/>

<Route
    path="/admin/analytics"
    element={<AdminAnalytics />}
/>

            {/* =================================================
                LEARNER - SETTINGS
            ================================================= */}
<Route
    path="/dashboard/leaderboard"
    element={<Leaderboard />}
/>
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


            {/* =================================================
                LEARNER - REPORTS
            ================================================= */}

            <Route
                path="/reports"
                element={
                    <ProtectedRoute
                        allowedRole="learner"
                    >
                        <Reports />
                    </ProtectedRoute>
                }
            />


            {/* =================================================
                LEARNER - ASSESSMENT
            ================================================= */}

            <Route
                path="/assessment"
                element={
                    <ProtectedRoute
                        allowedRole="learner"
                    >
                        <Assessment />
                    </ProtectedRoute>
                }
            />


            {/* =================================================
                ACCESSIBILITY TRAINER
                SHARED LAYOUT
            ================================================= */}

            <Route
                path="/accessibility-trainer"
                element={
                    <ProtectedRoute
                        allowedRole="accessibility_trainer"
                    >
                        <AccessibilityLayout />
                    </ProtectedRoute>
                }
            >

                {/* ---------------------------------------------
                    ACCESSIBILITY TRAINER - DASHBOARD
                --------------------------------------------- */}

                <Route
                    index
                    element={<AccessibilityTrainer />}
                />


                {/* ---------------------------------------------
                    ACCESSIBILITY TRAINER - ALL LEARNERS
                --------------------------------------------- */}

                <Route
                    path="learners"
                    element={<AllLearners />}
                />


                {/* ---------------------------------------------
                    ACCESSIBILITY TRAINER - ANALYTICS
                --------------------------------------------- */}

                <Route
                    path="analytics"
                    element={<AccessibilityAnalytics />}
                />


                {/* ---------------------------------------------
                    ACCESSIBILITY TRAINER - LEARNER DETAILS
                --------------------------------------------- */}

                <Route
                    path="learner/:learnerId"
                    element={<LearnerDetails />}
                />

            </Route>


            {/* =================================================
                ADMINISTRATOR - DASHBOARD
            ================================================= */}

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

{/* =================================================
    LEARNER DASHBOARD
================================================= */}
/* =================================================
    LEARNER DASHBOARD
================================================= */

<Route
    path="/dashboard"
    element={
        <ProtectedRoute
            allowedRole="learner"
        >
            <LearnerDashboardLayout />
        </ProtectedRoute>
    }
>

    {/* Dashboard Home */}

    <Route
        index
        element={<StudentDashboard />}
    />
    <Route
    path="profile"
    element={<ProfilePage />}
/>
<Route
    path="certification/session"
    element={<CertificationSession />}
 />
    {/* Practice */}

    <Route
        path="practice"
        element={<Lessons />}
    />

    {/* Reports */}

    <Route
        path="reports"
        element={<Reports />}
    />

    {/* Certification */}

    <Route
        path="certification"
        element={<Certification />}
    />
    <Route
    path="/dashboard/certification/result"
    element={<CertificationResult />}
/>

    {/* Settings */}

    <Route
        path="settings"
        element={<Settings />}
    />

</Route>

            {/* =================================================
                INSTRUCTOR - DASHBOARD
            ================================================= */}

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


            {/* =================================================
                INSTRUCTOR - STUDENTS
            ================================================= */}

            <Route
                path="/instructor/students"
                element={
                    <ProtectedRoute
                        allowedRole="instructor"
                    >
                        <InstructorStudents />
                    </ProtectedRoute>
                }
            />


            {/* =================================================
                INSTRUCTOR - STUDENT DETAILS
            ================================================= */}

            <Route
                path="/instructor/students/:studentId"
                element={
                    <ProtectedRoute
                        allowedRole="instructor"
                    >
                        <StudentDetails />
                    </ProtectedRoute>
                }
            />


            {/* =================================================
                INSTRUCTOR - REPORTS
            ================================================= */}

            <Route
                path="/instructor/reports"
                element={
                    <ProtectedRoute
                        allowedRole="instructor"
                    >
                        <InstructorReports />
                    </ProtectedRoute>
                }
            />


            {/* =================================================
                ADMINISTRATOR - CONTENT MANAGEMENT
            ================================================= */}

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


            {/* =================================================
                UNKNOWN ROUTES
            ================================================= */}

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