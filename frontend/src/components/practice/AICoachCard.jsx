export default function AICoachCard({

    lesson,
    prediction

}) {

    return (

        <div className="card ai-coach-card">

            <h2>🤖 AI Coach</h2>

            <div className="coach-letter">

                {lesson?.sign}

            </div>

            <div className="coach-status">

                {

                    prediction?.validation?.valid

                        ?

                        "✅ Hand Detected"

                        :

                        "❌ Waiting For Hand"

                }

            </div>

            <div className="coach-message">

                {

                    !prediction

                        ?

                        "Show your hand to the camera."

                        :

                        prediction.confidence >= 90

                        ?

                        "Excellent! Hold the gesture."

                        :

                        prediction.confidence >= 70

                        ?

                        "Good! Keep your hand steady."

                        :

                        prediction.confidence >= 40

                        ?

                        "Adjust your fingers."

                        :

                        "Move your hand inside the frame."

                }

            </div>

            <div

                className={

                    prediction?.stable

                        ?

                        "coach-stable"

                        :

                        "coach-wait"

                }

            >

                {

                    prediction?.stable

                        ?

                        "🟢 Stable Gesture"

                        :

                        "🟡 Waiting for Stability"

                }

            </div>

        </div>

    );

}