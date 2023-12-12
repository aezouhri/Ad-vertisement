from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import whisper
import os  # Added import for os module

app = Flask(__name__)
CORS(app)

# Specify the desired language (e.g., "en-US" for U.S. English)
language = "en"

# Load the model with the specified language
model = whisper.load_model("tiny")

@app.route('/')
def root():
    return send_from_directory('public', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('public', filename)

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'audio_data' not in request.files:
        return "Audio file not found", 400

    audio_file = request.files['audio_data']

    temp_audio_path = "temp_audio.mp3"
    audio_file.save(temp_audio_path)

    # Process the audio file with Whisper
    result = model.transcribe("temp_audio.mp3", language=language)
    text = result["text"]

    print("Whisper :", text)

    # Return the transcribed text
    return jsonify({'transcription': text})

if __name__ == '__main__':
    app.run(debug=True)
