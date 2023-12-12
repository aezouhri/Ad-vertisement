from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import whisper
import os  # Added import for os module
import openai
import config as cfg
import requests
from PIL import Image
from io import BytesIO

app = Flask(__name__)
CORS(app)

# Specify the desired language (e.g., "en-US" for U.S. English)
language = "en"

# Load the model with the specified language
model = whisper.load_model("tiny")


openai.api_key = cfg.open_ai_key


def generate_image_from_text(text_prompt):
    # Create the text prompt
    text_prompt_instance = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the engine that's suitable for text generation
        messages=[
            {
                "role": "system",
                "content": "You are a GPT designed for assisting in the creation of short movie advertisements. Given a text, you will create a prompt to generate and image. Do that and only that.",
            },
            {"role": "user", "content": text_prompt},
        ],
    )

    # Retrieve the generated text prompt
    generated_prompt = text_prompt_instance.choices[0].message["content"]

    # Use the generated text as input for the image prompt
    image_prompt_instance = openai.Image.create(
        model="dall-e-3",
        prompt=generated_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    # Retrieve the generated image
    generated_image = image_prompt_instance.data[0].url

    return generated_prompt, generated_image


def generate_instruction_given_image(image_url):
    read_image = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "You are assisting in the creating of a short movie advertisement. Your task is to give me very short instruction regarding potential cinematic and audio effect I could add that would match the given image.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            }
        ],
    )

    read_image_response = read_image.choices[0].message["content"]
    analysis_of_image = openai.ChatCompletion.create(
        model="gpt-4",  # Use the engine that's suitable for text generation
        messages=[
            {
                "role": "system",
                "content": "Given the description of an image. I want you to give me nice transitions, cinematic effects, and audio effects, that would match the description of the image.Only give me 3 to 4 very short points in the following JSON format: {\"visual_effect\": [\"effect_1_description\",\"effect_2_description\"],\"audio_effect\": [\"effect_1_description\",\"effect_2_description\"] }. Do that and only that. Answer should ONLY be a JSON!",
            },
            {"role": "user", "content": read_image_response},
        ],
    )

    return analysis_of_image.choices[0].message["content"]


@app.route("/")
def root():
    return send_from_directory("public", "index.html")


@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory("public", filename)


@app.route("/process_audio", methods=["POST"])
def process_audio():
    if "audio_data" not in request.files:
        return "Audio file not found", 400

    audio_file = request.files["audio_data"]

    temp_audio_path = "temp_audio.mp3"
    audio_file.save(temp_audio_path)

    # Process the audio file with Whisper
    result = model.transcribe("temp_audio.mp3", language=language)
    text = result["text"]

    print("Whisper :", text)

    generated_prompt, generated_image_url = generate_image_from_text(text)

    instructions = generate_instruction_given_image(generated_image_url)

    # # Make a GET request to the image URL
    # response = requests.get(generated_image_url)
    # # Load the image from the response content
    # generated_image = Image.open(BytesIO(response.content))

    # # Display the image
    # generated_image.show()

    # Return the transcribed text
    return jsonify(
        {"transcription": text, "prompt": generated_prompt, "instruction": instructions,
         "image_url": generated_image_url}
    )


if __name__ == "__main__":
    app.run(debug=True)
