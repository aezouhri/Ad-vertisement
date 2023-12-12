let recordButton = document.getElementById('recordButton');
let playButton = document.getElementById('playButton');
let transcribeButton = document.getElementById('transcribeButton');
let audioPlayback = document.getElementById('audioPlayback');

let mediaRecorder;
let audioChunks = [];
let audioBlob;

recordButton.addEventListener('click', () => {
    if (recordButton.textContent === 'Start Recording') {
        startRecording();
    } else {
        stopRecording();
    }
});

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();

            mediaRecorder.addEventListener('dataavailable', event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener('stop', () => {
                audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
                const audioUrl = URL.createObjectURL(audioBlob);
                audioPlayback.src = audioUrl;
                audioChunks = [];
                playButton.disabled = false;
                transcribeButton.disabled = false;
            });

            recordButton.textContent = 'Stop Recording';
        })
        .catch(error => {
            console.error('Error accessing media devices.', error);
        });
}

function stopRecording() {
    mediaRecorder.stop();
    recordButton.textContent = 'Start Recording';
}

playButton.addEventListener('click', () => {
    audioPlayback.play();
});

transcribeButton.addEventListener('click', () => {
    sendAudioToServer();
});

function sendAudioToServer() {
    let formData = new FormData();
    formData.append('audio_data', audioBlob, 'recording.mp3');

    fetch('/process_audio', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
    .then(data => {
        console.log('Transcription:', data.transcription);
        // Update the DOM with the transcription data
        let transcriptionElement = document.getElementById('transcription');
        transcriptionElement.textContent = data.transcription;
    })
    .catch(error => console.error('Error:', error));
}