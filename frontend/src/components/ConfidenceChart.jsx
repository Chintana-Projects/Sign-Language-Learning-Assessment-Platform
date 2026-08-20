
import React from "react";

import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer
} from "recharts";


// =====================================
// Confidence Formatter
// =====================================

function formatConfidence(value) {

    let confidence =
        Number(value ?? 0);

    if (confidence <= 1) {

        confidence =
            confidence * 100;

    }

    return Math.max(
        0,
        Math.min(
            confidence,
            100
        )
    );

}


// =====================================
// Confidence Chart
// =====================================

function ConfidenceChart({
    data = []
}) {


    // =====================================
    // Convert Backend Data
    // =====================================

    const formattedData =
        Array.isArray(data)

            ?

            data.map(
                (item, index) => ({

                    attempt:
                        index + 1,

                    gesture:
                        item?.gesture
                        ??
                        item?.prediction
                        ??
                        "Unknown",

                    confidence:
                        formatConfidence(
                            item?.confidence
                        )

                })
            )

            :

            [];


    // =====================================
    // Render
    // =====================================

    return (

        <div className="card chart-container">


            {/* =================================
                TITLE
            ================================= */}

            <h3>

                📈 Confidence Trend

            </h3>


            {/* =================================
                NO DATA
            ================================= */}

            {
                formattedData.length === 0

                    ?

                    (

                        <div className="chart-empty">

                            <p>
                                No confidence data available.
                            </p>

                        </div>

                    )

                    :

                    (

                        <ResponsiveContainer
                            width="100%"
                            height={300}
                        >

                            <LineChart
                                data={formattedData}
                                margin={{
                                    top: 20,
                                    right: 30,
                                    left: 20,
                                    bottom: 30
                                }}
                            >


                                {/* =================================
                                    GRID
                                ================================= */}

                                <CartesianGrid
                                    strokeDasharray="3 3"
                                />


                                {/* =================================
                                    X AXIS
                                ================================= */}

                                <XAxis
                                    dataKey="attempt"
                                    label={{
                                        value: "Attempt",
                                        position: "insideBottom",
                                        offset: -15
                                    }}
                                />


                                {/* =================================
                                    Y AXIS
                                ================================= */}

                                <YAxis
                                    domain={[0, 100]}
                                    allowDecimals={false}
                                    label={{
                                        value: "Confidence %",
                                        angle: -90,
                                        position: "insideLeft"
                                    }}
                                />


                                {/* =================================
                                    TOOLTIP
                                ================================= */}

                                <Tooltip
                                    formatter={(value) =>
                                        `${Number(value).toFixed(1)}%`
                                    }
                                    labelFormatter={(value) =>
                                        `Attempt ${value}`
                                    }
                                />


                                {/* =================================
                                    LINE
                                ================================= */}

                                <Line
                                    type="monotone"
                                    dataKey="confidence"
                                    name="Confidence"
                                    stroke="#2563eb"
                                    strokeWidth={3}
                                    dot={{
                                        r: 4
                                    }}
                                    activeDot={{
                                        r: 7
                                    }}
                                />

                            </LineChart>

                        </ResponsiveContainer>

                    )
            }

        </div>

    );

}


export default ConfidenceChart;

