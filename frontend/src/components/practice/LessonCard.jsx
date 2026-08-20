import "./../../styles/dashboard/LessonCard.css";

export default function LessonCard({ lesson }) {

    if (!lesson) return null;

    return (

        <div className="lesson-card">

            <div className="lesson-title">

                <h2>Reference Sign</h2>

                <span className="lesson-badge">
                    LEARN
                </span>

            </div>

            <div className="lesson-content">

                <div className="lesson-image-wrapper">

                    <img
    src={`/assets/asl/${lesson.sign}.jpg`}
    alt={lesson.sign}
    className="lesson-image"
/>

                </div>

                <div className="lesson-tips">

                    <h3>Quick Tips</h3>

                    <ul>
                        <li>✓ Keep your hand centered</li>
                        <li>✓ Hold the gesture steady</li>
                        <li>✓ Make sure all fingers are visible</li>
                    </ul>

                </div>

            </div>

        </div>

    );
}