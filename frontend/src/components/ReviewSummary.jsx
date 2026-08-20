import React from "react";


function ReviewSummary({
    reviewData
}) {


    if (!reviewData) {

        return (

            <div className="review-summary">

                <h3>
                    📋 Practice Summary
                </h3>

                <p>
                    No summary available.
                </p>

            </div>

        );

    }





    // ===============================
    // Motion Metrics
    // ===============================


    const motion =
        reviewData.motion_metrics || {};



    const stability =
        Number(
            motion.gesture_stability ?? 0
        );



    const confidence =
        Number(
            motion.average_confidence ?? 0
        );



    const confidencePercentage =
        confidence <= 1
        ?
        confidence * 100
        :
        confidence;



    const invalidFrames =
        motion.invalid_frames ?? 0;



    const timeTaken =
        motion.time_taken ?? 0;



    const frames =
        motion.frames_analyzed ?? 0;








    // ===============================
    // Sign Score FIX
    // ===============================


    const signScore =
    reviewData.sign_score
    ||
    reviewData.correct_attempts?.[0]?.sign_score
    ||
    {};



    const finalScore =

        Number(

            signScore.overall_score

            ??

            reviewData.overall_score

            ??

            0

        );





    const grade =

        signScore.grade

        ??

        (
            finalScore >= 90
            ?
            "Excellent"
            :
            finalScore >= 75
            ?
            "Good"
            :
            finalScore >= 50
            ?
            "Average"
            :
            "Needs Improvement"
        );









    // ===============================
    // Accuracy
    // ===============================


    const accuracy =

    Number(

        signScore.components?.accuracy

        ??

        reviewData.session_statistics?.accuracy

        ??

        0

    );







    // ===============================
    // Attempts
    // ===============================


    const correctAttempts =

        Array.isArray(
            reviewData.correct_attempts
        )

        ?

        reviewData.correct_attempts.length

        :

        (
            reviewData.total_correct
            ??
            0
        );






    const incorrectAttempts =

        Array.isArray(
            reviewData.incorrect_attempts
        )

        ?

        reviewData.incorrect_attempts.length

        :

        (
            reviewData.total_incorrect
            ??
            0
        );






    const totalAttempts =

        correctAttempts
        +
        incorrectAttempts;









    // ===============================
    // Mistakes
    // ===============================


    let mistakes = [];



    if(Array.isArray(reviewData.common_mistakes)){


        mistakes =
            reviewData.common_mistakes;


    }


    else if(reviewData.common_mistakes){


        mistakes =
            Object.entries(
                reviewData.common_mistakes
            );


    }









    // ===============================
    // Recommendations
    // ===============================


    const recommendations =


        reviewData.recommended_gestures
        ?.recommended


        ??

        reviewData.recommendations


        ??

        [];









    return (


        <div className="review-summary">







            <h2>
                📋 Practice Summary
            </h2>









            {/* Gesture Analysis */}



            <div className="summary-card">


                <h3>
                    📊 Gesture Analysis
                </h3>




                <p>

                    Gesture Stability:

                    {" "}

                    <b>
                        {stability.toFixed(2)}%
                    </b>

                </p>





                <p>

                    Average Confidence:

                    {" "}

                    <b>
                        {confidencePercentage.toFixed(2)}%
                    </b>

                </p>





                <p>

                    Invalid Frames:

                    {" "}

                    <b>
                        {invalidFrames}
                    </b>

                </p>





                <p>

                    Time Taken:

                    {" "}

                    <b>
                        {timeTaken} seconds
                    </b>

                </p>





                <p>

                    Frames Analysed:

                    {" "}

                    <b>
                        {frames}
                    </b>

                </p>



            </div>













            {/* Sign Score */}



            <div className="summary-card">


                <h3>
                    🏆 Sign Score
                </h3>




                <h1>

                    {finalScore.toFixed(2)}%

                </h1>





                <p>

                    Grade:

                    {" "}

                    <b>
                        {grade}
                    </b>

                </p>





                <p>
    Confidence:

    <b>
        {
        Number(
            signScore.components?.confidence
            ??
            confidencePercentage
        ).toFixed(2)
        }%
    </b>

</p>




<p>

    Stability:

    <b>

        {
        Number(
            signScore.components?.stability_score
            ??
            stability
        ).toFixed(2)

        }%

    </b>

</p>



            </div>












            {/* Accuracy */}



            <div className="summary-card">


                <h3>
                    🎯 Accuracy
                </h3>




                <p>

                    Accuracy:

                    {" "}

                    <b>
                        {accuracy.toFixed(2)}%
                    </b>

                </p>





                <p>

                    Total Attempts:

                    {" "}

                    <b>
                        {totalAttempts}
                    </b>

                </p>





                <p>

                    Correct Attempts:

                    {" "}

                    <b>
                        {correctAttempts}
                    </b>

                </p>





                <p>

                    Incorrect Attempts:

                    {" "}

                    <b>
                        {incorrectAttempts}
                    </b>

                </p>



            </div>












            {/* Mistakes */}



            <div className="summary-card">


                <h3>
                    ❌ Common Mistakes
                </h3>





                {

                mistakes.length > 0


                ?


                <ul>


                {


                mistakes.map(

                    (item,index)=>(


                        <li key={index}>


                        {

                        Array.isArray(item)

                        ?

                        `${item[0]} (${item[1]} times)`

                        :


                        typeof item === "object"

                        ?

                        `${item.mistake || "Unknown"} : ${item.count || 0} times`


                        :

                        item


                        }


                        </li>


                    )

                )


                }



                </ul>



                :


                <p>
                    No mistakes recorded 🎉
                </p>


                }



            </div>












            {/* Recommended Practice */}




            <div className="summary-card">


                <h3>
                    💡 Recommended Practice
                </h3>




                {


                recommendations.length > 0


                ?


                <ul>


                {


                recommendations.map(

                    (item,index)=>(


                        <li key={index}>


                        Practice:

                        {" "}


                        <b>

                        {

                        typeof item === "string"

                        ?

                        item


                        :

                        item.practice
                        ||
                        item.gesture
                        ||
                        "Unknown"


                        }


                        </b>



                        </li>


                    )

                )


                }


                </ul>



                :


                <p>
                    Keep practicing regularly.
                </p>


                }



            </div>












            {/* Next Step */}




            <div className="summary-card">


                <h3>
                    🚀 Next Step
                </h3>



                <p>

                    Continue practicing alphabet gestures
                    to improve recognition accuracy.

                </p>



            </div>






        </div>


    );


}


export default ReviewSummary;