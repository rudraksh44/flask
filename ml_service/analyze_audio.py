import librosa

def analyze_speech(audio_data):
    # Assuming `audio_data` is a raw byte string or numpy array
    y, sr = librosa.load(audio_data, sr=None)
    
    # Extract pitch and amplitude features
    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)
    pitch = pitches.max()  # Getting the highest pitch as an example
    amplitude = magnitudes.mean()  # Average amplitude

    return {
        "pitch": pitch,
        "amplitude": amplitude
    }
