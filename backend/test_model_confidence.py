from app.ai.engine.ai_engine import AIEngine
import cv2


engine = AIEngine()


image = cv2.imread(
    "C:\\Users\\DEll\\.vscode\\SignSync\\datasets\\asl_alphabet_train\\A\\3.jpg"
)


result = engine.predict_image(image)


print("Prediction:")
print(result.prediction)

print()

print("Confidence:")
print(result.confidence)

print()

print("Model Version:")
print(result.model_version)