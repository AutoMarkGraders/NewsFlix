import pytesseract
from PIL import Image, ImageDraw
import pytesseract

# Path to your tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Adjust as needed

def highlight_text_in_image(image_path, output_image_path):
    # Open the image using Pillow
    img = Image.open(image_path)

    # Use pytesseract to get bounding boxes of the text
    # 'output_type=pytesseract.Output.DICT' returns text and bounding box info
    data = pytesseract.image_to_boxes(img, output_type=pytesseract.Output.DICT)

    # Draw on the image
    draw = ImageDraw.Draw(img)
    for i in range(len(data['char'])):
        # Extract the coordinates for each character
        x1, y1, x2, y2 = data['left'][i], data['top'][i], data['right'][i], data['bottom'][i]
        
        # Draw a rectangle around each character
        draw.rectangle([x1, img.height - y2, x2, img.height - y1], outline="red", width=2)
    
    # Save the image with highlighted text
    img.save(output_image_path)
    img.show()

# Example usage
highlight_text_in_image('grees.jpg', 'highlighted_output_image.png')
