import os
import torch
from transformers import AutoImageProcessor, SegformerForSemanticSegmentation
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Set the environment variable to bypass OpenMP error (only as a temporary solution)
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Load the model and processor (Make sure the model name is correct)
processor = AutoImageProcessor.from_pretrained("Caraaaaa/image_segmentation_text")
model = SegformerForSemanticSegmentation.from_pretrained("Caraaaaa/image_segmentation_text")

def segment_image(image_path):
    # Load the image
    image = Image.open(image_path).convert("RGB")

    # Preprocess the image
    inputs = processor(images=image, return_tensors="pt")

    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the predicted segmentation map
    logits = outputs.logits
    upsampled_logits = torch.nn.functional.interpolate(
        logits,
        size=image.size[::-1],  # Upsample to match original image size
        mode="bilinear",
        align_corners=False
    )
    segmentation_map = upsampled_logits.argmax(dim=1).squeeze().cpu().numpy()

    # Visualize the segmentation map
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(image)
    plt.axis("off")
    plt.title("Original Image")
    
    plt.subplot(1, 2, 2)
    plt.imshow(segmentation_map, cmap="jet", alpha=0.8)
    plt.axis("off")
    plt.title("Segmentation Map")
    plt.show()

# Example usage
image_path = "akash_hindu-Optimized.jpg"  # Replace with your image file path
segment_image(image_path)
