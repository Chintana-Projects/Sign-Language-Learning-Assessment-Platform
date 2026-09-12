import React, { useEffect, useState } from "react";

import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,

    BarChart,
    Bar,

    PieChart,
    Pie,
    Cell,

    AreaChart,
    Area
} from "recharts";

const COLORS = [
    "#0088FE",
    "#00C49F",
    "#FFBB28",
    "#FF8042"
];

function AdminAnalytics() {

    const [analytics, setAnalytics] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchAnalytics();
    }, []);

    async function fetchAnalytics() {

        try {

            const response = await fetch(
                "http://127.0.0.1:8000/admin/analytics"
            );

            const data = await response.json();

            if (data.success) {
                setAnalytics(data.analytics);
            }

        } catch (error) {

            console.error(
                "Analytics Error:",
                error
            );

        } finally {

            setLoading(false);

        }
    }

    if (loading) {
        return (
            <div className="admin-page">
                <h2>Loading Analytics...</h2>
            </div>
        );
    }

    if (!analytics) {
        return (
            <div className="admin-page">
                <h2>No analytics available</h2>
            </div>
        );
    }

    return (

        <div className="admin-page">

            <h1>
                📊 Platform Analytics
                
            </h1>

            {/* ========================= */}
            {/* KPI CARDS */}
            {/* ========================= */}

            <div className="stats-grid">

                <div className="stat-card">
                    <h3>Total Users</h3>
                    <p>{analytics.total_users}</p>
                </div>

                <div className="stat-card">
                    <h3>Total Assessments</h3>
                    <p>{analytics.total_assessments}</p>
                </div>

                <div className="stat-card">
                    <h3>Avg Accuracy</h3>
                    <p>{analytics.average_accuracy}%</p>
                </div>

                <div className="stat-card">
                    <h3>Avg Confidence</h3>
                    <p>{analytics.average_confidence}%</p>
                </div>

            </div>

            {/* ========================= */}
            {/* USER GROWTH */}
            {/* ========================= */}

            <div className="chart-card">

                <h2>
                    User Growth
                </h2>

                <ResponsiveContainer
                    width="100%"
                    height={300}
                >

                    <LineChart
                        data={analytics.user_growth}
                    >

                        <CartesianGrid strokeDasharray="3 3" />

                        <XAxis dataKey="date" />

                        <YAxis />

                        <Tooltip />

                        <Line
                            type="monotone"
                            dataKey="count"
                            stroke="#8884d8"
                        />

                    </LineChart>

                </ResponsiveContainer>

            </div>

            {/* ========================= */}
            {/* ACCURACY TREND */}
            {/* ========================= */}

            <div className="chart-card">

                <h2>
                    Accuracy Trend
                </h2>

                <ResponsiveContainer
                    width="100%"
                    height={300}
                >

                    <AreaChart
                        data={analytics.accuracy_trends}
                    >

                        <CartesianGrid strokeDasharray="3 3" />

                        <XAxis dataKey="date" />

                        <YAxis />

                        <Tooltip />

                        <Area
                            type="monotone"
                            dataKey="accuracy"
                            stroke="#82ca9d"
                            fill="#82ca9d"
                        />

                    </AreaChart>

                </ResponsiveContainer>

            </div>

            {/* ========================= */}
            {/* ASSESSMENT ACTIVITY */}
            {/* ========================= */}

            <div className="chart-card">

                <h2>
                    Assessment Activity
                </h2>

                <ResponsiveContainer
                    width="100%"
                    height={300}
                >

                    <BarChart
                        data={analytics.assessment_activity}
                    >

                        <CartesianGrid strokeDasharray="3 3" />

                        <XAxis dataKey="date" />

                        <YAxis />

                        <Tooltip />

                        <Bar
                            dataKey="assessments"
                            fill="#8884d8"
                        />

                    </BarChart>

                </ResponsiveContainer>

            </div>

            {/* ========================= */}
            {/* ROLE DISTRIBUTION */}
            {/* ========================= */}

            <div className="chart-card">

                <h2>
                    Role Distribution
                </h2>

                <ResponsiveContainer
                    width="100%"
                    height={300}
                >

                    <PieChart>

                        <Pie
                            data={
                                analytics.role_distribution
                            }
                            dataKey="value"
                            nameKey="name"
                            outerRadius={100}
                            label
                        >

                            {
                                analytics.role_distribution.map(
                                    (entry, index) => (
                                        <Cell
                                            key={index}
                                            fill={
                                                COLORS[
                                                index %
                                                COLORS.length
                                                ]
                                            }
                                        />
                                    )
                                )
                            }

                        </Pie>

                        <Tooltip />

                    </PieChart>

                </ResponsiveContainer>

            </div>

            {/* ========================= */}
            {/* INSIGHTS */}
            {/* ========================= */}

            <div className="chart-card">

                <h2>
                    AI Insights
                </h2>

                <p>
                    <strong>
                        Most Practiced Letter:
                    </strong>{" "}
                    {analytics.most_practiced_letter}
                </p>

                <p>
                    <strong>
                        Most Confused Pair:
                    </strong>{" "}
                    {analytics.most_confused_pair}
                </p>

            </div>

        </div>
    );
}

export default AdminAnalytics;