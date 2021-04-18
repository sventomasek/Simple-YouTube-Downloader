from moviepy.editor import *
from pytube import YouTube
import os
import re

print('Very Simple YouTube Downloader by Sven Tomasek ( https://github.com/sventomasek )\n')

# This function will run whenever a chunk is downloaded from a video
def progress(stream, chunk, remaining):
    contentSize = video.filesize
    size = contentSize - remaining

    # Display the download progress
    print('\r' + 'Downloading: |%s%s| %.2f%%' % ('█' * int(size * 20 / contentSize), ' ' * (20 - int(size * 20 / contentSize)), float(size / contentSize * 100)), end = '')

while True:
    url = input('Video URL: ')
    format = input('File Format [mp4, mp3, wav]: ')
    logfile = open("logs.log", "w") # File used for storing errors

    # Get the video
    try: yt = YouTube(url, on_progress_callback = progress)
    except Exception as error:
        print(f'Connection error, check {logfile.name} for more info')
        logfile.write(str(error)) # Write error into the logfile
        os.system('pause')
        break

    video = yt.streams.filter(progressive = True, file_extension = 'mp4').get_highest_resolution()
    title = video.title # Get video title
    title = re.sub('[\/:*?"<>|]', '', title) # Remove characters from title
    dir = os.getcwd()

    # Download the video
    try:
        video.download()
        print('')
    except Exception as error:
        print(f'Failed downloading video, check {logfile.name} for more info')
        logfile.write(str(error))
        os.system('pause')
        break

    # Convert the video to mp3 or wav
    if format == 'mp3' or format == 'wav':
        try:
            video = VideoFileClip(f'{title}.mp4')
            video.audio.write_audiofile(f'{title}.{format}')
        except Exception as error:
            print(f'Failed converting video to {format}, check {logfile.name} for more info')
            logfile.write(str(error))
            os.system('pause')
            break
    else: format = 'mp4'

    print(f'\nFile saved to: {dir}\{title}.{format}\n')
