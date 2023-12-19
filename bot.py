def read_transcribed_text(file_path):
    """Reads the transcribed text from a file."""
    with open(file_path, 'r') as file:
        return file.read()

def chat_with_bot(user_input, context, client, conversation, model="gpt-4", frequency_penalty=0, max_tokens=350):
    """Creates a chat completion using the OpenAI API."""
    # Append user's message to the conversation history
    conversation.append({"role": "user", "content": user_input})

    # Preparing the messages for the API request
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "assistant", "content": context}
    ]
    messages += conversation

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
    conversation = [] # Initialize the conversation history list
    print("Chatbot is ready to talk! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        response = chat_with_bot(user_input, context, client, conversation)
        print("Bot:", response)