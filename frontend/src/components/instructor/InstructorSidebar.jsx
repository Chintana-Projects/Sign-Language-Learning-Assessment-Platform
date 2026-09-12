
import { useNavigate } from "react-router-dom";

export default function InstructorSidebar() {
    const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    localStorage.removeItem("role");

    navigate("/");
};
    const navigate = useNavigate();

    return (
        <aside
            style={{
                width: "250px",
                flexShrink: 0,

               background: "#111827",
border: "1px solid #1f2937",
color: "#ffffff",
display: "flex",
flexDirection: "column",
                borderRadius: "16px",

                boxShadow:
                    "0 4px 14px rgba(15, 23, 42, 0.06)",

                padding: "22px",

                boxSizing: "border-box",

                /* =========================================
                   EXTEND SIDEBAR TO BOTTOM
                ========================================= */

                minHeight: "calc(100vh - 56px)",

                height: "100%",

                position: "sticky",

                top: "28px",

                alignSelf: "stretch"
            }}
        >

            {/* =========================================
                PROFILE
            ========================================= */}

            <div
                style={{
                    textAlign: "center",

                    paddingBottom: "22px",

                    borderBottom:
                        "1px solid #eef0f4"
                }}
            >

                <div
                    style={{
                        width: "68px",

                        height: "68px",

                        margin: "0 auto 12px",

                        borderRadius: "50%",

                        background:
                            "linear-gradient(135deg, #4F46E5, #7C3AED)",

                        display: "flex",

                        alignItems: "center",

                        justifyContent: "center",

                        color: "#ffffff",

                        fontSize: "28px"
                    }}
                >
                    👨‍🏫
                </div>


                <h2
                    style={{
                        margin: 0,

                        fontSize: "18px",
                        color: "#ffffff",

                        fontWeight: "700"
                    }}
                >
                    Instructor
                </h2>


                <p
                    style={{
                        margin: "5px 0 0",

                        fontSize: "13px",

                       color: "#d1d5db"
                    }}
                >
                    Instructor Account
                </p>

            </div>


            {/* =========================================
                NAVIGATION
            ========================================= */}

            <nav
                style={{
                    marginTop: "20px",

                    display: "flex",

                    flexDirection: "column",

                    gap: "8px"
                }}
            >

                {/* Dashboard */}

                <button
                    type="button"

                    onClick={() =>
                        navigate("/instructor/dashboard")
                    }

                    style={{
                        width: "100%",

                        border: "none",

                        borderRadius: "10px",

                        padding: "11px 13px",

                      background: "#4F46E5",
color: "#ffffff",

                        fontSize: "14px",

                        fontWeight: "700",

                        textAlign: "left",

                        cursor: "pointer"
                    }}
                >
                    📊 Dashboard
                </button>


                {/* Students */}

                <button
                    type="button"

                    onClick={() =>
                        navigate("/instructor/students")
                    }

                    style={sidebarButtonStyle}
                >
                    👥 Students
                </button>


                {/* Reports */}

                <button
                    type="button"

                    onClick={() =>
                        navigate("/instructor/reports")
                    }

                    style={sidebarButtonStyle}
                >
                    📈 Reports
                </button>

            </nav>

            {/* =========================================
                STATUS
            ========================================= */}

            <div
                style={{
                    marginTop: "22px",
                    padding: "13px",
                    borderRadius: "11px",
                    background: "#1f2937",
                    border: "1px solid #374151"
                }}
            >
                <div
                    style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "8px"
                    }}
                >
                    <span
                        style={{
                            width: "8px",
                            height: "8px",
                            borderRadius: "50%",
                            background: "#22C55E",
                            display: "inline-block"
                        }}
                    />

                    <span
                        style={{
                            fontSize: "12px",
                            color: "#ffffff",
                            fontWeight: "600"
                        }}
                    >
                        Dashboard Active
                    </span>
                </div>

                <p
                    style={{
                        margin: "7px 0 0",
                        fontSize: "11px",
                        lineHeight: "1.5",
                        color: "#9ca3af"
                    }}
                >
                    Monitor learner progress and classroom
                    performance.
                </p>
            </div>

            {/* =========================================
                LOGOUT
            ========================================= */}

            <div
                style={{
                    marginTop: "auto",
                    paddingTop: "20px",
                    borderTop: "1px solid #374151"
                }}
            >
                <button
                    type="button"
                    onClick={handleLogout}
                    style={{
                        width: "100%",
                        border: "none",
                        borderRadius: "10px",
                        padding: "12px",
                        background: "#7f1d1d",
                        color: "#ffffff",
                        fontSize: "14px",
                        fontWeight: "600",
                        cursor: "pointer"
                    }}
                >
                    🚪 Logout
                </button>
            </div>

        </aside>
    );
}


/* =========================================
   SIDEBAR BUTTON
========================================= */

const sidebarButtonStyle = {
    width: "100%",
    border: "none",
    borderRadius: "10px",
    padding: "11px 13px",
    background: "transparent",
    color: "#d1d5db",
    fontSize: "14px",
    fontWeight: "600",
    textAlign: "left",
    cursor: "pointer"
};