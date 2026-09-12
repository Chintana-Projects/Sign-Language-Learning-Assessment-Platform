import React from "react";
import { Outlet } from "react-router-dom";

import AccessibilitySidebar from "../components/dashboard/AccessibilitySidebar";

import "../styles/accessibilityLayout.css";
export default function AccessibilityLayout() {

    return (
        <div className="accessibility-layout">

            {/* ================================
                SIDEBAR
            ================================= */}
            <aside className="accessibility-sidebar-wrapper">
                <AccessibilitySidebar />
            </aside>


            {/* ================================
                RIGHT SIDE
            ================================= */}
            <div className="accessibility-right">

                {/* ================================
                    TOP HEADER
                ================================= */}
                <header className="accessibility-header">

                    <div className="accessibility-header-title">
                        <h1>Accessibility Trainer</h1>
                        <p>Monitor learner progress and performance</p>
                    </div>

                    <div className="trainer-profile">
                        <div className="trainer-avatar">
                            AT
                        </div>
                    </div>

                </header>


                {/* ================================
                    PAGE CONTENT
                ================================= */}
                <main className="accessibility-main">
                    <Outlet />
                </main>

            </div>

        </div>
    );
}