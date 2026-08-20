import LessonCard from "./LessonCard";
import CameraSection from "./CameraSection";
import "../../styles/Layout.css";

export default function PracticeLayout({
    session,
    lesson,
    prediction,
    onResult,
    finishPractice
}){

    return (

        <div className="practice-container">

            {/* ===============================
                HEADER
            ================================ */}

            <div className="practice-header">

                <div className="practice-title">

                    <div className="practice-letter">
                        {lesson?.sign}
                    </div>

                    <div>

                        <h2>
                            Learning Letter {lesson?.sign}
                        </h2>

                        <p>
                            Practice until the AI confidently recognizes your sign.
                        </p>

                    </div>

                </div>

                <div className="practice-actions">

                    <button
                        className="end-session-btn"
                        onClick={finishPractice}
                    >
                        End Session
                    </button>

                </div>

            </div>

            {/* ===============================
                LESSON AREA
            ================================ */}

            <div className="lesson-top-row">

                <aside className="lesson-reference">

                    <LessonCard
                        lesson={lesson}
                    />

                </aside>

                <main className="lesson-camera">

<CameraSection
    key={lesson?.sign}
    session={session}
    prediction={prediction}
    onResult={onResult}
/>
                </main>

            </div>

        </div>

    );

}