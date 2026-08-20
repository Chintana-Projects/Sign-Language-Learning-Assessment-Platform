
import React from "react";

function ScoreCard({
    score = 0,
    correct = 0,
    total = 0,
    accuracy = null
}) {

    // =====================================
    // SCORE
    // =====================================

    let displayScore = 0;

    let grade = "";

    let components = {};


    // =====================================
    // Handle score object
    // =====================================

    if (
        typeof score === "object" &&
        score !== null
    ) {

        displayScore = Number(
            score.overall_score ??
            score.sign_score ??
            0
        );

        grade =
            score.grade ??
            "";

        components =
            score.components ??
            {};

    }

    // =====================================
    // Handle score number
    // =====================================

    else {

        displayScore =
            Number(score ?? 0);

    }


    // =====================================
    // Safe attempts conversion
    // =====================================

    const correctAttempts =
        Number(correct) || 0;

    const totalAttempts =
        Number(total) || 0;


    // =====================================
    // Accuracy
    // =====================================

    let displayAccuracy = 0;


    if (accuracy !== null) {

        displayAccuracy =
            Number(accuracy) || 0;

    }

    else if (totalAttempts > 0) {

        displayAccuracy =
            (
                correctAttempts /
                totalAttempts
            ) * 100;

    }


    // =====================================
    // Render
    // =====================================

    return (

        <div className="score-card">

            {/* =================================
                TITLE
            ================================= */}

            <h2>
                🏆 Practice Score
            </h2>


            {/* =================================
                SCORE
            ================================= */}

            <h1>

                {displayScore.toFixed(2)}%

            </h1>


            {/* =================================
                GRADE
            ================================= */}

            {
                grade && (

                    <h3>

                        Grade: {grade}

                    </h3>

                )
            }


            {/* =================================
                ATTEMPTS
            ================================= */}

            <p>

                <b>
                    Correct Attempts:
                </b>{" "}

                {correctAttempts}

                {" / "}

                {totalAttempts}

            </p>


            {/* =================================
                ACCURACY
            ================================= */}

            {
                totalAttempts > 0 && (

                    <p>

                        <b>
                            Accuracy:
                        </b>{" "}

                        {displayAccuracy.toFixed(2)}%

                    </p>

                )
            }


            {/* =================================
                SCORE BREAKDOWN
            ================================= */}

            {
                Object.keys(components).length > 0 && (

                    <div className="score-components">

                        <h3>
                            Score Breakdown
                        </h3>


                        {
                            Object.entries(
                                components
                            ).map(
                                ([key, value]) => {

                                    const numericValue =
                                        Number(value);

                                    return (

                                        <p key={key}>

                                            <b>

                                                {
                                                    key
                                                        .replaceAll(
                                                            "_",
                                                            " "
                                                        )
                                                        .replace(
                                                            /\b\w/g,
                                                            char =>
                                                                char.toUpperCase()
                                                        )
                                                }

                                            </b>

                                            :{" "}

                                            {
                                                Number.isFinite(
                                                    numericValue
                                                )
                                                    ? numericValue.toFixed(2)
                                                    : value
                                            }

                                            %

                                        </p>

                                    );

                                }
                            )
                        }

                    </div>

                )
            }

        </div>

    );

}


export default ScoreCard;

