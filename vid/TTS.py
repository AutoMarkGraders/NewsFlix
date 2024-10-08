from gtts import gTTS
import os

# Function to convert text to speech
def text_to_speech(text, lang='en', slow=False):
    tts = gTTS(text=text, lang=lang, slow=slow)
    tts.save("output.mp3")
    print("Speech saved as output.mp3")
    #os.system("start output.mp3")  # on Linux use "mpg321"

# Example usage
text = "Public Safety Paramount, Temple, Dargah On Road Must Go: Supreme Court"
text_to_speech(text)
