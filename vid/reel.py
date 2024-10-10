import moviepy.editor as mp
from moviepy.config import change_settings
from moviepy.editor import *

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"}) # Path to ImageMagick executable

# VIDEO SETTINGS
width, height = 1080, 1920  # aspect ratio 9:16
duration = 10  # seconds

background = ImageClip('stock_image.jpg').set_duration(duration)

# Calculate the new width after resizing to maintain the image's aspect ratio
image_width, image_height = background.size
aspect_ratio = image_width / image_height
new_width = int(aspect_ratio * height)  # Adjust width according to the height to fit the mobile screen height
# Resize the image to match the screen height while keeping the aspect ratio
background = background.resize(height=height)
# Adjust the animation to move the image fully across the screen
background = background.set_position(lambda t: (int(min(0, (width - new_width) * (1 - t / duration))), 0))

# SUBTITLE SETTINGS
input_text = "This is a long string that will scroll through the screen like a subtitle."
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
