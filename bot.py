def read_transcribed_text(file_path):
    """Reads the transcribed text from a file."""
    with open(file_path, 'r') as file:
        return file.read()

def chat_with_bot(user_input, context, client, model="gpt-4", frequency_penalty=0, max_tokens=350):
    """Creates a chat completion using the OpenAI API."""
    # Preparing the messages for the API request
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "assistant", "content": context},
        {"role": "user", "content": user_input}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        frequency_penalty=frequency_penalty,
        max_tokens=max_tokens
    )

    # Extracting the response message
    return response.choices[0].message.content

def start_chatbot(client):
    """Starts the chatbot interaction."""
    context = read_transcribed_text('transcribed_text.txt')
    print("Chatbot is ready to talk! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        response = chat_with_bot(user_input, context, client)
        print("Bot:", response)