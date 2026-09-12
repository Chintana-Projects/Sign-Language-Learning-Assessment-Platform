import React, { useState, useEffect } from "react";
import "../../styles/AdministratorDashboard.css";

export default function AdminSystemMonitoring() {
    const [metrics, setMetrics] = useState({
        totalAssessments: 197,
        avgAccuracy: 42.13,
        avgConfidence: 69.24,
        activeSessions: 0,
        uptimeSeconds: 3402,
        status: "Healthy"
    });

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    // Format uptime seconds into HH:MM:SS
    const formatUptime = (totalSeconds) => {
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;

        const pad = (num) => String(num).padStart(2, "0");
        return `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
    };

    // Increment uptime counter live
    useEffect(() => {
        const interval = setInterval(() => {
            setMetrics((prev) => ({
                ...prev,
                uptimeSeconds: prev.uptimeSeconds + 1
            }));
        }, 1000);

        return () => clearInterval(interval);
    }, []);

    return (
        <div className="admin-monitoring-container">
            {/* =====================================================
                STATISTICS CARDS GRID
            ===================================================== */}
            <div className="monitoring-stats-grid">
                <div className="monitoring-stat-card">
                    <div className="stat-icon">📋</div>
                    <div className="stat-content">
                        <span>Total Assessments</span>
                        <strong>{metrics.totalAssessments}</strong>
                    </div>
                </div>

                <div className="monitoring-stat-card">
                    <div className="stat-icon">🎯</div>
                    <div className="stat-content">
                        <span>Average Accuracy</span>
                        <strong>{metrics.avgAccuracy.toFixed(2)}%</strong>
                    </div>
                </div>

                <div className="monitoring-stat-card">
                    <div className="stat-icon">🤖</div>
                    <div className="stat-content">
                        <span>Confidence Score</span>
                        <strong>{metrics.avgConfidence.toFixed(2)}%</strong>
                    </div>
                </div>

                <div className="monitoring-stat-card">
                    <div className="stat-icon">👤</div>
                    <div className="stat-content">
                        <span>Active Sessions</span>
                        <strong>{metrics.activeSessions}</strong>
                    </div>
                </div>
            </div>

            {/* =====================================================
                PERFORMANCE METRICS (PROGRESS BARS)
            ===================================================== */}
            <div className="admin-panel performance-metrics-panel">
                <div className="admin-panel-header">
                    <div>
                        <span className="admin-eyebrow">ANALYTICS</span>
                        <h3>Performance Metrics</h3>
                    </div>
                </div>

                <div className="metrics-progress-grid">
                    <div className="metric-progress-card">
                        <div className="metric-header">
                            <span>Average Accuracy</span>
                            <strong>{metrics.avgAccuracy.toFixed(2)}%</strong>
                        </div>
                        <div className="progress-bar">
                            <div
                                className="progress-fill accuracy"
                                style={{ width: `${Math.min(metrics.avgAccuracy, 100)}%` }}
                            />
                        </div>
                    </div>

                    <div className="metric-progress-card">
                        <div className="metric-header">
                            <span>Confidence Score</span>
                            <strong>{metrics.avgConfidence.toFixed(2)}%</strong>
                        </div>
                        <div className="progress-bar">
                            <div
                                className="progress-fill confidence"
                                style={{ width: `${Math.min(metrics.avgConfidence, 100)}%` }}
                            />
                        </div>
                    </div>
                </div>
            </div>

            {/* =====================================================
                SYSTEM HEALTH PANEL
            ===================================================== */}
            <div className="monitoring-panel system-health-panel">
    <div className="health-panel-header">
        <div>
            <span className="panel-eyebrow">INFRASTRUCTURE</span>
            <h3 className="panel-title">System Health</h3>
        </div>
        <span className={`health-badge ${metrics.status.toLowerCase()}`}>
            <span className="badge-dot" />
            {metrics.status}
        </span>
    </div>

    <div className="health-grid">
        <div className="health-card">
            <span className="health-label">System Uptime</span>
            <strong className="health-value font-mono">{formatUptime(metrics.uptimeSeconds)}</strong>
        </div>

        <div className="health-card">
            <span className="health-label">Database</span>
            <strong className="health-value status-online">Operational</strong>
        </div>

        <div className="health-card">
            <span className="health-label">API Gateway</span>
            <strong className="health-value status-online">Operational</strong>
        </div>

        <div className="health-card">
            <span className="health-label">Recognition Service</span>
            <strong className="health-value status-online">Operational</strong>
        </div>
    </div>
</div>
        </div>
    );
}