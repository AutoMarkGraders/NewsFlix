#pip install moviepy pysrt

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import pysrt

# Load the video and subtitles
video = VideoFileClip("video.mp4")
subtitles = pysrt.open("subtitles.srt")

# Function to generate subtitle clips
def create_subtitle_clips(subs, video):
    subtitle_clips = []
    for sub in subs:
        start = sub.start.to_time()
        end = sub.end.to_time()
        text = sub.text.replace("\n", " ")

        txt_clip = (TextClip(text, fontsize=24, color='white', size=video.size)
                    .set_position('bottom')
                    .set_duration((end - start).total_seconds())
                    .set_start(start))
        subtitle_clips.append(txt_clip)
    return subtitle_clips

# Create subtitle clips and overlay them
subtitle_clips = create_subtitle_clips(subtitles, video)
final_video = CompositeVideoClip([video, *subtitle_clips])

# Export the video with subtitles
final_video.write_videofile("video_with_subtitles.mp4", fps=video.fps)
