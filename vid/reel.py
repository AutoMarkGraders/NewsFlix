import moviepy.editor as mp
from moviepy.config import change_settings
from moviepy.editor import *

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"}) # Path to ImageMagick executable

# VIDEO SETTINGS
width, height = 1080, 1920  # aspect ratio 9:16
duration = 30  # seconds

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
#input_text = "Moment dog sparks house fire after chewing power bank An indoor monitoring camera shows the moment a dog unintentionally caused a house fire after chewing on a portable lithium-ion battery power bank. In the video released by Tulsa Fire Department in Oklahoma, two dogs and a cat can be seen in the living room before a spark started the fire that spread within minutes. Tulsa Fire Department public information officer Andy Little said the pets escaped through a dog door, and according to local media the family was also evacuated safely. Had there not been a dog door, they very well could have passed away, he told CBS affiliate KOTV."
input_text = "Slovenian handball team makes it to Paris Olympics semifinal Lille, 8 August - Slovenia defeated Norway 33:28 in the Olympic men's handball tournament in Lille late on Wednesday to advance to the semifinal where they will face Denmark on Friday evening. This is the best result the team has so far achieved at the Olympic Games and one of the best performances in the history of Slovenia's team sports squads"
font_size = 150
font_color = 'yellow'

# Create the text clip (the width can be larger than the screen to allow movement)
text_clip = mp.TextClip(input_text, fontsize=font_size, color=font_color, font='Arial-Bold', size=(None, None), stroke_color="black", stroke_width=9)

# Length the text should move
text_width = text_clip.size[0]

# text scroll from right to left
text_clip = text_clip.set_position(lambda t: (width - int((text_width + width) * t / duration), height - 700)).set_duration(duration)

# Composite the text on the background
video = mp.CompositeVideoClip([background, text_clip], size=(width, height))

# Write the final video file
video.write_videofile("reel.mp4", fps=24)
