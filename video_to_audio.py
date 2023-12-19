from pytube import YouTube
from moviepy.editor import AudioFileClip

def download_youtube_video(video_url):
    try:
        # Create a YouTube object
        yt = YouTube(video_url)

        # Get the highest resolution stream (MP4 format)
        video_stream = yt.streams.filter(file_extension='mp4').first()

        # Ensure there is a stream available to download
        if video_stream:
          # Download the video
          video_stream.download(filename='temp_video.mp4')
          print("Download successful! Check the file 'temp_video.mp4'")
        else:
          print("No available video streams match the criteria.")
    except Exception as e:
        print(f"An error occurred: {e}")

def convert_mp4_to_mp3(mp4_file_path, mp3_file_path):
  try:
    video_clip = AudioFileClip(mp4_file_path)
    video_clip.write_audiofile(mp3_file_path)
    video_clip.close()
    print(f"MP4 to MP3 conversion completed successfully! MP3 saved as:'temp_audio.mp3'")
  except Exception as e:
     print(f"An error occurred during conversion: {e}")