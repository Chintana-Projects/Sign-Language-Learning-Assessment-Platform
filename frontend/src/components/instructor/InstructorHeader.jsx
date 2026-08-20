export default function InstructorHeader() {
    const today = new Date().toLocaleDateString(
        "en-IN",
        {
            weekday: "long",
            day: "numeric",
            month: "long",
            year: "numeric"
        }
    );

    return (
        <div
            style={{
                marginBottom: "30px",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "flex-start",
                gap: "24px",
                flexWrap: "wrap"
            }}
        >
            {/* =========================================
                LEFT SIDE
            ========================================= */}

            <div style={{ flex: 1, minWidth: "280px" }}>

                <div
                    style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "14px"
                    }}
                >
                    {/* Icon */}

                    <div
                        style={{
                            width: "52px",
                            height: "52px",
                            flexShrink: 0,
                            borderRadius: "15px",
                            background:
                                "linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%)",
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "center",
                            fontSize: "25px",
                            boxShadow:
                                "0 8px 20px rgba(79, 70, 229, 0.22)"
                        }}
                    >
                        👨‍🏫
                    </div>

                    {/* Title */}

                    <div>
                        <h1
                            style={{
                                margin: 0,
                                fontSize: "30px",
                                lineHeight: "1.2",
                                fontWeight: "750",
                                letterSpacing: "-0.5px",
                                color: "#111827"
                            }}
                        >
                            Instructor Dashboard
                        </h1>

                        <p
                            style={{
                                margin: "6px 0 0",
                                color: "#6B7280",
                                fontSize: "14px",
                                fontWeight: "500"
                            }}
                        >
                            {today}
                        </p>
                    </div>
                </div>

                {/* Description */}

                <p
                    style={{
                        margin: "15px 0 0 66px",
                        color: "#6B7280",
                        fontSize: "14px",
                        lineHeight: "1.6",
                        maxWidth: "680px"
                    }}
                >
                    Monitor student progress, identify learners
                    needing attention, and track overall class
                    performance.
                </p>
            </div>

            {/* =========================================
                STATUS
            ========================================= */}

            <div
                style={{
                    display: "inline-flex",
                    alignItems: "center",
                    gap: "9px",
                    background: "#FFFFFF",
                    border: "1px solid #E5E7EB",
                    borderRadius: "999px",
                    padding: "9px 15px",
                    boxShadow:
                        "0 3px 10px rgba(15, 23, 42, 0.05)",
                    whiteSpace: "nowrap",
                    marginTop: "4px"
                }}
            >
                <span
                    style={{
                        position: "relative",
                        width: "9px",
                        height: "9px",
                        borderRadius: "50%",
                        background: "#22C55E",
                        display: "inline-block",
                        boxShadow:
                            "0 0 0 4px rgba(34, 197, 94, 0.10)"
                    }}
                />

                <span
                    style={{
                        fontSize: "13px",
                        color: "#374151",
                        fontWeight: "600"
                    }}
                >
                    Dashboard Active
                </span>
            </div>
        </div>
    );
}