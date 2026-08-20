import "./../../../styles/dashboard/ActivityChart.css";

import {
    ResponsiveContainer,
    AreaChart,
    Area,
    CartesianGrid,
    Tooltip,
    XAxis,
    YAxis
} from "recharts";


export default function ActivityChart({
    history = []
}) {

    const today = new Date();

    const data = Array.from(
        { length: 7 },
        (_, index) => {

            const date = new Date(today);

            date.setDate(
                today.getDate() - (6 - index)
            );

            const dateKey =
                date.toISOString().split("T")[0];

            const practiceCount =
                history.filter((attempt) => {

                    if (!attempt.timestamp) {
                        return false;
                    }

                    return attempt.timestamp
                        .split("T")[0] === dateKey;

                }).length;


            return {

                day: date.toLocaleDateString(
                    "en-US",
                    {
                        weekday: "short"
                    }
                ),

                practice: practiceCount

            };

        }
    );


    return (

        <div className="activity-chart-card">

            <h3>
                Weekly Activity
            </h3>


            <ResponsiveContainer
                width="100%"
                height={250}
            >

                <AreaChart data={data}>

                    <defs>

                        <linearGradient
                            id="practiceColor"
                            x1="0"
                            y1="0"
                            x2="0"
                            y2="1"
                        >

                            <stop
                                offset="5%"
                                stopColor="#2563EB"
                                stopOpacity={0.8}
                            />

                            <stop
                                offset="95%"
                                stopColor="#2563EB"
                                stopOpacity={0}
                            />

                        </linearGradient>

                    </defs>


                    <CartesianGrid
                        strokeDasharray="3 3"
                    />


                    <XAxis
                        dataKey="day"
                    />


                    <YAxis
                        allowDecimals={false}
                    />


                    <Tooltip />


                    <Area
                        type="monotone"
                        dataKey="practice"
                        stroke="#2563EB"
                        fill="url(#practiceColor)"
                    />

                </AreaChart>

            </ResponsiveContainer>

        </div>

    );

}