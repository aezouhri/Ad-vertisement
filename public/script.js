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
            // let transcriptionElement = document.getElementById('transcription');
            // let promptElement = document.getElementById('prompt');
            // let instructionElement = document.getElementById('instruction');
            // transcriptionElement.textContent = data.transcription;
            // promptElement.textContent = data.prompt;
            // instructionElement.textContent = data.instruction;

            // Create a new card element
            const card = document.createElement('div');
            card.classList.add('card');

            // Create an image element for the generated image
            const image = document.createElement('img');
            image.classList.add('card-image');
            image.src = data.image_url;
            image.alt = 'Generated Image';

            console.log(data.image_url);
            // Create a content container for the transcription and prompt
            const content = document.createElement('div');
            content.classList.add('card-content');

            // Create a heading element for the transcription
            const transcription = document.createElement('h3');
            transcription.classList.add('card-transcription');
            transcription.textContent = data.transcription;

            // Create a paragraph element for the prompt
            const prompt = document.createElement('p');
            prompt.classList.add('card-prompt');
            prompt.textContent = data.prompt;

            const instructions = document.createElement('p');
            instructions.classList.add('card-instructions');

            console.log("raw data: ",data.instruction);
            const instruction_data = JSON.parse(data.instruction);
            console.log("extracted: ", instruction_data);
            const visual_effect = instruction_data.visual_effect;
            const audio_effect = instruction_data.audio_effect;

            console.log("visual: ", visual_effect);
            console.log("audio: ",audio_effect);
            let visualEffectsList = 'Visual Effect:\n';
            visual_effect.forEach(effect => {
            visualEffectsList += `  - ${effect}\n`;
            });

            let audioEffectsList = 'Audio Effect:\n';
            audio_effect.forEach(effect => {
            audioEffectsList += `  - ${effect}\n`;
            });

            let instructionsText = visualEffectsList + '\n' + audioEffectsList;
            instructions.textContent = instructionsText;
            // Append the image, transcription, and prompt to the content container
            content.appendChild(transcription);
            content.appendChild(prompt);
            content.appendChild(instructions);

            // Append the image and content to the card
            card.appendChild(image);
            card.appendChild(content);

            // Append the card to a container element on your page
            const cardContainer = document.getElementById('cardContainer');
            cardContainer.appendChild(card);
            card.style.display = 'block';
        })
        .catch(error => console.error('Error:', error));
}

