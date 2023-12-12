import openai
import config as cfg

# Set up your OpenAI API credentials
openai.api_key = cfg.open_ai_api_key

# Create two instances of ChatGPT using the ChatGPT API
chat_gpt_instance_1 = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
)

chat_gpt_instance_2 = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What's the weather like today?"}
    ]
)

# Create an instance of Whisper using the Whisper API
whisper_instance = openai.Completion.create(
    engine="davinci-whisper",
    prompt="Tell me a secret.",
    max_tokens=50
)

# Use the instances as needed
response_1 = chat_gpt_instance_1.choices[0].message.content
response_2 = chat_gpt_instance_2.choices[0].message.content
whisper_response = whisper_instance.choices[0].text

print(response_1)
print(response_2)
print(whisper_response)