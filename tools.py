from pytube import YouTube
from moviepy.editor import AudioFileClip
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def download_youtube_video(video_url):
    try:
        yt = YouTube(video_url)
        video_stream = yt.streams.filter(file_extension='mp4').first()
        if video_stream:
          video_path = video_stream.download()
          return video_path, None
        else:
          return None, "No available video streams match the criteria."
    except Exception as e:
        return None, (f"An error occurred: {e}")

def convert_mp4_to_mp3(mp4_file_path, mp3_file_path):
  try:
    video_clip = AudioFileClip(mp4_file_path)
    video_clip.write_audiofile(mp3_file_path)
    video_clip.close()
    return mp3_file_path, None
  except Exception as e:
     return None, f"An error occurred during conversion: {e}"

def transcribe_audio_to_text(audio_file_path):
   try:
    with open(audio_file_path, 'rb') as audio_file:
        response = client.audio.transcriptions.create(
           model="whisper-1",
           file=audio_file
           )
    if response:
       text = response.text
       return text, None
    else:
       return None, f"An error occured: {response} - {response.text}"
   except Exception as e:
      return None, f"An error ocurred: {e}"

def create_chatbot_context(transcribed_text):
   return [{"role": "system", "content": transcribed_text}]

def chat_with_bot(conversation, user_message, client, model="gpt-4", frequency_penalty=0, max_tokens=350):
    try:
      conversation.append({"role": "user", "content": user_message})
      response = client.chat.completions.create(
          model=model,
          messages=conversation,
          frequency_penalty=frequency_penalty,
          max_tokens=max_tokens
      )

      assistant_message = response.choices[0].message.content
      conversation.append({"role": "assistant", "content": assistant_message})
      return assistant_message, None
    except Exception as e:
      return None, f"An error occured: {e}"
