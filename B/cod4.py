import cv2
import numpy as np

def segment_paragraphs(image_path):
    # Load the image of the newspaper
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use adaptive thresholding to handle varying lighting conditions
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)

    # Dilate the thresholded image to connect text areas
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)

    # Find contours in the dilated image
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize a counter for saved segments
    article_count = 1

    # Loop through each contour and extract each segmented area (news article)
    for contour in contours:
        # Get bounding box for the contour
        x, y, w, h = cv2.boundingRect(contour)
        
        # Filter out small contours that might be noise
        if w > 100 and h > 100:  # Adjust size threshold based on your image resolution
            # Crop the image to the bounding box
            article_segment = image[y:y+h, x:x+w]

            # Convert the article segment to grayscale
            article_gray = cv2.cvtColor(article_segment, cv2.COLOR_BGR2GRAY)

            # Threshold the article segment
            article_thresh = cv2.adaptiveThreshold(article_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                   cv2.THRESH_BINARY_INV, 11, 2)

            # Further dilate to connect paragraphs
            kernel_paragraph = np.ones((1, 5), np.uint8)  # Wider horizontally for paragraph separation
            dilated_paragraphs = cv2.dilate(article_thresh, kernel_paragraph, iterations=1)

            # Find contours for paragraphs
            paragraph_contours, _ = cv2.findContours(dilated_paragraphs, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            paragraph_count = 1
            for para_contour in paragraph_contours:
                # Get bounding box for the paragraph
                px, py, pw, ph = cv2.boundingRect(para_contour)

                # Filter small noise
                if pw > 50 and ph > 20:  # Adjust thresholds as needed
                    paragraph_segment = article_segment[py:py+ph, px:px+pw]

                    # Save the paragraph segment
                    cv2.imwrite(f'article_{article_count}_paragraph_{paragraph_count}.png', paragraph_segment)
                    print(f'Saved: article_{article_count}_paragraph_{paragraph_count}.png')
                    paragraph_count += 1

            article_count += 1

    print("Paragraph segmentation complete!")

# Example usage
if __name__ == "__main__":
    image_path = 'grees.jpg'  # Replace with your actual image file
    segment_paragraphs(image_path)
