import moviepy.editor as mp
from moviepy.config import change_settings
# path to ImageMagick executable
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

from moviepy.editor import *
from moviepy.video.VideoClip import TextClip

# Video settings
width, height = 1080, 1920  # Mobile screen resolution (aspect ratio 9:16)
duration = 10  # in seconds
#background = ColorClip(size=(width, height), color=(0, 255, 0), duration=duration) # Green background
background = ImageClip('stock_image.jpg').set_duration(duration).resize((width, height))

input_text = "This is a long string that will scroll through the screen like a subtitle."
font_size = 100
font_color = 'white'

# Create text clip (the width can be larger than the screen to allow movement)
text_clip = mp.TextClip(input_text, fontsize=font_size, color=font_color, size=(None, None))

# length the text should move
text_width = text_clip.size[0]

# text scroll from right to left
text_clip = text_clip.set_position(lambda t: (width - int(t * (text_width + width) / duration), height - 1000)).set_duration(duration)

# Composite the text on the background
video = mp.CompositeVideoClip([background, text_clip])

video.write_videofile("video.mp4", fps=24)