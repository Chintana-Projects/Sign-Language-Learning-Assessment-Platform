# SignSync Inference Benchmark

## Model

`backend/app/ai/ml/models/random_forest.pkl`

## Dataset

`generated/landmarks.csv`

## Benchmark Configuration

- Predictions measured: 100
- Warm-up predictions: 10
- Measurement: single-sample prediction

## Results

| Metric | Result |
|---|---:|
| Average inference time | 143.6038 ms |
| Throughput | 6.96 predictions/sec |
| Peak memory | 0.25 MB |
| Model file size | 452.87 MB |

## Real-Time Suitability

**Suitable for real-time recognition: NO**

The inference time is relatively high and may introduce noticeable latency in real-time recognition.

## Conclusion

The benchmark measures model inference independently of webcam capture and MediaPipe landmark extraction. Therefore, the final end-to-end latency of SignSync will also depend on camera capture, MediaPipe processing, feature preparation, and frontend/backend communication.
