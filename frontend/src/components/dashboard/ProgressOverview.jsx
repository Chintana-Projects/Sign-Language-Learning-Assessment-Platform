import "./../../styles/ProgressOverview.css";

export default function ProgressOverview({
    profile = {},
    learningState = {}
}) {

    const accuracy =
        Number(
            learningState.progress ??
            profile.accuracy ??
            0
        );

    const completedLetters =
        profile.completed_letters?.length || 0;

    const practiceHours =
        Number(
            profile.practice_hours ??
            profile.total_practice_hours ??
            0
        );

    const totalSigns =
        Number(
            profile.total_signs ??
            profile.signs_practiced ??
            0
        );

    return (

        <div className="progress-overview">

            <h2>Progress Overview</h2>

            <div className="progress-cards">

                <div className="progress-box">

                    <h3>
                        {Math.round(accuracy)}%
                    </h3>

                    <p>Accuracy</p>

                </div>


                <div className="progress-box">

                    <h3>
                        {completedLetters}
                    </h3>

                    <p>Lessons</p>

                </div>


                <div className="progress-box">

                    <h3>
                        {practiceHours}h
                    </h3>

                    <p>Practice</p>

                </div>


                <div className="progress-box">

                    <h3>
                        {totalSigns}
                    </h3>

                    <p>Signs</p>

                </div>

            </div>

        </div>

    );

}
