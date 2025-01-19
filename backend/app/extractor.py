import os
from dotenv import load_dotenv
import google.generativeai as genai
import io

# Configure Gemini API
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp", generation_config=generation_config,)


def extract(image):

            # # Save the uploaded image file
        # image_path = "uploaded_image.jpg"
        # with open(image_path, "wb") as buffer:
        #     buffer.write(image.file.read())
        # # Upload the image to Gemini
        # uploaded_file = genai.upload_file(image_path, mime_type="image/jpeg")
        # print(f"Uploaded file '{uploaded_file.display_name}' as: {uploaded_file.uri}")

    # Upload the image to Gemini directly from memory
    image_data = image.file.read()
    image_file = io.BytesIO(image_data)
    uploaded_file = genai.upload_file(image_file, mime_type="image/jpeg")
    print(f"Uploaded file '{uploaded_file.display_name}' as: {uploaded_file.uri}")

    # Start a chat session with the Gemini model
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    uploaded_file,
                    "Return the text in the image. Don't insert line breaks in the output.",
                ],
            }
        ]
    )

    response = chat_session.send_message("Please process the image.")
    article = response.text

    return article
