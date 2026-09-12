import { useEffect, useState } from "react";
import InstructorLeaderboard
    from "./InstructorLeaderboard";
import InstructorSidebar from "./InstructorSidebar";
import InstructorHeader from "./InstructorHeader";
import InstructorStats from "./InstructorStats";
import TopPerformers from "./TopPerformers";
import { getInstructorDashboard } from "../../services/instructorDashboardService";

export default function InstructorDashboard() {
const [dashboard, setDashboard] = useState(null);
const [loading, setLoading] = useState(true);
const [error, setError] = useState("");


useEffect(() => {
    async function loadDashboard() {
        try {
            setLoading(true);
            setError("");

            const data = await getInstructorDashboard();

            setDashboard(data);
           
        } catch (err) {
            console.error(
                "Failed to load instructor dashboard:",
                err
            );

            setError(
                "Unable to load instructor dashboard."
            );
        } finally {
            setLoading(false);
        }
    }

    loadDashboard();
}, []);

/* ============================================
   LOADING
============================================ */

if (loading) {
    return (
        <div style={pageStyle}>
            <div style={centerMessageStyle}>
                <div style={spinnerStyle}>⟳</div>

                <h2 style={{ margin: "10px 0 5px" }}>
                    Loading Instructor Dashboard
                </h2>

                <p
                    style={{
                        margin: 0,
                        color: "#9ca3af"
                    }}
                >
                    Fetching student progress...
                </p>
            </div>
        </div>
    );
}

/* ============================================
   ERROR
============================================ */

if (error) {
    return (
        <div style={pageStyle}>
            <div style={centerMessageStyle}>
                <div
                    style={{
                        fontSize: "42px",
                        marginBottom: "10px"
                    }}
                >
                    ⚠️
                </div>

                <h2 style={{ margin: "0 0 8px" }}>
                    Something went wrong
                </h2>

                <p
                    style={{
                        margin: 0,
                        color: "#6b7280"
                    }}
                >
                    {error}
                </p>
            </div>
        </div>
    );
}

/* ============================================
   EMPTY DASHBOARD
============================================ */

if (!dashboard) {
    return (
        <div style={pageStyle}>
            <div style={centerMessageStyle}>
                <div
                    style={{
                        fontSize: "42px",
                        marginBottom: "10px"
                    }}
                >
                    📊
                </div>

                <h2 style={{ margin: "0 0 8px" }}>
                    No dashboard data
                </h2>

                <p
                    style={{
                        margin: 0,
                        color: "#6b7280"
                    }}
                >
                    There is currently no instructor
                    dashboard information available.
                </p>
            </div>
        </div>
    );
}

/* ============================================
   STUDENTS
============================================ */

const students = dashboard.students || [];

const studentsNeedingAttention = students
    .filter((student) =>
        Number(student.accuracy ?? 0) < 60 &&
        student.certification_level !== "Intermediate" &&
        student.certification_level !== "Advanced" &&
        student.certification_level !== "Professional"
    )
    .sort(
        (a, b) =>
            Number(a.accuracy ?? 0) -
            Number(b.accuracy ?? 0)
    );

/* ============================================
   DASHBOARD
============================================ */

return (
    <div style={pageStyle}>
        <div style={dashboardLayoutStyle}>

            {/* ============================================
                INSTRUCTOR SIDEBAR
            ============================================ */}

            <InstructorSidebar
                dashboard={dashboard}
            />

            {/* ============================================
                MAIN CONTENT
            ============================================ */}

            <main style={mainContentStyle}>

                <InstructorHeader />

                <InstructorStats
                    dashboard={dashboard}
                />

                <div
    style={{
        display: "grid",
        gridTemplateColumns:
            "repeat(auto-fit,minmax(220px,1fr))",
        gap: "18px",
        marginBottom: "28px"
    }}
>

   <CertificationCard
    title="Beginner"
    value={dashboard.beginner_students}
    icon="🥉"
/>

<CertificationCard
    title="Intermediate"
    value={dashboard.intermediate_students}
    icon="🥈"
/>

<CertificationCard
    title="Advanced"
    value={dashboard.advanced_students}
    icon="🥇"
/>

<CertificationCard
    title="Professional"
    value={dashboard.professional_students}
    icon="🏆"
/>
</div>

                {/* ============================================
                    ATTENTION NEEDED
                ============================================ */}

                
                <TopPerformersSection
    students={students}
/>
                <InstructorLeaderboard
    students={students}
/>

                {/* ============================================
                    STUDENT PROGRESS
                ============================================ */}

                

            </main>

        </div>
    </div>
);


}

