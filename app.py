from flask import Flask, render_template, request, jsonify
import cv2
import mediapipe as mp
import speech_recognition as sr

app = Flask(__name__)

# Initialize mediapipe for posture and face detection
mp_pose = mp.solutions.pose
mp_face_detection = mp.solutions.face_detection


# Route to render the homepage
@app.route('/')
def index():
    return render_template("index.html")


# Analyze video data (ML for posture and facial expressions)
@app.route('/analyze', methods=['POST'])
def analyze():
    # Retrieve the video file from the request
    video_file = request.files.get('video')

    # Convert video file to an OpenCV readable format
    cap = cv2.VideoCapture(video_file)

    with mp_pose.Pose() as pose, mp_face_detection.FaceDetection() as face_detection:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Analyze the frame for posture and facial expression
            results = pose.process(frame)
            face_results = face_detection.process(frame)

            # Process analysis results and return (dummy data for example)
            if results.pose_landmarks:
                analysis_result = {
                    "posture": "Good",
                    "facial_expression": "Neutral"
                }
            else:
                analysis_result = {
                    "posture": "Bad",
                    "facial_expression": "Nervous"
                }

            cap.release()
            return jsonify(analysis_result)

    return jsonify({"error": "Failed to analyze video"})


# Analyze audio data (ML for speech features like pitch and amplitude)
@app.route('/analyze-audio', methods=['POST'])
def analyze_audio():
    audio_file = request.files.get('audio')

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)

            # Speech to text conversion
            text = recognizer.recognize_google(audio)

            # Dummy confidence analysis (You can integrate pitch and amplitude analysis here)
            confidence_level = "High" if "confident" in text.lower() else "Low"

            return jsonify({
                "transcription": text,
                "confidence_level": confidence_level
            })
    except sr.UnknownValueError:
        return jsonify({"error": "Speech recognition could not understand the audio"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

