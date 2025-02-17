import moviepy.editor as mp
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"}) # path to ImageMagick executable
from moviepy.video.VideoClip import TextClip

import time
import os
from dotenv import load_dotenv
from math import ceil
import requests
from gtts import gTTS
from deep_translator import GoogleTranslator
from keybert import KeyBERT
from pydub import AudioSegment
import whisper

kb_model = KeyBERT() # load the model on app startup

def generate(summary, category, language):
    start_time = time.time()

# extract a keyphrase using english summary 
    keyphrase = kb_model.extract_keywords(summary, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=1,)[0][0]

# translate summary to target language
    if language != 'en':
        summary = GoogleTranslator(source="auto", target=language).translate(summary)
        print("\nTranslated Summary:", summary)
    # with open("translation.txt", "w", encoding="utf-8") as file:
    #     file.write(summary)

# gtts and speed up 1.1x to get reel.mp3
    tts = gTTS(summary, lang=language)
    tts.save("reeel.mp3")
    audio = AudioSegment.from_file("reeel.mp3")
    faster_audio = audio._spawn(audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * 1.1)}).set_frame_rate(audio.frame_rate)
    faster_audio.export("reel.mp3", format="mp3")
    os.remove("reeel.mp3")

# set duration as duration of reel.mp3
    narration = mp.AudioFileClip("reel.mp3")
    duration = narration.duration
    print(f'\nDuration = {duration}')

# fetch background images using keyphrase
    print(f'\nKeyphrase = {keyphrase}')
    n = ceil(duration/7)
    load_dotenv()
    API_KEY = os.getenv('PEXELS_KEY')
    url = 'https://api.pexels.com/v1/search'
    headers = {'Authorization': API_KEY}
    params = {
        'query': f'{keyphrase}',  # search term
        'per_page': n,  # Number of images 
        'orientation': 'portrait',
    }
    response = requests.get(url, headers=headers, params=params).json()
    for i, photo in enumerate(response['photos'], start=1):
        image_url = photo['src']['original']
        img_data = requests.get(image_url).content
        with open(f'{i}.jpg', 'wb') as handler: # saved in CWD (backend/)
            handler.write(img_data)
    print(f'\nNo.of images = {n}\n')

# set background images
    width, height = 1080, 1920  # aspect ratio 9:16
    video = mp.ColorClip(size=(width, height), color=(0, 0, 0), duration=0)
    
    backgrounds = []
    for i in range(1, n + 1):
        bg = mp.ImageClip(f"{i}.jpg").set_duration(7)
        # new width after resizing to maintain aspect ratio
        #image_width, image_height = bg.size
        #aspect_ratio = image_width / image_height
        #new_width = int(aspect_ratio * height)
        bg = bg.resize(height=height)
        # animation to move the image
        #bg = bg.set_position(lambda t: ((width - new_width) * (t / 10), 0))

        backgrounds.append(bg)

    # fast but no animation
    background = mp.concatenate_videoclips(backgrounds)
    video = mp.CompositeVideoClip([background], size=(width, height))

    # # slow but with animation
    # for bg in backgrounds:
    #     video = mp.CompositeVideoClip([video, bg.set_start(video.duration)], size=(width, height))

# transcript
    # Transcribe the audio with Whisper
    chunks = {}
    if language == 'en':
        model = whisper.load_model("base")
        transcription = model.transcribe("reel.mp3", word_timestamps=True)
        # for segment in transcription["segments"]:
        #     print(segment["text"])

        # turn it into per-second chunks
        #chunks = {}
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

    else:
        words = summary.split()
        word_duration = duration / len(words)
        for i, word in enumerate(words):
            second = int(i * word_duration)
            if second not in chunks:
                chunks[second] = []
            chunks[second].append(word)


    for second, words in (chunks.items()):
        if words == []: words.append('....') # if there is no transcript for that second
        print(f"[{second}s]: {' '.join(words)}")

# add captions
    lang_fonts = {"en": "C:/Windows/Fonts/ZILLASLABHIGHLIGHT-BOLD.ttf", "hi": "C:/Windows/Fonts/PRAGATINARROW-BOLD.ttf", "ml": "C:/Windows/Fonts/ANEKMALAYALAM-SEMIBOLD.ttf"}
    # Create TextClips for each second
    text_clips = []
    for second, words in chunks.items():
        caption_text = ' '.join(words)
        text = TextClip(
            caption_text,
            fontsize=70, 
            color="white",
            font=lang_fonts[language],
            stroke_color="black",
            stroke_width=2
        )
        text = text.set_position(("center", video.h - 400)).set_duration(1).set_start(second)
        text_clips.append(text)

    # Combine the video with the text clips
    video = mp.CompositeVideoClip([video, *text_clips])

    video = video.set_audio(narration)

    # Write the video file (1fps enough if no animation)
    half_time = time.time()
    video.write_videofile("reel.mp4", fps=1)
    end_time = time.time()
    print(f"Time taken to write reel.mp4 = {end_time - half_time} seconds\n")
    print(f"Total time taken to generate reel = {end_time - start_time} seconds\n")


if __name__ == '__main__':
    summary = "Slovenian handball team makes it to Paris Olympics semifinal Lille, 8 August - Slovenia defeated Norway 33:28 in the Olympic men's handball tournament in Lille late on Wednesday to advance to the semifinal where they will face Denmark on Friday evening. This is the best result the team has so far achieved at the Olympic Games and one of the best performances in the history of Slovenia's team sports squads"
    category = "handball"
    generate(summary, category)