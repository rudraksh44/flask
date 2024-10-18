// Capture user's webcam video
const videoElement = document.getElementById('videoElement');
const analyzeButton = document.getElementById('analyzeButton');
const recordAudioButton = document.getElementById('recordAudioButton');
const analysisResult = document.getElementById('analysisResult');

// Log to confirm script is running
console.log("Webcam and audio capture script initialized.");

// Access the webcam stream
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        videoElement.srcObject = stream;
    })
    .catch(error => {
        console.error('Error accessing webcam:', error);
    });

// Capture video and send to the server for analysis
analyzeButton.addEventListener('click', () => {
    // Pause the video to capture the current frame
    videoElement.pause();
    
    // Create a canvas to draw the video frame
    const canvas = document.createElement('canvas');
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

    // Convert canvas to Blob (image) and send for analysis
    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append('video', blob, 'video.mp4');

        fetch('/analyze', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            analysisResult.innerHTML = `Posture: ${data.posture}, Facial Expression: ${data.facial_expression}`;
            videoElement.play();  // Resume video playback after analysis
        })
        .catch(error => {
            console.error('Error analyzing video:', error);
            analysisResult.innerHTML = 'Error analyzing video. Please try again.';
        });
    });
});

// Record and analyze audio
recordAudioButton.addEventListener('click', () => {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            const mediaRecorder = new MediaRecorder(stream);
            let audioChunks = [];

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.start();

            // Stop recording after 5 seconds
            setTimeout(() => {
                mediaRecorder.stop();
            }, 5000);

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const formData = new FormData();
                formData.append('audio', audioBlob);

                fetch('/analyze-audio', {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    analysisResult.innerHTML += `<br>Transcription: ${data.transcription}, Confidence Level: ${data.confidence_level}`;
                })
                .catch(error => {
                    console.error('Error analyzing audio:', error);
                    analysisResult.innerHTML += '<br>Error analyzing audio. Please try again.';
                });
            };
        })
        .catch(error => {
            console.error('Error accessing microphone:', error);
            analysisResult.innerHTML = 'Error accessing microphone. Please check your permissions.';
        });
});
