# SignSync Future Live Recognition Pipeline

## Objective

The current SignSync system recognizes one static hand gesture at a time using a Random Forest classifier.

The future version will recognize continuous sign language by analyzing sequences of gestures over multiple frames using temporal deep learning models such as LSTM, GRU, or Transformers.

---

# Overall Pipeline

Webcam Stream
        │
        ▼
Frame Capture
        │
        ▼
MediaPipe Hand Detection
        │
        ▼
Landmark Extraction
        │
        ▼
Temporal Buffer
        │
        ▼
Sequence Generator
        │
        ▼
Sequence Model (Future LSTM / GRU / Transformer)
        │
        ▼
Gesture / Word Prediction
        │
        ▼
Sentence Builder

---

# Component Responsibilities

## 1. Webcam Stream

### Responsibility
Continuously captures video frames from the webcam.

### Input
Real-time webcam feed.

### Output
Individual image frames.

### Why Needed
Provides live input for gesture recognition.

---

## 2. Frame Capture

### Responsibility
Reads one frame at a time from the webcam.

### Input
Webcam stream.

### Output
Single image frame.

### Why Needed
Allows each frame to be processed independently.

---

## 3. MediaPipe Hand Detection

### Responsibility
Detects the presence of hands.

### Input
Image frame.

### Output
21 hand landmarks.

### Why Needed
Extracts the hand from the background.

---

## 4. Landmark Extraction

### Responsibility
Converts MediaPipe landmarks into numerical coordinates.

### Input
MediaPipe landmarks.

### Output
63-dimensional feature vector.

### Why Needed
Machine learning models operate on numerical features rather than images.

---

## 5. Temporal Buffer

### Responsibility
Stores the most recent feature vectors.

### Input
63-dimensional vectors.

### Output
Sliding window of recent frames.

### Why Needed
Captures motion over time.

---

## 6. Sequence Generator

### Responsibility
Converts buffered frames into a sequence suitable for temporal models.

### Input
Buffered landmark vectors.

### Output
Sequence of feature vectors.

### Why Needed
Prepares temporal input for sequence models.

---

## 7. Sequence Model (Future)

### Responsibility
Recognizes dynamic gestures using temporal information.

### Input
Sequence of feature vectors.

### Output
Gesture or word prediction.

### Why Needed
Unlike Random Forest, temporal models understand movement across time.

Possible future models:

- LSTM
- GRU
- Transformer

---

## 8. Sentence Builder

### Responsibility
Combines consecutive gesture predictions into words and sentences.

### Input
Predicted gestures.

### Output
Sentence.

### Why Needed
Provides natural language output instead of isolated letters.

---

# Advantages

• Supports continuous sign language.

• Understands motion rather than single images.

• Reduces prediction flickering.

• Enables sentence-level recognition.

• Easily extendable to LSTM, GRU, or Transformer architectures.

---

# Current Status

✔ Static gesture recognition implemented.

✔ AI Engine completed.

✔ Temporal Buffer implemented.

✔ Sequence Generator placeholder implemented.

✔ Sequence Model placeholder implemented.

✔ Sentence Builder implemented.

Future work:
Replace the placeholder Sequence Model with a trained LSTM, GRU, or Transformer model.