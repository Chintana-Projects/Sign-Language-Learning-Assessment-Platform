import "./../../styles/dashboard/LivePredictionCard.css";

export default function LivePredictionCard({ prediction }) {

    const stablePrediction = prediction?.stable_prediction || {};

    const confidence =
        stablePrediction.confidence ??
        prediction?.confidence ??
        0;

    const stability =
        stablePrediction.gesture_stability ??
        0;

    const stableFrames =
        stablePrediction.stable_frames ??
        0;

    const requiredFrames =
        stablePrediction.required_frames ??
        5;

    return (

        <div className="live-status-card">

            <div className="recognition-header">

                <div>

                    <h2>AI Recognition</h2>

                    <p>Real-time sign analysis</p>

                </div>

                <div
                    className={
                        stablePrediction.stable
                            ? "recognition-status stable"
                            : "recognition-status waiting"
                    }
                >
                    {stablePrediction.stable
                        ? "LIVE"
                        : "WAITING"}
                </div>

            </div>

            <div className="prediction-display">

                <span className="prediction-label">
                    Current Prediction
                </span>

                <h1>
                    {prediction?.prediction || "--"}
                </h1>

            </div>

            <div className="recognition-metrics">

                <div className="recognition-metric">

                    <div className="metric-header">

                        <span>Confidence</span>

                        <strong>
                            {confidence.toFixed(1)}%
                        </strong>

                    </div>

                    <div className="metric-progress">

                        <div
                            className="metric-progress-fill confidence-fill"
                            style={{
                                width: `${confidence}%`
                            }}
                        />

                    </div>

                </div>

                <div className="recognition-metric">

                    <div className="metric-header">

                        <span>Gesture Stability</span>

                        <strong>
                            {stability.toFixed(0)}%
                        </strong>

                    </div>

                    <div className="metric-progress">

                        <div
                            className="metric-progress-fill stability-fill"
                            style={{
                                width: `${stability}%`
                            }}
                        />

                    </div>

                </div>

            </div>

            <div className="stable-frame-section">

                <div className="stable-frame-header">

                    <span>Stable Frames</span>

                    <strong>
                        {stableFrames} / {requiredFrames}
                    </strong>

                </div>

                <div className="frame-dots">

                    {Array.from({
                        length: requiredFrames
                    }).map((_, i) => (

                        <div
                            key={i}
                            className={
                                i < stableFrames
                                    ? "frame-dot active"
                                    : "frame-dot"
                            }
                        />

                    ))}

                </div>

            </div>

        </div>

    );

}