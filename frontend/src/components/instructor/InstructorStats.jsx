export default function InstructorStats({ dashboard }) {
    const stats = [
        {
            title: "Total Students",
            value: dashboard.total_students ?? 0,
            icon: "👥",
            description: "Registered learners",
            iconBackground: "#EEF2FF",
            iconColor: "#4F46E5"
        },
        {
            title: "Active Students",
            value: dashboard.active_students ?? 0,
            icon: "🟢",
            description: "Have practiced",
            iconBackground: "#ECFDF5",
            iconColor: "#16A34A"
        },
        {
            title: "Completed",
            value: dashboard.completed_students ?? 0,
            icon: "🏆",
            description: "Alphabet completed",
            iconBackground: "#FFF7ED",
            iconColor: "#EA580C"
        },
        {
            title: "Average Accuracy",
            value: `${dashboard.average_accuracy ?? 0}%`,
            icon: "🎯",
            description: "Overall class accuracy",
            iconBackground: "#F5F3FF",
            iconColor: "#7C3AED"
        }
    ];

    return (
        <div
            style={{
                display: "grid",
                gridTemplateColumns:
                    "repeat(auto-fit, minmax(220px, 1fr))",
                gap: "18px",
                marginBottom: "28px"
            }}
        >
            {stats.map((stat) => (
                <StatCard
                    key={stat.title}
                    {...stat}
                />
            ))}
        </div>
    );
}

function StatCard({
    title,
    value,
    icon,
    description,
    iconBackground,
    iconColor
}) {
    return (
        <div
            style={{
                background: "#ffffff",
                borderRadius: "16px",
                padding: "22px",
                border: "1px solid #e5e7eb",
                boxShadow:
                    "0 4px 14px rgba(15, 23, 42, 0.06)",
                transition:
                    "transform 0.2s ease, box-shadow 0.2s ease",
                cursor: "default"
            }}
            onMouseEnter={(e) => {
                e.currentTarget.style.transform =
                    "translateY(-3px)";
                e.currentTarget.style.boxShadow =
                    "0 8px 22px rgba(15, 23, 42, 0.10)";
            }}
            onMouseLeave={(e) => {
                e.currentTarget.style.transform =
                    "translateY(0)";
                e.currentTarget.style.boxShadow =
                    "0 4px 14px rgba(15, 23, 42, 0.06)";
            }}
        >
            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "flex-start"
                }}
            >
                <div>
                    <p
                        style={{
                            margin: 0,
                            color: "#6b7280",
                            fontSize: "13px",
                            fontWeight: "600"
                        }}
                    >
                        {title}
                    </p>

                    <h2
                        style={{
                            margin: "10px 0 5px",
                            fontSize: "30px",
                            lineHeight: "1",
                            color: "#111827",
                            fontWeight: "700"
                        }}
                    >
                        {value}
                    </h2>

                    <p
                        style={{
                            margin: 0,
                            color: "#9ca3af",
                            fontSize: "12px"
                        }}
                    >
                        {description}
                    </p>
                </div>

                <div
                    style={{
                        width: "46px",
                        height: "46px",
                        borderRadius: "13px",
                        background: iconBackground,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        fontSize: "21px",
                        color: iconColor
                    }}
                >
                    {icon}
                </div>
            </div>
        </div>
    );
}