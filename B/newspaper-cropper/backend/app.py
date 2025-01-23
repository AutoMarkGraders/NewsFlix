from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from PyPDF2 import PdfReader
from PIL import Image
import fitz  # PyMuPDF for rendering PDF pages

app = Flask(__name__, static_folder='output')  # Set the output folder as static folder
CORS(app)

# Set up upload and output directories
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route for uploading PDF
@app.route('/upload', methods=['POST'])  # to upload pdf
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(pdf_path)

    return jsonify({"message": "PDF uploaded successfully!", "pdf_path": pdf_path}), 200

# Route to get the pages as images
@app.route('/get-pages', methods=['GET'])
def get_pages():
    pdf_path = request.args.get('pdf_path')
    if not pdf_path or not os.path.exists(pdf_path):
        return jsonify({"error": "PDF not found"}), 404

    # Extract pages as images
    output_images = []
    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        image_path = os.path.join(OUTPUT_FOLDER, f"page_{page_num + 1}.png")
        pix.save(image_path)
        # Serve images from the static folder with forward slashes
        output_images.append(f"/static/{os.path.basename(image_path)}")  # Return URL path for image

    return jsonify({"pages": output_images}), 200

# Route to crop a section of the page
@app.route('/crop', methods=['POST'])
def crop_image():
    data = request.json
    image_path = data.get('image_path')
    x = data.get('x')
    y = data.get('y')
    width = data.get('width')
    height = data.get('height')

    # Normalize the path in case it's relative
    image_path = os.path.join(OUTPUT_FOLDER, image_path.lstrip('/'))

    if not os.path.exists(image_path):
        return jsonify({"error": "Image not found"}), 404

    try:
        # Open image and crop
        with Image.open(image_path) as img:
            cropped_image = img.crop((x, y, x + width, y + height))
            cropped_path = os.path.join(OUTPUT_FOLDER, f"cropped_{os.path.basename(image_path)}")
            cropped_image.save(cropped_path)

        return jsonify({"cropped_image_path": f"/static/{os.path.basename(cropped_path)}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to download cropped image
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

# Route to get all generated image URLs
@app.route('/get-images', methods=['GET'])
def get_images():
    image_files = os.listdir(OUTPUT_FOLDER)
    image_files = [f for f in image_files if f.endswith('.png')]  # Filter only .png files
    image_urls = [f"/static/{f}" for f in image_files]  # Return URLs for each image
    return jsonify(image_urls)

# Serve images from the output folder
@app.route('/static/<filename>')
def serve_output_image(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
