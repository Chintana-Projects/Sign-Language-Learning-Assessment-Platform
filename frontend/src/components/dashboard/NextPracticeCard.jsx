import "../../styles/Cards.css";
import { useNavigate } from "react-router-dom";

export default function NextPracticeCard({
    nextPractice = null
}) {

    const navigate = useNavigate();


    // ==========================================
    // NO RECOMMENDATION
    // ==========================================

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


    // ==========================================
    // DATA
    // ==========================================

    const alphabet =
        nextPractice.alphabet ||
        nextPractice.letter ||
        null;

    const reason =
        nextPractice.reason ||
        nextPractice.message ||
        nextPractice.description ||
        "Continue practicing your sign language alphabet.";

    const priority =
        nextPractice.priority ||
        "NORMAL";


    // ==========================================
    // START PRACTICE
    // ==========================================

    function handleStartPractice() {

        navigate(
            "/dashboard/practice"
        );

    }


    // ==========================================
    // CARD
    // ==========================================

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

                <button
                    className="primary-btn"
                    onClick={
                        handleStartPractice
                    }
                >
                    Start Practice
                </button>

            )}

        </div>

    );

}