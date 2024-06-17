import moviepy
from moviepy.editor import VideoFileClip
import os
import glob

mp4Path = rf"C:\Users\Trent\coding\python projects\San Diego Data Scrape"
mp4Files = glob.glob(os.path.join(mp4Path, '*.mp4'))
print(mp4Files.__class__)
for mp4 in mp4Files:
    filename = os.path.splitext(os.path.basename(mp4))[0]
    mp3Path = os.path.join(mp4Path, filename + '.mp3')
    videoClip = VideoFileClip(mp4)
    audioClip = videoClip.audio
    audioClip.write_audiofile(mp3Path)
    audioClip.close()
    videoClip.close()
