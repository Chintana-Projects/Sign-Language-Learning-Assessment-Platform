import cv2

# ==========================================================
# SignSync Camera Test
# ==========================================================

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Unable to access the webcam.")
    exit()

print("=" * 50)
print("         SignSync Camera Test")
print("=" * 50)
print("Press 'Q' to exit.")

while True:

    success, frame = camera.read()

    if not success:
        print("Error: Failed to capture frame.")
        break

    cv2.imshow("SignSync Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()