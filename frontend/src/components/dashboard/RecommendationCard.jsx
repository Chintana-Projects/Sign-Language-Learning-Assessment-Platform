import { FaRobot, FaArrowRight, FaBolt } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
export default function RecommendationCard({
    nextPractice = null,
    recommendations = []
}) {
    const recommendation =
        nextPractice || recommendations?.[0] || {};

    const letter =
        recommendation.alphabet ||
        recommendation.letter ||
        "C";

    const message =
        recommendation.message ||
        recommendation.description ||
        "Next alphabet in learning sequence.";
    const navigate = useNavigate();
    const priority =
        recommendation.priority || "HIGH";

    const priorityColors = {
        HIGH: {
            background: "#FEF2F2",
            color: "#DC2626"
        },
        MEDIUM: {
            background: "#FFF7ED",
            color: "#EA580C"
        },
        LOW: {
            background: "#ECFDF5",
            color: "#16A34A"
        }
    };

    const priorityStyle =
        priorityColors[priority] ||
        priorityColors.MEDIUM;

    return (
        <div style={cardStyle}>

            {/* ================= HEADER ================= */}

            <div style={headerStyle}>

                <div style={headerLeftStyle}>

                    <div style={aiIconStyle}>
                        <FaRobot />
                    </div>

                    <div>
                        <h2 style={titleStyle}>
                            AI Recommendation
                        </h2>

                        <p style={subtitleStyle}>
                            Personalized learning suggestion
                        </p>
                    </div>

                </div>

                <div
                    style={{
                        ...priorityBadgeStyle,
                        background:
                            priorityStyle.background,
                        color:
                            priorityStyle.color
                    }}
                >
                    <FaBolt size={10} />
                    {priority}
                </div>

            </div>


            {/* ================= RECOMMENDATION ================= */}

            <div style={recommendationStyle}>

                {/* Letter */}

                <div style={letterContainerStyle}>

                    <span style={letterLabelStyle}>
                        NEXT
                    </span>

                    <span style={letterStyle}>
                        {letter}
                    </span>

                </div>


                {/* Content */}

                <div style={contentStyle}>

                    <h3 style={recommendationTitleStyle}>
                        Continue with letter {letter}
                    </h3>

                    <p style={messageStyle}>
                        {message}
                    </p>

                    <div style={reasonStyle}>
                        <span style={reasonDotStyle} />

                        <span>
                            Next alphabet in your
                            learning sequence
                        </span>
                    </div>

                </div>

            </div>


            {/* ================= FOOTER ================= */}

            <div style={footerStyle}>

                <div style={aiMessageStyle}>
                    <FaRobot size={12} />

                    <span>
                        Recommendation generated from your
                        learning progress
                    </span>
                </div>

 <button
    style={buttonStyle}
    onClick={() => navigate("/dashboard/practice")}
>
    Start Practice
    <FaArrowRight size={11} />
</button>
            </div>

        </div>
    );
}


/* ============================================
   CARD
============================================ */

const cardStyle = {
    background:
        "linear-gradient(135deg, #FFFFFF 0%, #FAFAFF 100%)",
    border: "1px solid #E5E7EB",
    borderRadius: "20px",
    padding: "24px",
    marginTop: "24px",
    boxShadow:
        "0 8px 24px rgba(15, 23, 42, 0.07)",
    position: "relative",
    overflow: "hidden"
};


/* ============================================
   HEADER
============================================ */

const headerStyle = {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "15px",
    marginBottom: "22px"
};

const headerLeftStyle = {
    display: "flex",
    alignItems: "center",
    gap: "12px"
};

const aiIconStyle = {
    width: "44px",
    height: "44px",
    borderRadius: "13px",
    background:
        "linear-gradient(135deg, #EEF2FF, #F5F3FF)",
    color: "#6366F1",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "19px"
};

const titleStyle = {
    margin: 0,
    fontSize: "19px",
    fontWeight: "700",
    color: "#111827"
};

const subtitleStyle = {
    margin: "4px 0 0",
    fontSize: "12px",
    color: "#9CA3AF"
};


/* ============================================
   PRIORITY
============================================ */

const priorityBadgeStyle = {
    display: "flex",
    alignItems: "center",
    gap: "5px",
    padding: "6px 10px",
    borderRadius: "20px",
    fontSize: "11px",
    fontWeight: "800",
    letterSpacing: "0.04em"
};


/* ============================================
   RECOMMENDATION
============================================ */

const recommendationStyle = {
    display: "flex",
    alignItems: "center",
    gap: "20px",
    background: "#F8FAFC",
    border: "1px solid #EEF0F4",
    borderRadius: "16px",
    padding: "18px"
};

const letterContainerStyle = {
    width: "78px",
    height: "78px",
    flexShrink: 0,
    borderRadius: "18px",
    background:
        "linear-gradient(135deg, #4F46E5, #7C3AED)",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    boxShadow:
        "0 8px 18px rgba(79, 70, 229, 0.25)"
};

const letterLabelStyle = {
    color: "rgba(255,255,255,0.7)",
    fontSize: "9px",
    fontWeight: "800",
    letterSpacing: "0.12em"
};

const letterStyle = {
    color: "#FFFFFF",
    fontSize: "34px",
    lineHeight: "1",
    fontWeight: "800",
    marginTop: "3px"
};


/* ============================================
   CONTENT
============================================ */

const contentStyle = {
    flex: 1,
    minWidth: 0
};

const recommendationTitleStyle = {
    margin: "0 0 5px",
    fontSize: "17px",
    fontWeight: "700",
    color: "#1F2937"
};

const messageStyle = {
    margin: "0 0 10px",
    fontSize: "13px",
    lineHeight: "1.5",
    color: "#6B7280"
};

const reasonStyle = {
    display: "flex",
    alignItems: "center",
    gap: "7px",
    fontSize: "11px",
    color: "#9CA3AF"
};

const reasonDotStyle = {
    width: "6px",
    height: "6px",
    borderRadius: "50%",
    background: "#6366F1"
};


/* ============================================
   FOOTER
============================================ */

const footerStyle = {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "15px",
    marginTop: "18px",
    paddingTop: "16px",
    borderTop: "1px solid #EEF0F4",
    flexWrap: "wrap"
};

const aiMessageStyle = {
    display: "flex",
    alignItems: "center",
    gap: "7px",
    color: "#9CA3AF",
    fontSize: "11px"
};

const buttonStyle = {
    display: "flex",
    alignItems: "center",
    gap: "8px",
    border: "none",
    borderRadius: "10px",
    padding: "10px 15px",
    background:
        "linear-gradient(135deg, #4F46E5, #7C3AED)",
    color: "#FFFFFF",
    fontSize: "12px",
    fontWeight: "700",
    cursor: "pointer",
    boxShadow:
        "0 5px 12px rgba(79,70,229,0.2)"
};