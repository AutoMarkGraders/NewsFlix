import cv2
import numpy as np

def segment_articles(image_path):
    # Load the image of the newspaper
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Use adaptive thresholding to handle varying lighting conditions
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)

    # Dilate the thresholded image to connect text areas
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)

    # Find contours in the dilated image
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize a counter for saved segments
    segment_count = 1

    # Loop through each contour and extract each segmented area (news article)
    for contour in contours:
        # Get bounding box for the contour
        x, y, w, h = cv2.boundingRect(contour)
        
        # Filter out small contours that might be noise
        if w > 100 and h > 100:  # Adjust size threshold based on your image resolution
            # Crop the image to the bounding box
            article_segment = image[y:y+h, x:x+w]

            # Save the segmented image
            cv2.imwrite(f'article_segment_{segment_count}.png', article_segment)
            print(f'Saved: article_segment_{segment_count}.png')
            segment_count += 1

    print("Segmentation complete!")

# Example usage
if __name__ == "__main__":
    image_path = 'paper2.jpg'  # Replace with your actual image file
    segment_articles(image_path)
