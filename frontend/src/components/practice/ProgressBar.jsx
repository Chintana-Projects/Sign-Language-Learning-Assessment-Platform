export default function ProgressBar({ completedLetters }) {
    const progress = (completedLetters.length / 26) * 100;

    return (
        <div className="session-progress">
            <div className="progress-track">
                <div
                    className="progress-fill"
                    style={{
                        width: `${progress}%`
                    }}
                />
            </div>

            <p>
                {completedLetters.length} / 26 Alphabets Mastered
            </p>
        </div>
    );
}