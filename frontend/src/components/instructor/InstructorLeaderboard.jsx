export default function InstructorLeaderboard({
    students
}) {

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
                background: "#fff",
                padding: "20px",
                borderRadius: "16px",
                marginTop: "20px"
            }}
        >
           

          
        </div>
    );
}