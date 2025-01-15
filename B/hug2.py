import cv2
import numpy as np
from huggingface_hub import from_pretrained_keras
from PIL import Image
import matplotlib.pyplot as plt

# Load the pretrained model for paragraph segmentation
model = from_pretrained_keras("SBB/eynollah-main-regions-aug-scaling")

def segment_paragraphs(image_path):
    # Load the input image
    image = cv2.imread(image_path)
    original_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Convert image to RGB for the model
    pil_image = Image.fromarray(original_image)

    # Use the model to segment regions
    regions = model.predict(pil_image)

    # Convert segmentation map to numpy array for further processing
    segmentation_map = np.array(regions["segmentation"])

    # Threshold the segmentation map to identify unique regions
    unique_regions = np.unique(segmentation_map)
    print(f"Identified regions: {unique_regions}")

    # Create an output image for visualization
    segmented_image = original_image.copy()
    paragraph_count = 1

    # Extract each paragraph and save or visualize it
    for region in unique_regions:
        if region == 0:  # Skip the background region
            continue

        # Create a mask for the current region
        mask = (segmentation_map == region).astype(np.uint8)

        # Find contours for the region
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            # Get bounding box for each paragraph
            x, y, w, h = cv2.boundingRect(contour)
            
            # Skip small noise
            if w > 50 and h > 50:
                # Draw a rectangle on the segmented image
                cv2.rectangle(segmented_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Crop and save the paragraph
                paragraph = original_image[y:y + h, x:x + w]
                cv2.imwrite(f"paragraph_{paragraph_count}.png", paragraph)
                print(f"Saved: paragraph_{paragraph_count}.png")
                paragraph_count += 1

    # Display the original and segmented images
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(original_image)
    plt.axis("off")
    plt.title("Original Image")

    plt.subplot(1, 2, 2)
    plt.imshow(segmented_image)
    plt.axis("off")
    plt.title("Segmented Paragraphs")
    plt.show()

# Example usage
image_path = "grees.jpg"  # Replace with the path to your image
segment_paragraphs(image_path)
