import moviepy.editor as mp
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"}) # path to ImageMagick executable
from moviepy.video.VideoClip import TextClip

from math import ceil
import os
from dotenv import load_dotenv
import requests
from gtts import gTTS


def generate(summary, category):

# gtts to get reel.mp3
    tts = gTTS(text=summary, lang='en')
    tts.save("reel.mp3")

# set duration as 85% of reel.mp3 duration
    narration = mp.AudioFileClip("reel.mp3")
    duration = narration.duration * 0.85
    narration = narration.fx(mp.vfx.speedx, final_duration=duration)
    print(f'Duration = {duration}')

# fetch background images
    n = ceil(duration/10)
    load_dotenv()
    API_KEY = os.getenv('PEXELS_KEY')
    url = 'https://api.pexels.com/v1/search'
    headers = {
        'Authorization': API_KEY
    }
    params = {
        'query': f'{category}',  # search term
        'per_page': n,  # Number of images 
        'orientation': 'landscape',
    }
    response = requests.get(url, headers=headers, params=params).json()
    for i, photo in enumerate(response['photos'], start=1):
        image_url = photo['src']['original']
        img_data = requests.get(image_url).content
        with open(f'{i}.jpg', 'wb') as handler: # saved in CWD (backend/)
            handler.write(img_data)
    print(f'no.of images = {n}')

# set background images
    width, height = 1080, 1920  # aspect ratio 9:16
    video = mp.ColorClip(size=(width, height), color=(0, 0, 0), duration=0)
    
    backgrounds = []
    for i in range(1, n + 1):
        bg = mp.ImageClip(f"{i}.jpg").set_duration(10)
        # new width after resizing to maintain aspect ratio
        image_width, image_height = bg.size
        aspect_ratio = image_width / image_height
        new_width = int(aspect_ratio * height)
        bg = bg.resize(height=height)
        # animation to move the image fully across the screen
        bg = bg.set_position(lambda t: ((width - new_width) * (t / 10), 0))

        backgrounds.append(bg)

    # # fast but no animation
    # background = mp.concatenate_videoclips(backgrounds)
    # video = mp.CompositeVideoClip([background], size=(width, height))

    # slow but with animation
    for bg in backgrounds:
        video = mp.CompositeVideoClip([video, bg.set_start(video.duration)], size=(width, height))

# Set the audio to the video
    video = video.set_audio(narration)

    # transcript
    # add captions

    video.write_videofile("reel.mp4", fps=24)        


if __name__ == '__main__':
    summary = "Slovenian handball team makes it to Paris Olympics semifinal Lille, 8 August - Slovenia defeated Norway 33:28 in the Olympic men's handball tournament in Lille late on Wednesday to advance to the semifinal where they will face Denmark on Friday evening. This is the best result the team has so far achieved at the Olympic Games and one of the best performances in the history of Slovenia's team sports squads"
    category = "handball"
    generate(summary, category)