import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Settings.css";

export default function Settings() {
    const navigate = useNavigate();

    const [notifications, setNotifications] = useState(true);
    const [reportUpdates, setReportUpdates] = useState(true);

    const handleRefresh = () => {
        window.location.reload();
    };

    return (
        <div className="settings-page">

            {/* HEADER */}
            <div className="settings-header">
                <div>
                    <span className="settings-eyebrow">
                        SETTINGS
                    </span>

                    <h1>Settings</h1>

                    <p>
                        Manage your SignSync preferences.
                    </p>
                </div>
            </div>


            {/* PLATFORM */}
            <section className="settings-section">

                <span className="settings-eyebrow">
                    PLATFORM
                </span>

                <h2>Platform Information</h2>

                <div className="settings-card">

                    <div className="setting-row">
                        <span>Application</span>
                        <strong>SignSync</strong>
                    </div>

                    <div className="setting-row">
                        <span>Version</span>
                        <strong>1.0.0</strong>
                    </div>

                    <div className="setting-row">
                        <span>Backend API</span>
                        <strong className="status-good">
                            ● Operational
                        </strong>
                    </div>

                    <div className="setting-row">
                        <span>AI Recognition</span>
                        <strong className="status-good">
                            ● Operational
                        </strong>
                    </div>

                </div>

            </section>


            {/* PREFERENCES */}
            <section className="settings-section">

                <span className="settings-eyebrow">
                    PREFERENCES
                </span>

                <h2>Administrator Preferences</h2>

                <div className="settings-card">

                    <div className="preference-row">

                        <div>
                            <strong>Notifications</strong>

                            <p>
                                Receive important platform
                                notifications.
                            </p>
                        </div>

                        <label className="switch">

                            <input
                                type="checkbox"
                                checked={notifications}
                                onChange={(e) =>
                                    setNotifications(
                                        e.target.checked
                                    )
                                }
                            />

                            <span className="slider"></span>

                        </label>

                    </div>


                    <div className="preference-row">

                        <div>
                            <strong>Report Updates</strong>

                            <p>
                                Keep learning reports updated
                                automatically.
                            </p>
                        </div>

                        <label className="switch">

                            <input
                                type="checkbox"
                                checked={reportUpdates}
                                onChange={(e) =>
                                    setReportUpdates(
                                        e.target.checked
                                    )
                                }
                            />

                            <span className="slider"></span>

                        </label>

                    </div>

                </div>

            </section>


            {/* SYSTEM */}
            <section className="settings-section">

                <span className="settings-eyebrow">
                    SYSTEM
                </span>

                <h2>System Actions</h2>

                <div className="settings-actions">

                    <button
                        className="settings-button"
                        onClick={handleRefresh}
                    >
                        🔄 Refresh System
                    </button>

                    <button
                        className="settings-button secondary"
                        onClick={() =>
                            navigate("/dashboard")
                        }
                    >
                        ← Back to Overview
                    </button>

                </div>

            </section>

        </div>
    );
}