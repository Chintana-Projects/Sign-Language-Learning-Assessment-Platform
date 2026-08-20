
import React from "react";


// =====================================
// Reference Card
// =====================================

export default function ReferenceCard({
    lesson
}) {

    // No lesson selected
    if (!lesson) {
        return null;
    }


    return (

        <div className="card reference-card">

            {/* ================================
                HEADER
            ================================= */}

            <h2>
                📖 Reference Sign
            </h2>


            {/* ================================
                CONTENT
            ================================= */}

            <div className="reference-content">


                {/* ================================
                    SIGN IMAGE
                ================================= */}

                <div className="reference-image-wrapper">

                    <img
                        src={
                            lesson.image
                                ? "/" + lesson.image
                                : ""
                        }
                        alt={
                            lesson.sign
                                ? `ASL sign ${lesson.sign}`
                                : "Reference sign"
                        }
                        className="lesson-image"
                    />

                </div>


                {/* ================================
                    SIGN INFORMATION
                ================================= */}

                <div className="reference-info">


                    {/* Letter */}

                    <div className="reference-letter">

                        {lesson.sign ?? "--"}

                    </div>


                    {/* Description */}

                    {
                        lesson.description && (

                            <p>
                                {lesson.description}
                            </p>

                        )
                    }


                    {/* Meaning */}

                    {
                        lesson.meaning && (

                            <>

                                <p>
                                    <strong>
                                        Meaning
                                    </strong>
                                </p>

                                <p>
                                    {lesson.meaning}
                                </p>

                            </>

                        )
                    }


                </div>

            </div>

        </div>

    );

}