/* ============================================================
ATTENTION NEEDED SECTION
============================================================ */

function AttentionSection({ students }) {
return (
<div
style={{
background: "#ffffff",
borderRadius: "16px",
border: "1px solid #e5e7eb",
boxShadow:
"0 4px 14px rgba(15, 23, 42, 0.06)",
marginBottom: "28px",
overflow: "hidden"
}}
>


        {/* HEADER */}

        <div
            style={{
                padding: "20px 24px",
                borderBottom:
                    "1px solid #eef0f4",
                display: "flex",
                alignItems: "center",
                gap: "12px"
            }}
        >

            <div
                style={{
                    width: "40px",
                    height: "40px",
                    borderRadius: "11px",
                    background: "#FEF2F2",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: "19px"
                }}
            >
                ⚠️
            </div>

            <div>

                <h2
                    style={{
                        margin: 0,
                        fontSize: "18px",
                        color: "#111827"
                    }}
                >
                    Attention Needed
                </h2>

                <p
                    style={{
                        margin: "4px 0 0",
                        color: "#9ca3af",
                        fontSize: "13px"
                    }}
                >
                    Learners who may need additional practice
                </p>

            </div>

        </div>

        {/* STUDENTS */}

        {students.length === 0 ? (

            <div
                style={{
                    padding: "25px",
                    display: "flex",
                    alignItems: "center",
                    gap: "12px",
                    color: "#15803D"
                }}
            >

                <span style={{ fontSize: "22px" }}>
                    ✓
                </span>

                <div>

                    <strong>
                        All students are doing well!
                    </strong>

                    <div
                        style={{
                            fontSize: "13px",
                            color: "#6b7280",
                            marginTop: "3px"
                        }}
                    >
                        No learners currently require
                        immediate attention.
                    </div>

                </div>

            </div>

        ) : (

            <div>

                {students.map((student, index) => (
                    <AttentionStudent
                        key={
                            student.student_id ||
                            `attention-${index}`
                        }
                        student={student}
                    />
                ))}

            </div>

        )}

    </div>
);


}

/* ============================================================
ATTENTION STUDENT
============================================================ */

