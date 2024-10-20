from flask import Flask, render_template, request, jsonify
import os
from deepface import DeepFace
import cv2
import torch
import torch.nn as nn   
import librosa
import numpy as np

app = Flask(__name__)

class EmotionCNN(nn.Module):
    def __init__(self):
        super(EmotionCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.fc1 = nn.Linear(64 * 10 * 25, 128)
        self.fc2 = nn.Linear(128, 7)
        self.dropout = nn.Dropout(p=0.5)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.reshape(x.size(0), -1)
        x = self.dropout(torch.relu(self.fc1(x)))
        x = self.fc2(x)
        return x
model=EmotionCNN()
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/interview')
def interview():
    return render_template('interview.html')

@app.route('/interview', methods=['POST'])
def handle_interview():
    if 'interview_recording' not in request.files:
        return jsonify({'status': 'error', 'message': 'No video data received'}), 400
    
    recording = request.files['interview_recording']
    temp_file_path = os.path.join("uploads", recording.filename)
    recording.save(temp_file_path)

    expression_list = []

    def analyze_frame(frame):
        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            if isinstance(result, list):
                dominant_emotion = result[0]['dominant_emotion']
            else:
                dominant_emotion = result['dominant_emotion']
            expression_list.append(dominant_emotion)
        except Exception as e:
            print("Error analyzing frame: ", e)

    cap = cv2.VideoCapture(temp_file_path)
    
    if not cap.isOpened():
        return jsonify({'status': 'error', 'message': 'Failed to open video'}), 400

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        analyze_frame(frame_rgb)

    cap.release()
    os.remove(temp_file_path)

    if not expression_list:
        return jsonify({"status": "error", "message": "No expressions detected"}), 400

    emotion_counts = {emotion: expression_list.count(emotion) for emotion in ['happy', 'sad', 'fear', 'disgust', 'angry', 'surprise', 'neutral']}
    total_expressions = len(expression_list)
    percentages = {emotion: (count / total_expressions) * 100 for emotion, count in emotion_counts.items()}
    dominant_expr = max(percentages, key=percentages.get)

    return jsonify({
        "dominant_emotion": dominant_expr,
        "percentages": percentages
    })
@app.route('/interview/audio', methods=['POST'])
def handle_audio_snippet():
    if 'audio_recording' not in request.files:
        print("Error: No audio file part in the request")
        return jsonify({'error': 'No audio file part in the request'}), 400
    
    file = request.files['audio_recording']
    
    if file.filename == '':
        print("Error: No selected audio file")
        return jsonify({'error': 'No selected audio file'}), 400

    try:
        # Load audio file
        audio_data, sr = librosa.load(file, sr=None)
        print("Loaded audio data with sample rate:", sr)
        print("Audio data length:", len(audio_data))

        # Process audio in chunks of 5 seconds
        duration = 5  # seconds
        mfcc_features = []

        for start in range(0, len(audio_data), duration * sr):
            end = start + (duration * sr)
            chunk = audio_data[start:end]
            
            if len(chunk) < duration * sr:
                continue  # Skip if the last chunk is not long enough

            # Extract MFCC features
            mfcc = librosa.feature.mfcc(y=chunk, sr=sr, n_mfcc=13)
            mfcc_mean = np.mean(mfcc, axis=1)
            mfcc_input = torch.tensor(mfcc_mean, dtype=torch.float32).unsqueeze(0)  # Shape (1, n_mfcc)
            mfcc_features.append(mfcc_input)

        if mfcc_features:
            mfcc_features = torch.cat(mfcc_features)  # Shape (batch_size, n_mfcc)
            with torch.no_grad():
                predictions = model(mfcc_features)
            predicted_classes = torch.argmax(predictions, dim=1).tolist()

            print("Predictions:", predicted_classes)
            return jsonify({'predictions': predicted_classes}), 200
        else:
            print("No valid audio chunks processed")
            return jsonify({'message': 'No valid audio chunks processed'}), 400
    except Exception as e:
        print("An error occurred:", str(e))
        return jsonify({'error': 'An error occurred while processing audio: {}'.format(str(e))}), 500

if __name__ == '__main__':
    if not os.path.exists("uploads"):
        os.makedirs("uploads")  # Create an uploads directory to store temporary video files
    app.run(debug=True)
