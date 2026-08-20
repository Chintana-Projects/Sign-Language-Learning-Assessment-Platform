# SignSync Error Analysis

## Model

Random Forest with 100 trees.

## Dataset

`generated/landmarks.csv`

## Test Accuracy

0.9983

## Top 5 Most Confused Gestures

| Rank | Actual | Predicted | Errors |
|---:|---|---|---:|
| 1 | C | B | 3 |
| 2 | B | C | 1 |
| 3 | C | A | 1 |

## Possible Causes

The most common sources of gesture confusion may include:

- Similar finger positions between gestures.
- Occlusion of fingers or parts of the hand.
- Poor-quality or inconsistent training images.
- Incorrect or ambiguous dataset labels.
- Similar landmark configurations between different signs.
- Variations in hand orientation or camera position.
- Background and lighting conditions affecting landmark detection.

## Recommendations

The confused gesture pairs should be investigated individually. Additional training samples can be collected for visually similar gestures, particularly samples covering different hand orientations, distances, lighting conditions, and backgrounds.
