import os
from flask import Flask, request, render_template, jsonify
from tools import download_youtube_video, convert_mp4_to_mp3, transcribe_audio_to_text, chat_with_bot, create_chatbot_context
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

conversation_context = []
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_video():
  video_url = request.form.get('youtube_url')

  video_path, error = download_youtube_video(video_url)
  if error:
    return jsonify({'error': error})
  
  audio_path, error = convert_mp4_to_mp3(video_path, 'temp_audio.mp3')
  if error:
    return jsonify({'error': error})
  
  transcribed_text, error = transcribe_audio_to_text(audio_path)
  if error:
    return jsonify({'error': error})
  
  global conversation_context
  conversation_context = create_chatbot_context(transcribed_text)

  return jsonify({'message': 'Transcription complete. You can now chat with the bot.'})

@app.route('/chat', methods=['POST'])
def chat():
  user_message = request.form.get('user_message')

  global conversation_context
  try:
    bot_response = chat_with_bot(conversation_context, user_message, client)
    return jsonify({'bot_response': bot_response})
  except Exception as e:
    return jsonify({'error': str(e)})

if __name__ == '__main__':
  app.run(debug=True)