import cv2
import numpy as np
import os

def segment_paragraphs(image_path, output_folder):
    # Load the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Preprocessing: Apply binary threshold
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Dilation to connect text regions
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    dilated = cv2.dilate(binary, kernel, iterations=1)
    
    # Find contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Extract each paragraph as a separate image
    paragraph_count = 0
    for contour in contours:
        # Get bounding box
        x, y, w, h = cv2.boundingRect(contour)
        
        # Filter small regions (noise)
        if w > 100 and h > 100:  # Adjust threshold as needed
            paragraph = image[y:y+h, x:x+w]
            paragraph_count += 1
            
            # Save the paragraph image
            output_path = os.path.join(output_folder, f"paragraph_{paragraph_count}.png")
            cv2.imwrite(output_path, paragraph)
            print(f"Saved: {output_path}")
    
    print(f"Total paragraphs segmented: {paragraph_count}")

# Example usage
image_path = "test1.png"  # Replace with your image path
output_folder = "output_paragraphs"  # Replace with your desired output folder
segment_paragraphs(image_path, output_folder)
