export default function TopPerformers({ students = [] }) {
    const topStudents = [...students]
        .sort(
            (a, b) =>
                (b.accuracy || 0) -
                (a.accuracy || 0)
        )
        .slice(0, 5);

    return (
        <div
            style={{
                background: "#fff",
                borderRadius: "16px",
                padding: "24px",
                border: "1px solid #e5e7eb",
                marginBottom: "28px"
            }}
        >
            <h2
                style={{
                    marginBottom: "20px"
                }}
            >
                🏆 Top Performers
            </h2>

            {topStudents.map(
                (student, index) => (
                    <div
                        key={student.student_id}
                        style={{
                            display: "flex",
                            justifyContent:
                                "space-between",
                            padding: "12px 0",
                            borderBottom:
                                "1px solid #f3f4f6"
                        }}
                    >
                        <div>
    <strong>
        #{index + 1}
    </strong>{" "}
    {student.student_name || student.student_id}
</div>

                        <div>
                            {student.accuracy}%
                        </div>
                    </div>
                )
            )}
        </div>
    );
}