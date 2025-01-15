import cv2
import numpy as np

# Load the image of the newspaper
image_path = 'image.png'  # Replace with your actual image file
image = cv2.imread(image_path)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Use adaptive thresholding to handle varying lighting conditions
thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                               cv2.THRESH_BINARY_INV, 11, 2)

# Find contours in the thresholded image
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Loop through each contour and extract each segmented area (news segment)
for i, contour in enumerate(contours):
    # Get bounding box for the contour
    x, y, w, h = cv2.boundingRect(contour)
    
    # Filter out small contours that might be noise
    if w > 100 and h > 100:  # Adjust size threshold based on image resolution
        # Crop the image to the bounding box
        segment = image[y:y+h, x:x+w]

        # Optionally save the segmented image
        cv2.imwrite(f'segment_{i+1}.png', segment)
        
        # Draw green bounding boxes on the original image (for visualization)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Show the final image with the detected segments outlined in green boxes
cv2.imshow("Segmented Newspaper with Green Boxes", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
