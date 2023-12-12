from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import whisper
import os  # Added import for os module

app = Flask(__name__)
CORS(app)
# Load your Whisper model
model = whisper.load_model("small")

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
    # print(request.files['audio_data'])
    # Save the audio file temporarily
    temp_audio_path = "temp_audio.mp3"
    audio_file.save(temp_audio_path)

    # Process the audio file with Whisper
    result = model.transcribe("temp_audio.mp3")
    text = result["text"]

    print("Whisper :", text)

    # Return the transcribed text
    return jsonify({'transcription': "empty"})

if __name__ == '__main__':
    app.run(debug=True)
