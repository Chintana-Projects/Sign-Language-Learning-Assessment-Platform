import { FaPlay } from "react-icons/fa";
import { useState, useEffect } from "react";
import { FaCheckCircle } from "react-icons/fa";

import "../styles/Layout.css";
import "../styles/Cards.css";

import PracticeLayout from "../components/practice/PracticeLayout";
import PracticeReview from "../pages/PracticeReview";

import { useAuth } from "../context/AuthContext";


export default function Lessons() {

    // ==========================================
    // ALPHABET LIST
    // ==========================================

    const alphabets = [
        "A", "B", "C", "D", "E", "F",
        "G", "H", "I", "J", "K", "L",
        "M", "N", "O", "P", "Q", "R",
        "S", "T", "U", "V", "W", "X",
        "Y", "Z"
    ];


    // ==========================================
    // AUTHENTICATED USER
    // ==========================================

    const { user, accessToken } = useAuth();


    // ==========================================
    // STATES
    // ==========================================

    const [selectedLetter, setSelectedLetter] =
        useState("A");

    const [session, setSession] =
        useState(null);

    const [lesson, setLesson] =
        useState(null);

    const [lessonCache, setLessonCache] =
        useState({});

    const [prediction, setPrediction] =
        useState(null);

    const isValidAlphabet = (letter) =>
        alphabets.includes(letter);

    const [assessment, setAssessment] =
        useState(null);

    const [loading, setLoading] =
        useState(false);

    const [completedLetters, setCompletedLetters] =
        useState([]);

    const [nextPractice, setNextPractice] =
        useState(null);

    const [showReview, setShowReview] =
        useState(false);

    const [showSessionSummary, setShowSessionSummary] =
        useState(false);

    const [reviewSessionId, setReviewSessionId] =
        useState(null);

    const [masteredPopup, setMasteredPopup] =
        useState(null);


    // =====================================================
    // LOAD LOGGED-IN USER'S LEARNING PROGRESS
    // =====================================================

    useEffect(() => {

        async function loadProgress() {

            if (!accessToken || !user) {
                return;
            }

            try {

                console.log(
                    "Loading learning progress for:",
                    user
                );

                const response = await fetch(
                    "http://127.0.0.1:8000/dashboard",
                    {
                        method: "GET",

                        headers: {
                            "Authorization":
                                `Bearer ${accessToken}`
                        }
                    }
                );

                if (!response.ok) {

                    throw new Error(
                        "Unable to load dashboard progress"
                    );
                }

                const data =
                    await response.json();

                console.log(
                    "DASHBOARD PROGRESS:",
                    data
                );


                // -----------------------------------------
                // LOAD COMPLETED LETTERS
                // -----------------------------------------

                const completed =
                    Array.isArray(
                        data.completed_letters
                    )
                        ? data.completed_letters
                        : [];


                setCompletedLetters(
                    completed
                );


                // -----------------------------------------
                // LOAD CURRENT LETTER
                // -----------------------------------------

                if (
                    data.current_letter &&
                    isValidAlphabet(
                        data.current_letter
                    )
                ) {

                    setSelectedLetter(
                        data.current_letter
                    );

                }


                console.log(
                    "COMPLETED LETTERS:",
                    completed
                );

                console.log(
                    "PROGRESS:",
                    completed.length,
                    "/ 26"
                );

            }

            catch (error) {

                console.error(
                    "Progress loading error:",
                    error
                );

                // -----------------------------------------
                // IMPORTANT:
                // Do NOT keep old user's progress.
                // If dashboard cannot be loaded,
                // start with empty progress.
                // -----------------------------------------

                setCompletedLetters([]);

            }

        }


        loadProgress();

    }, [accessToken, user]);


    // ==========================================
    // SELECT LETTER
    // ==========================================

    async function selectLetter(letter) {

        if (!isValidAlphabet(letter)) {

            console.log(
                "Ignoring invalid lesson:",
                letter
            );

            return;
        }


        // Stop current practice
        setSession(null);


        // Reset recognition state
        setPrediction(null);

        setAssessment(null);

        setNextPractice(null);

        setShowReview(false);


        // Change selected letter
        setSelectedLetter(letter);


        // Check cache first
        if (lessonCache[letter]) {

            setLesson(
                lessonCache[letter]
            );

            return;
        }


        try {

            setLoading(true);


            const response =
                await fetch(
                    `http://127.0.0.1:8000/practice/lesson/${letter}`
                );


            if (!response.ok) {

                throw new Error(
                    "Unable to load lesson"
                );
            }


            const data =
                await response.json();


            if (data.lesson) {

                setLesson(
                    data.lesson
                );


                setLessonCache(prev => ({
                    ...prev,
                    [letter]: data.lesson
                }));

            }

        }

        catch (error) {

            console.error(
                "Lesson loading error:",
                error
            );

            setLesson(null);

        }

        finally {

            setLoading(false);

        }

    }


    // ==========================================
    // START PRACTICE
    // ==========================================

    async function startPractice() {

        try {

            setLoading(true);


            const lessonId =
                alphabets.indexOf(
                    selectedLetter
                ) + 1;


            const response =
                await fetch(
                    `http://127.0.0.1:8000/practice/start/${lessonId}/1`,
                    {
                        method: "POST"
                    }
                );


            const data =
                await response.json();


            console.log(
                "START RESPONSE:",
                data
            );


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Unable to start practice"
                );

            }


            setSession(
                data.session
            );


            if (data.lesson) {

                setLesson(
                    data.lesson
                );


                setLessonCache(prev => ({
                    ...prev,
                    [selectedLetter]:
                        data.lesson
                }));

            }

            else if (
                lessonCache[selectedLetter]
            ) {

                setLesson(
                    lessonCache[selectedLetter]
                );

            }


            setPrediction(null);

            setAssessment(null);

            setShowReview(false);

        }

        catch (error) {

            console.error(
                "Start Practice Error:",
                error
            );

            alert(
                error.message
            );

        }

        finally {

            setLoading(false);

        }

    }


    // ==========================================
    // HANDLE PREDICTION
    // ==========================================

    function handlePrediction(data) {

        console.log(
            "========== FULL PRACTICE RESPONSE =========="
        );

        console.log(
            JSON.stringify(data, null, 2)
        );

        console.log(
            "EXPECTED:",
            data.assessment?.expected
        );

        console.log(
            "PREDICTED:",
            data.assessment?.predicted
        );

        console.log(
            "CORRECT:",
            data.assessment?.correct
        );

        console.log(
            "LESSON SIGN:",
            lesson?.sign
        );

        console.log(
            "SELECTED LETTER:",
            selectedLetter
        );

        console.log(
            "============================================"
        );


        // ------------------------------------------
        // LIVE / STABLE PREDICTION
        // ------------------------------------------

        if (
            data.prediction ||
            data.stable_prediction
        ) {

            const stable =
                data.stable_prediction || {};


            setPrediction({

                expected:
                    lesson?.sign,

                prediction:
                    data.prediction,

                confidence:
                    data.confidence,

                validation:
                    data.validation,

                performance:
                    data.performance,

                motion_metrics:
                    data.motion_metrics,

                stable_prediction:
                    stable,

                stable:
                    stable.stable ?? false,

                stable_gesture:
                    stable.prediction ?? null,

                stable_confidence:
                    stable.confidence ?? 0,

                stable_frames:
                    stable.stable_frames ?? 0,

                required_frames:
                    stable.required_frames ?? 5,

                gesture_stability:
                    stable.gesture_stability ?? 0,

                new_stable:
                    stable.new_stable ?? false,

                majority_prediction:
                    stable.majority_prediction ?? null,

                majority_ratio:
                    stable.majority_ratio ?? 0,

                unstable_frames:
                    stable.unstable_frames ?? 0

            });

        }


        // ------------------------------------------
        // FINAL ASSESSMENT
        // ------------------------------------------

        if (data.assessment) {

            setAssessment(
                data.assessment
            );


            if (
                data.assessment.correct
            ) {

                setMasteredPopup({

                    letter:
                        data.assessment.expected,

                    next:
                        data.next_practice?.alphabet

                });


                setTimeout(() => {

                    setMasteredPopup(null);

                }, 1800);

            }


            setPrediction(prev => ({

                ...prev,

                assessment:
                    data.assessment,

                feedback:
                    data.feedback,

                sign_score:
                    data.sign_score,

                session:
                    data.session,

                profile:
                    data.profile,

                learning_state:
                    data.learning_state,

                recommendations:
                    data.recommendations,

                next_practice:
                    data.next_practice,

                dashboard:
                    data.dashboard

            }));

        }


        // ------------------------------------------
        // SESSION UPDATE
        // ------------------------------------------

        if (data.session) {

            setSession(prev => ({

                ...prev,

                ...data.session

            }));


            // Automatically load the current lesson
            // from backend

            if (
                data.session?.current_letter &&
                data.session.current_letter !==
                    selectedLetter &&
                isValidAlphabet(
                    data.session.current_letter
                )
            ) {

                selectLetter(
                    data.session.current_letter
                );

            }

        }


        // ------------------------------------------
        // KEEP ALPHABET GRID SYNCHRONIZED
        // ------------------------------------------

        if (
            data.session?.completed_letters
        ) {

            setCompletedLetters(
                data.session.completed_letters
            );

        }


        if (
            data.session?.current_letter &&
            data.session.current_letter !==
                selectedLetter
        ) {

            setSelectedLetter(
                data.session.current_letter
            );

        }


        // ------------------------------------------
        // NEXT PRACTICE
        // ------------------------------------------

        if (data.next_practice) {

            setNextPractice(
                data.next_practice
            );


            const nextAlphabet =
                data.next_practice.alphabet;


            if (
                nextAlphabet &&
                isValidAlphabet(nextAlphabet) &&
                nextAlphabet !== selectedLetter
            ) {

                setSelectedLetter(
                    nextAlphabet
                );

                selectLetter(
                    nextAlphabet
                );

            }

        }


        // ------------------------------------------
        // COMPLETED LETTERS
        // ------------------------------------------

        if (
            data.session?.completed_letters
        ) {

            setCompletedLetters(
                data.session.completed_letters
            );

        }

    }


    // ==========================================
    // FINISH PRACTICE
    // ==========================================

    async function finishPractice() {

        if (!session) {
            return;
        }


        try {

            const response =
                await fetch(
                    `http://127.0.0.1:8000/practice/${session.session_id}/end`,
                    {
                        method: "POST"
                    }
                );


            const data =
                await response.json();


            console.log(
                "SESSION END:",
                data
            );


            setReviewSessionId(
                session.session_id
            );


            setShowSessionSummary(
                true
            );

        }

        catch (error) {

            console.error(
                "Finish Practice Error:",
                error
            );

            alert(
                "Unable to finish practice."
            );

        }

    }


    // ==========================================
    // SESSION SUMMARY
    // ==========================================

    if (showSessionSummary) {

        return (

            <div
                style={{
                    minHeight: "100vh",
                    background: "#F5F7FB",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    padding: "20px 32px"
                }}
            >

                <div
                    style={{
                        width: "100%",
                        maxWidth: "650px",
                        background: "#ffffff",
                        borderRadius: "20px",
                        padding: "35px",
                        textAlign: "center",
                        boxShadow:
                            "0 10px 35px rgba(15,23,42,0.10)"
                    }}
                >

                    <h1>
                        🎉 Session Completed
                    </h1>


                    <p
                        style={{
                            color: "#6b7280",
                            marginTop: "8px"
                        }}
                    >
                        Great job completing your practice session.
                    </p>


                    <h3
                        style={{
                            marginTop: "30px",
                            color: "#6b7280"
                        }}
                    >
                        Overall Score
                    </h3>


                    <div
                        style={{
                            fontSize: "48px",
                            fontWeight: "800",
                            color: "#4F46E5",
                            margin: "10px 0 25px"
                        }}
                    >
                        {session?.accuracy ?? 0}%
                    </div>


                    <div
                        style={{
                            display: "grid",
                            gridTemplateColumns:
                                "1fr 1fr",
                            gap: "15px",
                            marginBottom: "25px"
                        }}
                    >

                        <div
                            style={{
                                background: "#F8FAFC",
                                borderRadius: "14px",
                                padding: "18px"
                            }}
                        >

                            <strong>
                                Attempts
                            </strong>

                            <div
                                style={{
                                    fontSize: "24px",
                                    fontWeight: "700",
                                    marginTop: "5px"
                                }}
                            >
                                {session?.attempts ?? 0}
                            </div>

                        </div>


                        <div
                            style={{
                                background: "#F8FAFC",
                                borderRadius: "14px",
                                padding: "18px"
                            }}
                        >

                            <strong>
                                Completed
                            </strong>

                            <div
                                style={{
                                    fontSize: "24px",
                                    fontWeight: "700",
                                    marginTop: "5px"
                                }}
                            >
                                {completedLetters.length}/26
                            </div>

                        </div>

                    </div>


                    {nextPractice && (

                        <div
                            style={{
                                background: "#EEF2FF",
                                borderRadius: "14px",
                                padding: "18px",
                                marginBottom: "25px"
                            }}
                        >

                            <strong>
                                🎯 Next Recommended Practice
                            </strong>

                            <div
                                style={{
                                    fontSize: "28px",
                                    fontWeight: "800",
                                    color: "#4F46E5",
                                    marginTop: "8px"
                                }}
                            >
                                {nextPractice.alphabet}
                            </div>

                            <p
                                style={{
                                    margin: "6px 0 0",
                                    color: "#6b7280"
                                }}
                            >
                                {nextPractice.reason}
                            </p>

                        </div>

                    )}


                    <div
                        style={{
                            display: "flex",
                            gap: "12px",
                            justifyContent: "center",
                            flexWrap: "wrap"
                        }}
                    >

                        <button
                            className="start-btn"
                            onClick={() => {

                                setShowSessionSummary(
                                    false
                                );

                                setShowReview(
                                    true
                                );

                            }}
                        >
                            📊 Review Session
                        </button>


                        <button
                            className="secondary-btn"
                            onClick={async () => {

                                setShowSessionSummary(
                                    false
                                );

                                setSession(null);

                                setLesson(null);

                                setPrediction(null);

                                setAssessment(null);


                                if (
                                    nextPractice?.alphabet
                                ) {

                                    await selectLetter(
                                        nextPractice.alphabet
                                    );

                                    setSelectedLetter(
                                        nextPractice.alphabet
                                    );


                                    setTimeout(() => {

                                        startPractice();

                                    }, 300);

                                }

                            }}
                        >
                            ▶ Continue Learning
                        </button>

                    </div>

                </div>

            </div>

        );

    }


    // ==========================================
    // REVIEW PAGE
    // ==========================================

    if (showReview) {

        return (

            <div
                style={{
                    minHeight: "100vh",
                    background: "#F5F7FB",
                    padding: "30px"
                }}
            >

                <PracticeReview
                    sessionId={reviewSessionId}
                />


                <div
                    style={{
                        marginTop: "20px",
                        textAlign: "center"
                    }}
                >

                    <button
                        className="start-btn"
                        onClick={() => {

                            setShowReview(false);

                            setSession(null);

                            setLesson(null);

                            setPrediction(null);

                            setAssessment(null);

                        }}
                    >
                        🔄 Back To Lessons
                    </button>

                </div>

            </div>

        );

    }


    // ==========================================
    // MAIN LESSONS PAGE
    // ==========================================

    return (

        <div
            style={{
                minHeight: "100vh",
                background: "#F5F7FB",
                padding: "30px"
            }}
        >

            {/* HEADER */}

            <div
                style={{
                    maxWidth: "1500px",
                    width: "100%",
                    margin: "0 auto"
                }}
            >

                <h1
                    style={{
                        margin: 0,
                        fontSize: "30px",
                        color: "#111827"
                    }}
                >
                    Sign Language Lessons
                </h1>


                <p
                    style={{
                        marginTop: "6px",
                        color: "#6B7280"
                    }}
                >
                    Choose a letter and practice your sign.
                </p>

            </div>


            {/* ALPHABET SELECTOR */}

            <div
                style={{
                    maxWidth: "1450px",
                    margin: "0 auto 28px",
                    background: "#ffffff",
                    borderRadius: "20px",
                    padding: "30px",
                    boxShadow:
                        "0 8px 30px rgba(15,23,42,0.08)"
                }}
            >

                <div
                    style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        marginBottom: "22px",
                        flexWrap: "wrap",
                        gap: "20px"
                    }}
                >

                    <div>

                        <h2
                            style={{
                                margin: 0,
                                fontSize: "24px",
                                color: "#111827"
                            }}
                        >
                            Choose Alphabet
                        </h2>


                        <p
                            style={{
                                marginTop: "6px",
                                color: "#6B7280"
                            }}
                        >
                            Select a sign and begin practicing.
                        </p>

                    </div>


                    <button
                        className="start-btn"
                        onClick={
                            !session
                                ? startPractice
                                : undefined
                        }
                        disabled={
                            loading || session
                        }
                    >

                        {loading ? (

                            <>
                                ⏳ Starting...
                            </>

                        ) : session ? (

                            <>
                                🟢 Practice Running
                            </>

                        ) : (

                            <>
                                <FaPlay />
                                Start Practice
                            </>

                        )}

                    </button>

                </div>


                {/* =====================================
                    ALPHABET GRID
                ===================================== */}

                <div
                    style={{
                        display: "grid",
                        gridTemplateColumns:
                            "repeat(13, 1fr)",
                        gap: "12px"
                    }}
                >

                    {alphabets.map(letter => {

                        const isSelected =
                            selectedLetter === letter;


                        const isCompleted =
                            completedLetters.includes(
                                letter
                            );


                        return (

                            <button
                                key={letter}
                                onClick={() =>
                                    selectLetter(
                                        letter
                                    )
                                }
                                style={{

                                    height: "58px",

                                    borderRadius: "14px",

                                    border:
                                        isSelected
                                            ? "2px solid #4F46E5"
                                            : isCompleted
                                            ? "2px solid #22C55E"
                                            : "1px solid #E5E7EB",

                                    background:
                                        isSelected
                                            ? "#4F46E5"
                                            : isCompleted
                                            ? "#DCFCE7"
                                            : "#ffffff",

                                    color:
                                        isSelected
                                            ? "#ffffff"
                                            : isCompleted
                                            ? "#15803D"
                                            : "#374151",

                                    fontSize: "18px",

                                    fontWeight: "700",

                                    cursor: "pointer",

                                    transition:
                                        "0.2s"

                                }}
                            >

                                <div
                                    style={{
                                        display: "flex",
                                        justifyContent:
                                            "center",
                                        alignItems:
                                            "center",
                                        gap: "6px"
                                    }}
                                >

                                    <span>
                                        {letter}
                                    </span>


                                    {isCompleted &&
                                        !isSelected && (

                                            <FaCheckCircle
                                                color="#16A34A"
                                                size={14}
                                            />

                                        )}

                                </div>

                            </button>

                        );

                    })}

                </div>


                {/* =====================================
                    LEARNING PROGRESS
                ===================================== */}

                <div
                    style={{
                        marginTop: "22px"
                    }}
                >

                    <div
                        style={{
                            display: "flex",
                            justifyContent:
                                "space-between",
                            marginBottom: "8px",
                            fontWeight: "600",
                            color: "#374151"
                        }}
                    >

                        <span>
                            Learning Progress
                        </span>


                        <span>
                            {completedLetters.length} / 26
                        </span>

                    </div>


                    <div
                        style={{
                            width: "100%",
                            height: "12px",
                            background: "#E5E7EB",
                            borderRadius: "999px",
                            overflow: "hidden"
                        }}
                    >

                        <div
                            style={{
                                width:
                                    `${(
                                        completedLetters.length
                                        / 26
                                    ) * 100}%`,

                                height: "100%",

                                background: "#22C55E",

                                transition:
                                    "0.4s ease"
                            }}
                        />

                    </div>


                    <div
                        style={{
                            marginTop: "10px",
                            color: "#6B7280",
                            fontSize: "14px"
                        }}
                    >

                        Current Letter:

                        <strong
                            style={{
                                color: "#4F46E5",
                                marginLeft: "6px"
                            }}
                        >
                            {selectedLetter}
                        </strong>

                    </div>

                </div>

            </div>


            {/* =====================================
                MASTERED POPUP
            ===================================== */}

            {masteredPopup && (

                <div
                    style={{
                        position: "fixed",
                        top: "30px",
                        right: "30px",
                        background: "#22C55E",
                        color: "white",
                        padding: "18px 28px",
                        borderRadius: "18px",
                        boxShadow:
                            "0 12px 35px rgba(0,0,0,0.18)",
                        zIndex: 9999,
                        animation:
                            "fadeIn 0.3s"
                    }}
                >

                    <div
                        style={{
                            fontSize: "22px",
                            fontWeight: "700"
                        }}
                    >
                        🎉 Letter {masteredPopup.letter} Mastered!
                    </div>


                    {masteredPopup.next && (

                        <div
                            style={{
                                marginTop: "6px",
                                opacity: 0.9
                            }}
                        >
                            Moving to{" "}
                            {masteredPopup.next}...
                        </div>

                    )}

                </div>

            )}


            {/* =====================================
                PRACTICE AREA
            ===================================== */}

            {session && (

                <div
                    style={{
                        maxWidth: "1500px",
                        width: "100%",
                        margin: "0 auto"
                    }}
                >

                    <PracticeLayout
                        session={session}
                        lesson={lesson}
                        prediction={prediction}
                        completedLetters={
                            completedLetters
                        }
                        onResult={
                            handlePrediction
                        }
                        finishPractice={
                            finishPractice
                        }
                    />

                </div>

            )}

        </div>

    );

}