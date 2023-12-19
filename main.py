from video_to_audio import download_youtube_video, convert_mp4_to_mp3
from transcribe import transcribe_audio_to_text

url = "https://youtu.be/2Pd0YExeC5o?si=mUoteWpg8VJSQ2-O"

download_youtube_video(url)
convert_mp4_to_mp3('temp_video.mp4', 'temp_audio.mp3')
transcribe_audio_to_text('temp_audio.mp3', 'transcribed_text.txt')