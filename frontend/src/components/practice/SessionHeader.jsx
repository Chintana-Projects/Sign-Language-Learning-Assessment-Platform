export default function SessionHeader({ lesson }) {

    return (

        <div className="session-header">

            <h2>

                Learning Alphabet

                <span
                    style={{
                        color: "#2563eb",
                        marginLeft: "12px"
                    }}
                >
                    {lesson?.sign}
                </span>

            </h2>

            <p>

                Perform the sign until the AI detects
                a stable gesture.

            </p>

        </div>

    );

}