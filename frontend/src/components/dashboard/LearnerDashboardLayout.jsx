import { Outlet } from "react-router-dom";

import Header from "./Header";
import Sidebar from "./Sidebar";

import "../../pages/StudentDashboard.css";
export default function LearnerDashboardLayout() {
    return (
        <div className="dashboard">

            {/* Fixed dashboard sidebar */}
            <Sidebar />

            {/* Main dashboard area */}
            <div className="dashboard-content">

                <Header />

                {/* Page content changes here */}
                <Outlet />

            </div>

        </div>
    );
}