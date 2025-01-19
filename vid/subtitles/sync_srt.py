#pip install librosa numpy pysrt

import librosa
import pysrt

# Load audio from the video
audio_file = "video.mp4"
audio, sr = librosa.load(audio_file, sr=None, mono=True)

# Detect silent intervals to segment speech
silence_threshold = 0.02  # Adjust based on your audio
intervals = librosa.effects.split(audio, top_db=-20)

# Your transcript text
transcript = [
    "Hello, and welcome to the video.",
    "In this section, we'll cover Python programming.",
    "Thank you for watching!"
]

# Generate SRT file
subs = pysrt.SubRipFile()
for idx, (start, end) in enumerate(intervals[:len(transcript)]):
    start_time = librosa.frames_to_time(start, sr=sr)
    end_time = librosa.frames_to_time(end, sr=sr)
    
    subs.append(pysrt.SubRipItem(
        index=idx + 1,
        start=f"{int(start_time // 3600):02}:{int(start_time % 3600 // 60):02}:{start_time % 60:.3f}".replace('.', ','),
        end=f"{int(end_time // 3600):02}:{int(end_time % 3600 // 60):02}:{end_time % 60:.3f}".replace('.', ','),
        text=transcript[idx]
    ))

# Save to SRT
subs.save("subtitles.srt", encoding="utf-8")
