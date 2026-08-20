import "../../styles/Cards.css";

export default function NextPracticeCard({
    nextPractice = null
}) {

    if (!nextPractice) {
        return (
            <div className="card">

                <h2>
                    Next Practice
                </h2>

                <p>
                    No practice recommendation available yet.
                </p>

            </div>
        );
    }


    const alphabet =
        nextPractice.alphabet;

    const reason =
        nextPractice.reason ||
        "Continue practicing your sign language alphabet.";

    const priority =
        nextPractice.priority ||
        "NORMAL";


    return (

        <div className="card">

            <h2>
                Next Practice
            </h2>

            <h3>
                {alphabet
                    ? `Alphabet - ${alphabet}`
                    : "Continue Learning"}
            </h3>

            <p>
                {reason}
            </p>

            <p>
                Priority:{" "}
                <strong>
                    {priority}
                </strong>
            </p>

            {alphabet && (

                <button className="primary-btn">
                    Start Practice
                </button>

            )}

        </div>

    );
}