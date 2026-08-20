export default function SessionControls({
    finishPractice
}) {

    return (

        <div className="session-controls">

            <button
                className="end-session-btn"
                onClick={finishPractice}
            >
                🚪 End Session
            </button>

        </div>

    );

}