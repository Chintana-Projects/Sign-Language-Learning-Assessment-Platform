import "../../styles/dashboard/AlphabetMastery.css";

export default function AlphabetMasteryTable({
    alphabetMastery = {}
}) {
    const letters = Array.from(
        { length: 26 },
        (_, index) => String.fromCharCode(65 + index)
    );
    console.log("Alphabet Mastery Data:", alphabetMastery);

    return (
        <div className="mastery-card">

            {/* Header */}
            <div className="mastery-header">
                <div>
                    <h2>Alphabet Mastery</h2>
                    <p>
                        Track your progress across all 26 letters
                    </p>
                </div>

                <div className="mastery-summary">
                    {
    Object.values(alphabetMastery).filter(
        (data) => Number(data?.attempts ?? 0) > 0
    ).length
}/26
<span> practiced</span>
                </div>
            </div>

            {/* Alphabet Grid */}
            <div className="mastery-grid">
{letters.map((letter) => {
    const data = alphabetMastery?.[letter];

    const practiced =
        !!data &&
        Number(data?.attempts ?? 0) > 0;

    const accuracy = practiced
        ? Math.min(
              Math.max(
                  Number(data?.accuracy ?? 0),
                  0
              ),
              100
          )
        : 0;

    let statusClass = "not-practiced";

    if (practiced) {
        if (accuracy >= 80) {
            statusClass = "mastered";
        } else if (accuracy >= 50) {
            statusClass = "learning";
        } else {
            statusClass = "needs-practice";
        }
    }

    return (
        <div
            key={letter}
            className={`mastery-item ${statusClass}`}
        >
            <div className="mastery-letter">
                {letter}
            </div>

            <div className="mastery-accuracy">
                {practiced
                    ? `${accuracy}%`
                    : "—"}
            </div>

            <div className="mastery-progress">
                <div
                    className="mastery-progress-fill"
                    style={{
                        width: `${accuracy}%`
                    }}
                />
            </div>

            <div className="mastery-status">
                {!practiced
                    ? "Not practiced"
                    : accuracy >= 80
                    ? "Mastered"
                    : accuracy >= 50
                    ? "Learning"
                    : "Practice"}
            </div>
        </div>
    );
})}

            </div>

            {/* Legend */}
            <div className="mastery-legend">

                <div>
                    <span className="legend-dot mastered-dot" />
                    Mastered
                </div>

                <div>
                    <span className="legend-dot learning-dot" />
                    Learning
                </div>

                <div>
                    <span className="legend-dot practice-dot" />
                    Needs Practice
                </div>

                <div>
                    <span className="legend-dot empty-dot" />
                    Not Practiced
                </div>

            </div>

        </div>
    );
}