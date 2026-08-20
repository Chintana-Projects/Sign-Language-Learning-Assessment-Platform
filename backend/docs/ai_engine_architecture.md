\# SignSync AI Recognition Engine Architecture



\## Overview



The AI Engine provides a single interface for gesture recognition.



A developer can call:



predict(image)



without knowing internal ML implementation details.





\## Pipeline



Image / Webcam Frame



↓



MediaPipe Hand Detection



↓



21 Hand Landmarks



↓



Landmark Validation



↓



Feature Normalization



↓



63-Dimensional Feature Vector



↓



Random Forest Model



↓



Prediction Probability



↓



Confidence Threshold



↓



PredictionResult Object





\# Components





\## Hand Detection



Purpose:

Detect the presence of a hand in an input image.



Input:

Image frame.



Output:

21 MediaPipe hand landmarks.



Why needed:

Converts raw image data into meaningful hand information.





\## Landmark Validation



Purpose:

Check whether extracted landmarks are valid.



Input:

Landmark coordinates.



Output:

Valid/invalid status.



Why needed:

Prevents incorrect predictions from incomplete data.





\## Feature Normalization



Purpose:

Convert landmarks into the same coordinate format used during training.



Input:

21 landmark coordinates.



Output:

Normalized landmark values.



Why needed:

Ensures training and inference data are consistent.





\## Feature Generation



Purpose:

Convert landmarks into ML model input.



Input:

21 landmarks.



Output:

63 dimensional feature vector.



Why needed:

Machine learning models require numerical feature representation.





\## Model Manager



Purpose:

Load and manage trained ML models.



Input:

Model files.



Output:

Loaded Random Forest classifier.



Why needed:

Allows future model version upgrades.





\## Prediction Engine



Purpose:

Generate gesture prediction.



Input:

63 feature vector.



Output:

Gesture label and probability.





\## Confidence System



Purpose:

Reject uncertain predictions.



Input:

Prediction probability.



Output:

Accepted prediction or Unknown.





\## Prediction Result



Contains:



\- Gesture prediction

\- Confidence score

\- Model version

\- Inference time

\- Status message





\## Backend Integration



FastAPI can directly import:



AIEngine



and call:



predict(frame)



without modifying internal AI components.