function AttentionStudent({ student }) {


const accuracy =
    Number(student.accuracy ?? 0);

const completed =
    Number(student.completed_letters ?? 0);

const studentName =
    student.student_name || `Learner ${student.student_id}`;

return (
    <div
        style={{
            padding: "16px 24px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            gap: "20px",
            borderBottom:
                "1px solid #f1f3f5",
            flexWrap: "wrap"
        }}
    >

        {/* STUDENT */}

        <div
            style={{
                display: "flex",
                alignItems: "center",
                gap: "12px"
            }}
        >

            <div
                style={{
                    width: "38px",
                    height: "38px",
                    borderRadius: "50%",
                    background: "#FEF2F2",
                    color: "#DC2626",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontWeight: "700"
                }}
            >
                {String(studentName)
                    .charAt(0)
                    .toUpperCase()}
            </div>

            <div>

                <div
                    style={{
                        fontWeight: "600",
                        color: "#1f2937"
                    }}
                >
                    {studentName}
                </div>

                <div
                    style={{
                        fontSize: "12px",
                        color: "#9ca3af"
                    }}
                >
                    Current letter:{" "}
                    {student.current_letter || "-"}
                </div>

            </div>

        </div>

        {/* PROGRESS + ACCURACY */}

        <div
            style={{
                display: "flex",
                alignItems: "center",
                gap: "28px"
            }}
        >

            <div
                style={{
                    textAlign: "right"
                }}
            >

                <div
                    style={{
                        fontSize: "11px",
                        color: "#9ca3af",
                        textTransform: "uppercase",
                        fontWeight: "600"
                    }}
                >
                    Progress
                </div>

                <div
                    style={{
                        fontSize: "13px",
                        color: "#4b5563",
                        fontWeight: "600"
                    }}
                >
                    {completed}/26 letters
                </div>

            </div>

            <div
                style={{
                    padding: "6px 11px",
                    borderRadius: "20px",
                    background: "#FEF2F2",
                    color: "#DC2626",
                    fontWeight: "700",
                    fontSize: "13px"
                }}
            >
                {accuracy}%
            </div>

        </div>

    </div>
);


}
function TopPerformersSection({ students }) {

    const topStudents = [...students]
        .sort(
            (a, b) =>
                Number(b.accuracy || 0) -
                Number(a.accuracy || 0)
        )
        .slice(0, 5);

    return (

        <div
            style={{
                background: "#ffffff",
                borderRadius: "16px",
                border: "1px solid #e5e7eb",
                boxShadow:
                    "0 4px 14px rgba(15,23,42,0.06)",
                marginBottom: "28px",
                overflow: "hidden"
            }}
        >

            <div
                style={{
                    padding: "20px 24px",
                    borderBottom:
                        "1px solid #eef0f4"
                }}
            >


              <h2
    style={{
        margin: 0,
        fontSize: "18px",
        color: "#111827"
    }}
>
    🏆 Top Performers
</h2>

<p
    style={{
        marginTop: "6px",
        color: "#6b7280"
    }}
>
    Learners with the highest assessment accuracy
</p>

            </div>

            {topStudents.map((student, index) => (

    <div
        key={student.student_id || index}
        style={{
            padding: "16px 24px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            borderBottom: "1px solid #f3f4f6"
        }}
    >

        <div
            style={{
                display: "flex",
                alignItems: "center",
                gap: "12px"
            }}
        >

            <div
                style={{
                    width: "42px",
                    height: "42px",
                    borderRadius: "50%",
                    background:
                        index === 0
                            ? "#FEF3C7"
                            : index === 1
                            ? "#E5E7EB"
                            : index === 2
                            ? "#FED7AA"
                            : "#EEF2FF",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontWeight: "700",
                    color: "#111827"
                }}
            >
                {index === 0
                    ? "🥇"
                    : index === 1
                    ? "🥈"
                    : index === 2
                    ? "🥉"
                    : index + 1}
            </div>

            <div>
                <div
                    style={{
                        fontWeight: "700",
                        color: "#111827"
                    }}
                >
                    {student.student_name || `Learner ${index + 1}`}
                </div>

                <div
                    style={{
                        fontSize: "12px",
                        color: "#6b7280"
                    }}
                >
                    Top Performer
                </div>
            </div>

        </div>

        <div
            style={{
                padding: "8px 14px",
                borderRadius: "999px",
                background: "#DCFCE7",
                color: "#15803D",
                fontWeight: "700",
                fontSize: "13px"
            }}
        >
            ⭐ {Number(student.accuracy || 0).toFixed(2)}%
        </div>

    </div>

))}

        </div>

    );

}
/* ============================================================
PAGE
============================================================ */
function CertificationCard({
    title,
    value,
    icon
}) {

    return (
        <div
            style={{
                background: "#fff",
                borderRadius: "16px",
                padding: "22px",
                border: "1px solid #e5e7eb",
                boxShadow:
                    "0 4px 14px rgba(15,23,42,0.06)"
            }}
        >
            <div
                style={{
                    fontSize: "32px",
                    marginBottom: "12px"
                }}
            >
                {icon}
            </div>

            <h3
                style={{
                    margin: 0,
                    color: "#111827"
                }}
            >
                {value}
            </h3>

            <p
                style={{
                    marginTop: "8px",
                    color: "#6b7280"
                }}
            >
                {title} Learners
            </p>
        </div>
    );
}
const pageStyle = {
minHeight: "100vh",

background:
    "linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%)",

padding: "28px 24px",

boxSizing: "border-box"


};

/* ============================================================
DASHBOARD LAYOUT
============================================================ */

const dashboardLayoutStyle = {
    width: "100%",
    maxWidth: "1600px",
    margin: "0 auto",
    display: "grid",
    gridTemplateColumns: "250px minmax(0, 1fr)",
    gap: "28px",
    alignItems: "stretch"
};

/* ============================================================
MAIN CONTENT
============================================================ */

const mainContentStyle = {
minWidth: 0,


width: "100%"


};

/* ============================================================
LOADING / ERROR / EMPTY STATE
============================================================ */

const centerMessageStyle = {
minHeight: "70vh",


display: "flex",

flexDirection: "column",

alignItems: "center",

justifyContent: "center",

textAlign: "center",

color: "#1f2937"


};

const spinnerStyle = {
fontSize: "42px",

color: "#4F46E5",

animation:
    "spin 1s linear infinite"

    

};
