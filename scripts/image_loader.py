import cv2
from pathlib import Path

# ==========================================================
# SignSync Image Loader
# ==========================================================

# Ask user for image path
image_path = input("Enter image path: ").strip()

image = cv2.imread(image_path)

# ----------------------------------------------------------
# Check if image loaded successfully
# ----------------------------------------------------------

if image is None:
    print("\nError: Unable to load image.")
    exit()

# ----------------------------------------------------------
# Image Properties
# ----------------------------------------------------------

height = image.shape[0]
width = image.shape[1]
channels = image.shape[2]
image_size = image.size

# ----------------------------------------------------------
# Display Information
# ----------------------------------------------------------

print("\n========== Image Information ==========")
print(f"Height   : {height}")
print(f"Width    : {width}")
print(f"Channels : {channels}")
print(f"Image Size : {image_size}")

# ----------------------------------------------------------
# Display Image
# ----------------------------------------------------------

cv2.imshow("SignSync Image Loader", image)

print("\nPress any key to close the image window.")

cv2.waitKey(0)
cv2.destroyAllWindows()