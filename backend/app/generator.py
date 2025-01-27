import moviepy.editor as mp
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"}) # path to ImageMagick executable
from moviepy.video.VideoClip import TextClip

from math import ceil
import os
from dotenv import load_dotenv
import requests
from gtts import gTTS
from pydub import AudioSegment
import whisper

def generate(summary, category):

# gtts and speed up to get reel.mp3
    tts = gTTS(text=summary, lang='en')
    tts.save("reeel.mp3")
    # 1.2 times faster
    audio = AudioSegment.from_file("reeel.mp3")
    faster_audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * 1.2)
    }).set_frame_rate(audio.frame_rate)
    faster_audio.export("reel.mp3", format="mp3")

# set duration as duration of reel.mp3
    narration = mp.AudioFileClip("reel.mp3")
    duration = narration.duration
    print(f'\nDuration = {duration}')

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
        'orientation': 'portrait',
    }
    response = requests.get(url, headers=headers, params=params).json()
    for i, photo in enumerate(response['photos'], start=1):
        image_url = photo['src']['original']
        img_data = requests.get(image_url).content
        with open(f'{i}.jpg', 'wb') as handler: # saved in CWD (backend/)
            handler.write(img_data)
    print(f'no.of images = {n}\n')

# TODO image every 7s
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
        # animation to move the image
        bg = bg.set_position(lambda t: ((width - new_width) * (t / 10), 0))

        backgrounds.append(bg)

    # fast but no animation
    background = mp.concatenate_videoclips(backgrounds)
    video = mp.CompositeVideoClip([background], size=(width, height))

    # # slow but with animation
    # for bg in backgrounds:
    #     video = mp.CompositeVideoClip([video, bg.set_start(video.duration)], size=(width, height))

# transcript
    # Step 1: Transcribe the audio with Whisper
    model = whisper.load_model("base")
    transcription = model.transcribe("reel.mp3", word_timestamps=True)

    # Step 2: turn it into per-second chunks
    chunks = {}
    last_word = None

    for segment in transcription["segments"]:
        words = segment.get("words", []) # returns [] if no words data in segment
        
        for word in words:
            word_start = word["start"]
            word_end = word["end"]
            word_text = word["word"]

            if word_start is None or word_end is None:
                continue

            # Round timestamps to the nearest second
            start_second = int(word_start)
            end_second = int(word_end)
            # Add word to the correct second
            for second in range(start_second, end_second + 1):
                if second not in chunks:
                    chunks[second] = [] 
                if word_text != last_word:  # Avoid repeating words
                    chunks[second].append(word_text)
                    last_word = word_text    

    for second, words in (chunks.items()):
        if words == []: words.append('....') # if there is no transcript for that second
        print(f"[{second}s]: {' '.join(words)}")

# add captions
    # Create a list of TextClips for each second
    text_clips = []
    for second, words in chunks.items():
        caption_text = ' '.join(words)
        text = TextClip(
            caption_text,
            fontsize=70, 
            color="white",
            font="Arial-Bold",
            stroke_color="black",
            stroke_width=2
        )
        text = text.set_position(("center", video.h - 400)).set_duration(1).set_start(second)
        text_clips.append(text)

    # Combine the video with the text clips
    video = mp.CompositeVideoClip([video, *text_clips])

    video = video.set_audio(narration)

    # Write the output video file
    video.write_videofile("reel.mp4", fps=10)


if __name__ == '__main__':
    summary = "Slovenian handball team makes it to Paris Olympics semifinal Lille, 8 August - Slovenia defeated Norway 33:28 in the Olympic men's handball tournament in Lille late on Wednesday to advance to the semifinal where they will face Denmark on Friday evening. This is the best result the team has so far achieved at the Olympic Games and one of the best performances in the history of Slovenia's team sports squads"
    category = "handball"
    generate(summary, category)