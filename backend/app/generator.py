import moviepy.editor as mp
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"}) # path to ImageMagick executable
from moviepy.editor import *
from moviepy.video.VideoClip import TextClip

from math import ceil
import os
from dotenv import load_dotenv
import requests
from gtts import gTTS


def generate(summary, category):

    n = summary.count(' ') + 1 # no.of words
    print(f'Number of words: {n}')

    # fetch background images
    load_dotenv()
    API_KEY = os.getenv('PEXELS_KEY')
    url = 'https://api.pexels.com/v1/search'
    headers = {
        'Authorization': API_KEY
    }
    params = {
        'query': f'{category}',  # search term
        'per_page': ceil(n/25),  # Number of results 
        'orientation': 'landscape',
    }
    response = requests.get(url, headers=headers, params=params).json()
    for i, photo in enumerate(response['photos'], start=1):
        image_url = photo['src']['original']
        img_data = requests.get(image_url).content
        with open(f'{i}.jpg', 'wb') as handler: # saved in CWD (backend/)
            handler.write(img_data)    

    # Video settings
    width, height = 1080, 1920  # aspect ratio 9:16
    duration = n/25 * 10  # in seconds
    print(f'Duration= {duration}')

    background = ImageClip('1.jpg').set_duration(duration)

    # Calculate the new width after resizing to maintain the image's aspect ratio
    image_width, image_height = background.size
    aspect_ratio = image_width / image_height
    new_width = int(aspect_ratio * height)  # Adjust width according to the height to fit the mobile screen height
    # Resize the image to match the screen height while keeping the aspect ratio
    background = background.resize(height=height)
    # Adjust the animation to move the image fully across the screen
    background = background.set_position(lambda t: (int(min(0, (width - new_width) * (1 - t / duration))), 0))

    # SUBTITLE SETTINGS
    #input_text = "This is a long string that will scroll through the screen like a subtitle."
    font_size = 150
    font_color = 'yellow'

    # Create the text clip (the width can be larger than the screen to allow movement)
    text_clip = mp.TextClip(summary, fontsize=font_size, color=font_color, font='Arial-Bold', size=(None, None), stroke_color="black", stroke_width=5)

    # Length the text should move
    text_width = text_clip.size[0]

    # text scroll from right to left
    text_clip = text_clip.set_position(lambda t: (width - int((text_width + width) * t / duration), height - 700)).set_duration(duration)

    # Composite the text on the background
    video = mp.CompositeVideoClip([background, text_clip], size=(width, height))


    # narration audio
    tts = gTTS(text=summary, lang='en')
    tts.save("reel.mp3")
    narration = mp.AudioFileClip("reel.mp3")
    narration = narration.fx(mp.vfx.speedx, final_duration=duration)
    video = video.set_audio(narration)

    # Write the final video file
    video.write_videofile("reel.mp4", fps=24) # saved in CWD (backend/)

# better algo
# gtts to get reel.mp3
# set duration as 80% of reel.mp3 duration
# make video with multiple images
# add audio to video
# transcript
# add captions