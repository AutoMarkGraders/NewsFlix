import cv2
import numpy as np
import easyocr

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Load the newspaper image
image_path = 'newspaper.jpg'  # Replace with your actual image path
image = cv2.imread(image_path)

# Step 1: Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Step 2: Apply GaussianBlur to remove noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Step 3: Apply adaptive threshold to binarize the image (black text on white background)
thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY_INV, 11, 2)

# Step 4: Dilate the image to merge text areas into blocks
kernel = np.ones((5, 5), np.uint8)
dilated = cv2.dilate(thresh, kernel, iterations=3)

# Step 5: Find contours of potential articles/headlines
contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Step 6: Process each detected contour
headline_count = 1
for contour in contours:
    # Get the bounding box for each detected area
    x, y, w, h = cv2.boundingRect(contour)

    # Filter out small boxes (likely noise or irrelevant regions)
    if w > 100 and h > 100:  # You can adjust these values
        # Crop the article area
        article_segment = image[y:y+h, x:x+w]

        # Crop the headline area (assuming it's at the top of the segment)
        headline_area = article_segment[:int(h * 0.2), :]  # Adjust as needed

        # Use EasyOCR to extract text from the headline area
        result = reader.readtext(headline_area)

        # If EasyOCR detects text, assume it's a headline and save both the headline and article
        if result:
            # Save the headline image
            cv2.imwrite(f'headline_{headline_count}.png', headline_area)

            # Save the entire article as well
            cv2.imwrite(f'article_{headline_count}.png', article_segment)

            # Optionally, draw the bounding box around the headline and display it for visualization
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Print the detected headline text for reference
            print(f'Headline {headline_count}:')
            for (bbox, text, prob) in result:
                print(f' - {text} (confidence: {prob:.2f})')

            headline_count += 1

# Step 7: Display the final image with all detected headlines boxed
cv2.imshow("Detected Headlines", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
