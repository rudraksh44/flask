document.getElementById('interview-button').addEventListener('click', async () => {
  const videoElement = document.getElementById('video');
  const audioElement = document.getElementById('audio');
  
  // Access video and audio streams
  const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
  videoElement.srcObject = stream;
  audioElement.srcObject = stream;
  
  // Record the video and audio
  const mediaRecorder = new MediaRecorder(stream);
  mediaRecorder.start();

  let chunks = [];
  
  mediaRecorder.ondataavailable = (event) => {
    chunks.push(event.data); // Collect data chunks
    
    if (mediaRecorder.state === "inactive") {
      // Combine all chunks into a single Blob
      const blob = new Blob(chunks, { type: "video/webm" });
      
      const formData = new FormData();
formData.append('interview_recording', fileInputElement.files[0]); // Assuming you have a file input

fetch('/interview', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.status === 'success') {
        window.location.href = '/interview';
        console.log(data.message);
    } else {
        console.error('Error:', data.message);
    }
})
.catch(error => console.error('Error posting interview data:', error));

  // Stop recording after a certain time, e.g., 5 seconds (5000 ms)
  setTimeout(() => {
    mediaRecorder.stop(); // Stop recording
  }, 5000);

    }
  };
});
// Audio extraction every 5 seconds
setInterval(() => {
  const audioBlob = new Blob(chunks, { type: 'audio/webm' }); // Assuming chunks is defined
  const audioFormData = new FormData();
  audioFormData.append('audio_recording', audioBlob, 'audio.webm'); // Specify a name

  fetch('/interview/audio', {
      method: 'POST',
      body: audioFormData
  })
  .then(response => {
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      return response.json();
  })
  .then(data => console.log("Audio processed", data))
  .catch(error => console.error('Audio Error:', error));
}, 5000); // Sends audio every 5 seconds

