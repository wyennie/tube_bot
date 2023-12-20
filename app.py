from flask import Flask, render_template, request, redirect, url_for
from openai import OpenAI
import threading
from dotenv import load_dotenv
import os

import bot
import transcribe
import video_to_audio

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)
app = Flask(__name__)

# Route for the homepage
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Extract the YouTube URL from the form
        youtube_url = request.form.get('youtube_url')
        
        # Start transcription process in a separate thread
        threading.Thread(target=transcribe_video, args=(youtube_url,)).start()
        
        # Redirect to chat page
        return redirect(url_for('chat'))

    return render_template('index.html')

# Route for the chat interface
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    context = bot.read_transcribed_text('transcribed_text.txt')
    conversation = [] # Initialize the conversation history list

    if request.method == 'POST':
        # Process chatbot interaction
        user_message = request.form.get('user_message')
        chatbot_response = process_chatbot_message(user_message, context, conversation)
        return render_template('chat.html', response=chatbot_response)

    return render_template('chat.html')

def transcribe_video(youtube_url):
    # Transcription logic from your main.py
    video_to_audio.download_youtube_video(youtube_url)
    video_to_audio.convert_mp4_to_mp3('temp_video.mp4', 'temp_audio.mp3')
    transcribe.transcribe_audio_to_text('temp_audio.mp3', 'transcribed_text.txt', client)
    pass

def process_chatbot_message(user_message, context, conversation):
    # Chatbot processing logic
    response = bot.chat_with_bot(user_message, context, client, conversation)
    return response

if __name__ == '__main__':
    app.run(debug=True)
