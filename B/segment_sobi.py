from PIL import Image
import pytesseract
from collections import defaultdict

# Load the newspaper image
image_path = 'paper.jpg'
newspaper_image = Image.open(image_path)

# Convert the image to grayscale to improve OCR accuracy
grayscale_image = newspaper_image.convert('L')

# Use pytesseract to get bounding boxes of detected text areas
data = pytesseract.image_to_data(grayscale_image, output_type=pytesseract.Output.DICT)

# Extract individual bounding boxes
bounding_boxes = []
n_boxes = len(data['level'])
for i in range(n_boxes):
    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
    if w > 50 and h > 20:  # Filter out very small boxes
        bounding_boxes.append((x, y, w, h))

# Sort bounding boxes by vertical and horizontal position
sorted_boxes = sorted(bounding_boxes, key=lambda b: (b[1], b[0]))

# Adjust the grouping logic to better combine headings and content into full articles

def group_boxes_into_full_articles(boxes):
    """
    Improved logic to group bounding boxes into full articles, ensuring the heading and content 
    are combined properly.
    """
    grouped_boxes = defaultdict(list)
    current_group = 0
    threshold_y = 100  # Increased vertical proximity threshold to better group headings and content

    for i, box in enumerate(boxes):
        x, y, w, h = box

        if i == 0:
            grouped_boxes[current_group].append(box)
        else:
            prev_x, prev_y, prev_w, prev_h = boxes[i - 1]

            # Check if the current box is close to the previous box vertically or overlaps horizontally
            if abs(prev_y + prev_h - y) < threshold_y or abs(prev_x - x) < prev_w // 2:
                grouped_boxes[current_group].append(box)
            else:
                current_group += 1
                grouped_boxes[current_group].append(box)

    return grouped_boxes

# Group bounding boxes into full articles
grouped_full_articles = group_boxes_into_full_articles(sorted_boxes)

# Save each grouped article as a single image
output_full_articles = []
for group_id, article_boxes in grouped_full_articles.items():
    # Get the bounding box for the entire article
    min_x = min(box[0] for box in article_boxes)
    min_y = min(box[1] for box in article_boxes)
    max_x = max(box[0] + box[2] for box in article_boxes)
    max_y = max(box[1] + box[3] for box in article_boxes)

    # Crop and save the article
    article_image = newspaper_image.crop((min_x, min_y, max_x, max_y))
    output_path = f'full_article_{group_id + 1}.png'
    article_image.save(output_path)
    output_full_articles.append(output_path)



print("Articles saved:", output_articles)