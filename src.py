from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
import subprocess
import sys
from datetime import datetime

clear = lambda: os.system('cls')
clear()

def downloadVideo(url):
    try:
        now = datetime.now()
        curTime = now.strftime("%m%d%Y_%H%M%S")
        curPath = os.path.dirname(os.path.abspath(sys.argv[0]))
        outputPath = curPath + "\\output"
        ffmpegpath = curPath + "\\ffmpeg\\ffmpeg.exe"

        video = YouTube(url, use_oauth=True, allow_oauth_cache=True, on_progress_callback=on_progress)
        video_stream = video.streams.filter(only_video=False, file_extension='mp4').order_by('bitrate').desc().first()
        print("{} is now downloading... ({}mb)".format(video_stream.title, video_stream.filesize_mb))
        video_path = video_stream.download(filename="video.mp4", output_path=outputPath)

        audio_stream = video.streams.filter(only_audio=True).order_by("abr").desc().first()
        audio_path = audio_stream.download(filename="audio.mp3", output_path=outputPath)

        clear()
        print("Merging...")
        subprocess.run([
            ffmpegpath, "-i", video_path, "-i", audio_path, 
            "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", outputPath+"\\{}_result.mp4".format(curTime),
            "-y"
        ], check=True, shell=True)

        clear()

        print("{} is downloaded!".format(video_stream.title))
        os.remove(video_path)
        os.remove(audio_path)        
    except Exception as e:
        print("Download failed!", e)

url = sys.argv[1]
if url != "":
    clear()
    print("Fetching...")
    downloadVideo(url)

ask = True
while ask == 1:
    url = input("Enter the YouTube video link: ")
    if url.upper() == "EXIT":
        print("Exiting program...")
        ask = False
    else:
        clear()
        print("Fetching...")
        downloadVideo(url)