import React, {
    useEffect,
    useState
} from "react";

import { useAuth } from "../context/AuthContext";


function ProgressDashboard({
    refresh
}) {

    const { token, user } = useAuth();

    const [progress, setProgress] = useState(null);
    const [loading, setLoading] = useState(true);


    // =====================================
    // FETCH DASHBOARD DATA
    // =====================================

    useEffect(() => {

        if (token) {
            fetchProgress();
        }

    }, [token, refresh]);


    async function fetchProgress() {

        try {

            setLoading(true);


            const response = await fetch(
                "http://127.0.0.1:8000/dashboard",
                {
                    method: "GET",

                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json"
                    }
                }
            );


            if (!response.ok) {

                if (response.status === 401) {

                    console.error(
                        "Dashboard unauthorized - token may be invalid or expired."
                    );

                }

                throw new Error(
                    `Dashboard API failed: ${response.status}`
                );

            }


            const data = await response.json();


            console.log(
                "Dashboard Response:",
                data
            );


            setProgress(data);

        }

        catch (error) {

            console.error(
                "Progress API Error:",
                error
            );

            setProgress(null);

        }

        finally {

            setLoading(false);

        }

    }


    // =====================================
    // LOADING
    // =====================================

    if (loading) {

        return (

            <div className="card">

                Loading Progress...

            </div>

        );

    }


    // =====================================
    // FAILED
    // =====================================

    if (!progress) {

        return (

            <div className="card progress-card">

                <h2>
                    📊 Learning Progress
                </h2>

                <p>
                    Unable to load progress data.
                </p>

            </div>

        );

    }


    // =====================================
    // PROFILE
    // =====================================

    const profile =
        progress.profile || {};


    // =====================================
    // BASIC STATISTICS
    // =====================================

    const totalAttempts =
        profile.total_attempts ?? 0;


    const correctAttempts =
        profile.correct_attempts ?? 0;


    const incorrectAttempts =
        profile.incorrect_attempts ?? 0;


    const overallAccuracy =
        profile.overall_accuracy ?? 0;


    // =====================================
    // COMPLETED LESSONS
    // =====================================

    const completedLetters =
        profile.completed_letters || [];


    const totalLessons = 26;


    const completedLessons =
        completedLetters.length;


    const remainingLessons =
        Math.max(
            0,
            totalLessons - completedLessons
        );


    const lessonProgress =
        Math.round(
            (
                completedLessons /
                totalLessons
            ) * 10000
        ) / 100;


    // =====================================
    // CURRENT LESSON
    // =====================================

    const currentLetter =
        profile.current_letter || "A";


    const nextLetter =
        profile.next_letter || currentLetter;


    // =====================================
    // ALPHABET MASTERY
    // =====================================

    const alphabetScores =
        profile.alphabet_mastery || {};


    const masteryEntries =
        Object.entries(
            alphabetScores
        );


    // =====================================
    // AVERAGE CONFIDENCE
    // =====================================

    const confidenceValues =
        masteryEntries
            .map(
                ([, data]) =>
                    Number(
                        data.average_confidence ?? 0
                    )
            )
            .filter(
                value =>
                    !Number.isNaN(value)
            );


    const confidence =
        confidenceValues.length > 0
            ?
            confidenceValues.reduce(
                (sum, value) =>
                    sum + value,
                0
            ) /
            confidenceValues.length
            :
            0;


    // =====================================
    // STRONGEST GESTURE
    // =====================================

    const strongestGesture =
        masteryEntries.length > 0
            ?
            [...masteryEntries].sort(
                (a, b) =>
                    Number(
                        b[1].accuracy ?? 0
                    )
                    -
                    Number(
                        a[1].accuracy ?? 0
                    )
            )[0]?.[0]
            :
            "-";


    // =====================================
    // WEAKEST GESTURE
    // =====================================

    const weakestGesture =
        masteryEntries.length > 0
            ?
            [...masteryEntries].sort(
                (a, b) =>
                    Number(
                        a[1].accuracy ?? 0
                    )
                    -
                    Number(
                        b[1].accuracy ?? 0
                    )
            )[0]?.[0]
            :
            "-";


    // =====================================
    // PRACTICE STREAK
    // =====================================

    const practiceSessions =
        profile.total_sessions ?? 0;


    // =====================================
    // RETURN
    // =====================================

    return (

        <div className="card progress-card">


            <h2>
                📊 Learning Progress
            </h2>


            {/* =================================
                LESSON PROGRESS
            ================================= */}

            <div className="lesson-progress-section">

                <h3>
                    📚 Alphabet Lessons
                </h3>


                <div className="progress-main">

                    <h1>
                        {lessonProgress}%
                    </h1>

                </div>


                <p>

                    <b>
                        {completedLessons}
                    </b>

                    {" "}of{" "}

                    <b>
                        {totalLessons}
                    </b>

                    {" "}lessons completed

                </p>


                <div
                    className="progress-bar-container"
                    style={{
                        width: "100%",
                        height: "12px",
                        background: "#e5e7eb",
                        borderRadius: "10px",
                        overflow: "hidden"
                    }}
                >

                    <div
                        className="progress-bar"
                        style={{
                            width: `${lessonProgress}%`,
                            height: "100%",
                            background: "#4f46e5",
                            borderRadius: "10px",
                            transition: "width 0.4s ease"
                        }}
                    />

                </div>


                <p>

                    {remainingLessons} lessons remaining

                </p>

            </div>


            <hr />


            {/* =================================
                CURRENT LESSON
            ================================= */}

            <div>

                <h3>
                    🎯 Current Lesson
                </h3>

                <h2>
                    {currentLetter}
                </h2>

                <p>
                    Next lesson:{" "}
                    <b>
                        {nextLetter}
                    </b>
                </p>

            </div>


            <hr />


            {/* =================================
                ATTEMPTS
            ================================= */}

            <div>

                <h3>
                    📈 Practice Statistics
                </h3>


                <p>

                    Total Attempts:{" "}

                    <b>
                        {totalAttempts}
                    </b>

                </p>


                <p>

                    Correct Attempts:{" "}

                    <b>
                        {correctAttempts}
                    </b>

                </p>


                <p>

                    Incorrect Attempts:{" "}

                    <b>
                        {incorrectAttempts}
                    </b>

                </p>


                <p>

                    Overall Accuracy:{" "}

                    <b>
                        {Number(
                            overallAccuracy
                        ).toFixed(2)}%
                    </b>

                </p>


                <p>

                    Average Confidence:{" "}

                    <b>
                        {Number(
                            confidence
                        ).toFixed(2)}%
                    </b>

                </p>

            </div>


            <hr />


            {/* =================================
                STRONGEST / WEAKEST
            ================================= */}

            <h3>
                🏆 Strongest Gesture
            </h3>

            <h2>
                {strongestGesture}
            </h2>


            <h3>
                📉 Weakest Gesture
            </h3>

            <h2>
                {weakestGesture}
            </h2>


            <h3>
                🔥 Practice Sessions
            </h3>

            <h2>
                {practiceSessions}
            </h2>


            <hr />


            {/* =================================
                ALPHABET SCORES
            ================================= */}

            <h3>
                🔤 Alphabet Scores
            </h3>


            {
                masteryEntries.length === 0

                ?

                <p>
                    No alphabet practice completed yet.
                </p>

                :

                masteryEntries.map(
                    ([letter, data]) => (

                        <p key={letter}>

                            <b>
                                {letter}
                            </b>

                            {" : "}

                            {
                                Number(
                                    data.accuracy ?? 0
                                ).toFixed(2)
                            }%

                        </p>

                    )
                )
            }


            <hr />


            {/* =================================
                RECOMMENDATIONS
            ================================= */}

            <h3>
                🎯 Recommended Practice
            </h3>


            {
                progress.recommendations?.length > 0

                ?

                progress.recommendations.map(
                    (item, index) => (

                        <p
                            key={
                                item.alphabet
                                ??
                                item.letter
                                ??
                                index
                            }
                        >

                            <b>
                                {
                                    item.alphabet
                                    ??
                                    item.letter
                                    ??
                                    "Practice"
                                }
                            </b>

                            {" - "}

                            {
                                item.reason
                                ??
                                item.message
                                ??
                                "Continue practicing."
                            }

                        </p>

                    )
                )

                :

                <p>
                    🎉 No recommendations yet.
                </p>
            }


        </div>

    );

}


export default ProgressDashboard;