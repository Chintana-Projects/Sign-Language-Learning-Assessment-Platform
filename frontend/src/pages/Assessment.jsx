import { useEffect, useRef, useState } from "react";
import "./Assessment.css";

export default function Assessment() {

    const videoRef = useRef(null);
    const streamRef = useRef(null);

    const [currentLetter, setCurrentLetter] = useState("A");
    const [attempting, setAttempting] = useState(false);
    const [submitted, setSubmitted] = useState(false);
    const [cameraError, setCameraError] = useState("");

    /* =====================================================
       START CAMERA
    ===================================================== */

    const startCamera = async () => {

        setCameraError("");

        try {

            const stream =
                await navigator.mediaDevices.getUserMedia({
                    video: true,
                    audio: false,
                });

            streamRef.current = stream;

            if (videoRef.current) {
                videoRef.current.srcObject = stream;
            }

            setAttempting(true);
            setSubmitted(false);

        } catch (error) {

            console.error("Camera error:", error);

            setCameraError(
                "Unable to access the camera. Please allow camera permission and try again."
            );

        }
    };


    /* =====================================================
       STOP CAMERA
    ===================================================== */

    const stopCamera = () => {

        if (streamRef.current) {

            streamRef.current
                .getTracks()
                .forEach((track) => track.stop());

            streamRef.current = null;
        }

    };


    /* =====================================================
       SUBMIT ATTEMPT
    ===================================================== */

    const handleSubmit = () => {

        stopCamera();

        setAttempting(false);
        setSubmitted(true);

        /*
            Prediction and database recording
            will be added in the next step.
        */

    };


    /* =====================================================
       CLEANUP CAMERA
    ===================================================== */

    useEffect(() => {

        return () => {
            stopCamera();
        };

    }, []);


    return (

        <div className="assessment-page">

            {/* =========================================
               HEADER
            ========================================= */}

            <div className="assessment-header">

                <div>

                    <h1>
                        Alphabet Assessment
                    </h1>

                    <p>
                        Test your sign language skills
                        across all 26 letters.
                    </p>

                </div>


                <div className="assessment-progress">

                    Letter 1 of 26

                </div>

            </div>


            {/* =========================================
               MAIN ASSESSMENT CARD
            ========================================= */}

            <div className="assessment-card">


                {/* =====================================
                   EXPECTED LETTER
                ===================================== */}

                <div className="assessment-letter-section">

                    <span className="assessment-label">
                        EXPECTED LETTER
                    </span>


                    <div className="assessment-letter">

                        {currentLetter}

                    </div>


                    {!attempting && !submitted && (

                        <button
                            className="attempt-btn"
                            onClick={startCamera}
                        >
                            🎥 Attempt Letter
                        </button>

                    )}

                </div>


                {/* =====================================
                   CAMERA
                ===================================== */}

                {attempting && (

                    <div className="assessment-camera-section">

                        <div className="camera-placeholder">

                            <div className="camera-icon">
                                📷
                            </div>


                            <h2>
                                Perform the Sign
                            </h2>


                            <p>
                                Show the expected letter
                                to the camera.
                            </p>


                            {/* REAL CAMERA */}

                            <div className="camera-preview">

                                <video
                                    ref={videoRef}
                                    autoPlay
                                    playsInline
                                    muted
                                />

                            </div>


                        </div>


                        <button
                            className="submit-btn"
                            onClick={handleSubmit}
                        >
                            Submit Attempt
                        </button>

                    </div>

                )}


                {/* =====================================
                   CAMERA ERROR
                ===================================== */}

                {cameraError && (

                    <div className="camera-error">

                        {cameraError}

                    </div>

                )}


                {/* =====================================
                   ATTEMPT RECORDED
                ===================================== */}

                {submitted && (

                    <div className="attempt-recorded">

                        <div className="success-icon">
                            ✓
                        </div>


                        <h2>
                            Attempt Recorded
                        </h2>


                        <p>
                            Your attempt has been recorded.
                        </p>

                    </div>

                )}

            </div>


            {/* =========================================
               INFORMATION CARDS
            ========================================= */}

            <div className="assessment-info">


                <div className="info-card">

                    <span>
                        📝
                    </span>

                    <div>

                        <h3>
                            26 Letters
                        </h3>

                        <p>
                            Complete the full alphabet
                            assessment.
                        </p>

                    </div>

                </div>


                <div className="info-card">

                    <span>
                        🎯
                    </span>

                    <div>

                        <h3>
                            Final Score
                        </h3>

                        <p>
                            Your result will be shown
                            after the test.
                        </p>

                    </div>

                </div>


                <div className="info-card">

                    <span>
                        🏆
                    </span>

                    <div>

                        <h3>
                            Certificate
                        </h3>

                        <p>
                            Pass the assessment to
                            unlock your certificate.
                        </p>

                    </div>

                </div>


            </div>

        </div>

    );
}