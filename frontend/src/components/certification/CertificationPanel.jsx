import "./CertificationPanel.css";

export default function CertificationPanel({
    handDetected,
    currentLetter,
    progress,
    loading,
    onCapture,
    disabled
}) {

    return (

        <div className="certification-panel">

            <div className="certification-header">

                <h3>
                    Certification Assessment
                </h3>

                <span
                    className={
                        handDetected
                            ? "status detected"
                            : "status waiting"
                    }
                >
                    {handDetected
                        ? "Hand Detected"
                        : "Show Your Hand"}
                </span>

            </div>

            <div className="letter-card">

                <span>
                    Current Letter
                </span>

                <h1>
                    {currentLetter}
                </h1>

            </div>

            <div className="progress-card">

                <span>
                    Progress
                </span>

                <strong>
                    {progress} / 26
                </strong>

            </div>

            <button
                className="capture-btn"
                onClick={onCapture}
                disabled={disabled || loading}
            >
                {loading
                    ? "Capturing..."
                    : "📸 Capture Sign"}
            </button>

        </div>

    );
}