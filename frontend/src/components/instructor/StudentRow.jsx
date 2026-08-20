export default function StudentRow({

    student

}) {

    return (

        <tr
            style={{
                borderTop: "1px solid #E5E7EB"
            }}
        >

            <td
                style={{
                    padding: "12px 0",
                    fontWeight: "600"
                }}
            >
                {student.student_id}
            </td>

            <td>

                {student.current_letter}

            </td>

            <td>

                {student.completed_letters}

            </td>

            <td>

                <span
                    style={{
                        padding: "4px 10px",
                        borderRadius: "20px",
                        color: "#fff",
                        background:
                            student.accuracy >= 80
                                ? "#22C55E"
                                : student.accuracy >= 50
                                ? "#F59E0B"
                                : "#EF4444",
                        fontWeight: "600"
                    }}
                >
                    {student.accuracy}%
                </span>

            </td>

            <td>

                {student.total_sessions}

            </td>

            <td>

                {student.last_updated
                    ? new Date(
                          student.last_updated
                      ).toLocaleString()
                    : "-"}

            </td>

        </tr>

    );

}