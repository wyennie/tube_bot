def transcribe_audio_to_text(audio_file_path, output_text_file, client):
   """
   Transcribe the given audio file to text using OpenAI's Whisper API.
   
   :param audio_file_path: str - Path to the audio file to transcribe
   :return: str - THe transcribed text.
   """

   try:
    with open(audio_file_path, 'rb') as audio_file:
        response = client.audio.transcriptions.create(
           model="whisper-1",
           file=audio_file
           )
      
        text = response.text
        
        with open(output_text_file, 'w') as text_file:
           text_file.write(text)
        print(f"Transcription saved to {output_text_file}")
   except client.OpenAIError as e:
      print(f"An error occurred with the OpneAI service: {e}")
   except Exception as e:
      print(f"An error ocurred: {e}")