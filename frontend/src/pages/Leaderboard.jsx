import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/leaderboard.css";

export default function Leaderboard() {
    const [leaders, setLeaders] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        fetchLeaderboard();
    }, []);

    const fetchLeaderboard = async () => {
        try {
            const response = await fetch(
                "http://127.0.0.1:8000/leaderboard"
            );

            const data = await response.json();

            setLeaders(data || []);
        } catch (error) {
            console.error(
                "Failed to load leaderboard:",
                error
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div
            style={{
                padding: "30px",
                maxWidth: "1200px",
                margin: "0 auto"
            }}
        >
            <h2
                style={{
                    marginBottom: "8px"
                }}
            >
                🏆 Leaderboard
            </h2>

            <p
                style={{
                    color: "#666",
                    marginBottom: "25px"
                }}
            >
                Top learners ranked by performance and certification.
            </p>

            {loading ? (
                <p>Loading leaderboard...</p>
            ) : (
                <>
                    {/* Back Button */}
                    <div className="leaderboard-header">
                        <button
                            className="back-btn"
                            onClick={() => navigate(-1)}
                        >
                            ← Back
                        </button>
                    </div>

                    {/* Table Card */}
                    <div
                        style={{
                            background: "#fff",
                            borderRadius: "16px",
                            overflow: "hidden",
                            boxShadow:
                                "0 4px 20px rgba(0,0,0,0.08)"
                        }}
                    >
                        <table
                            style={{
                                width: "100%",
                                borderCollapse: "collapse"
                            }}
                        >
                            <thead>
                                <tr
                                    style={{
                                        background:
                                            "linear-gradient(90deg,#4f46e5,#7c3aed)",
                                        color: "#fff"
                                    }}
                                >
                                    <th style={headerStyle}>Rank</th>
                                    <th style={headerStyle}>Student</th>
                                    <th style={headerStyle}>Accuracy</th>
                                    <th style={headerStyle}>Progress</th>
                                    <th style={headerStyle}>Level</th>
                                    <th style={headerStyle}>Certificate</th>
                                </tr>
                            </thead>

                            <tbody>
                                {leaders.map((leader, index) => (
                                    <tr
                                        key={leader.student_id}
                                        style={{
                                            background:
                                                index % 2 === 0
                                                    ? "#fff"
                                                    : "#fafafa"
                                        }}
                                    >
                                        <td
                                            style={{
                                                ...cellStyle,
                                                textAlign: "center",
                                                fontSize: "20px"
                                            }}
                                        >
                                            {index === 0
                                                ? "🥇"
                                                : index === 1
                                                ? "🥈"
                                                : index === 2
                                                ? "🥉"
                                                : index + 1}
                                        </td>

                                        <td
                                            style={{
                                                ...cellStyle,
                                                fontWeight: "600"
                                            }}
                                        >
                                            {leader.student_name ||
                                                leader.student_id}
                                        </td>

                                        <td
                                            style={{
                                                ...cellStyle,
                                                color:
                                                    leader.accuracy >= 80
                                                        ? "#16a34a"
                                                        : "#ea580c",
                                                fontWeight: "600"
                                            }}
                                        >
                                            {leader.accuracy}%
                                        </td>

                                        <td style={cellStyle}>
                                            {leader.completed_letters}/26
                                        </td>

                                        <td style={cellStyle}>
                                            <span
                                                style={{
                                                    padding: "6px 12px",
                                                    borderRadius: "20px",
                                                    background: "#eef2ff",
                                                    color: "#4f46e5",
                                                    fontWeight: "600",
                                                    fontSize: "13px"
                                                }}
                                            >
                                                {
                                                    leader.certification_level
                                                }
                                            </span>
                                        </td>

                                        <td style={cellStyle}>
                                            {leader.certificate_id ? (
                                                <span
                                                    style={{
                                                        color: "#16a34a",
                                                        fontWeight: "600"
                                                    }}
                                                >
                                                    ✓ Certified
                                                </span>
                                            ) : (
                                                "-"
                                            )}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </>
            )}
        </div>
    );
}

const headerStyle = {
    padding: "16px",
    textAlign: "left",
    fontWeight: "600"
};

const cellStyle = {
    padding: "16px",
    borderBottom: "1px solid #eee"
};