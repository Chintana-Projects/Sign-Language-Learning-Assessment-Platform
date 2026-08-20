import {
    FaRobot,
    FaArrowRight,
    FaClock,
    FaBullseye
} from "react-icons/fa";

import { useNavigate } from "react-router-dom";

import "./../../../styles/dashboard/AICoachCard.css";


export default function AICoachCard({
    nextPractice = null
}) {

    const navigate = useNavigate();


    const alphabet =
        nextPractice?.alphabet || null;


    const reason =
        nextPractice?.reason ||
        "Continue practicing your sign language alphabet.";


    const priority =
        nextPractice?.priority ||
        "NORMAL";


    const handleStartPractice = () => {

        navigate("/lessons");

    };


    return (

        <div className="ai-coach-card">

            {/* ================================
                HEADER
            ================================= */}

            <div className="coach-header">

                <FaRobot className="coach-icon" />

                <h3>
                    AI Coach
                </h3>

            </div>


            {/* ================================
                BODY
            ================================= */}

            <div className="coach-body">

                <div className="coach-item">

                    <FaBullseye />

                    <span>
                        Today's Goal
                    </span>

                </div>


                {alphabet ? (

                    <p>

                        Practice letter{" "}

                        <strong>
                            {alphabet}
                        </strong>

                        {" "}to continue your
                        learning sequence.

                    </p>

                ) : (

                    <p>
                        {reason}
                    </p>

                )}


                <div className="coach-item">

                    <FaClock />

                    <span>
                        Priority
                    </span>

                </div>


                <h2>
                    {priority}
                </h2>


                {/* ================================
                    START PRACTICE
                ================================= */}

                {alphabet && (

                    <button
                        type="button"
                        onClick={handleStartPractice}
                    >

                        Start Practice

                        <FaArrowRight />

                    </button>

                )}

            </div>

        </div>

    );

}