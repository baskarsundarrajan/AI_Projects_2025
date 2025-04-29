from flask import Flask, request, jsonify, render_template, send_from_directory
from fer import FER
import cv2
import os
from datetime import datetime
import tempfile
from generatemusic import main as generate_music_main

app = Flask(__name__)

# Paths to the text files
USER_FILE = "user.txt"
PREFERENCES_FILE = "final.txt"
MUSIC_FOLDER = "music"

def analyze_face_sentiment(image_path):
    """
    Analyzes an image with a single face to return the dominant sentiment using FER.

    Args:
        image_path (str): The file path to the image.

    Returns:
        list: A list containing the dominant emotion (e.g., 'happy', 'sad', 'neutral') for the face.
              Returns an empty list if no face is detected or if the image path is invalid.
    """
    results = ""

    # Input validation
    if not isinstance(image_path, str):
        return ""
    if not os.path.exists(image_path):
        return ""
    if not os.path.isfile(image_path):
        return ""

    try:
        # Initialize FER detector (uses MTCNN for face detection by default)
        detector = FER(mtcnn=True)

        # Read image using OpenCV
        img = cv2.imread(image_path)
        if img is None:
            return ""

        # Detect emotions
        result = detector.detect_emotions(img)

        # Process result for single face
        if result and len(result) > 0:
            # Get the first (and only) face's emotions
            emotions = result[0]['emotions']
            # Find the dominant emotion (highest score)
            dominant_emotion = max(emotions, key=emotions.get)
            results = dominant_emotion

    except Exception:
        return ""

    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_message', methods=['POST'])
def save_message():
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({"error": "No message provided"}), 400

        # Append the message to user.txt
        with open(USER_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{message}\n")
        
        return jsonify({"status": "Message saved successfully"}), 200
    
    except Exception as e:
        print(f"Error saving message: {e}")
        return jsonify({"error": "Failed to save message"}), 500

@app.route('/save_preferences', methods=['POST'])
def save_preferences():
    try:
        data = request.get_json()
        preferences = data.get('preferences', '').strip()
        
        if not preferences:
            return jsonify({"error": "No preferences provided"}), 400

        # Append the preferences to final.txt
        with open(PREFERENCES_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[Music Preferences: {preferences}\n")
        
        return jsonify({"status": "Preferences saved successfully"}), 200
    
    except Exception as e:
        print(f"Error saving preferences: {e}")
        return jsonify({"error": "Failed to save preferences"}), 500

@app.route('/analyze_face', methods=['POST'])
def analyze_face():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400

        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({"error": "No image selected"}), 400

        # Save the image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            image_path = temp_file.name
            image_file.save(image_path)

        # Analyze the image for sentiment
        sentiment = analyze_face_sentiment(image_path)

        # Clean up the temporary file
        try:
            os.unlink(image_path)
        except Exception as e:
            print(f"Error deleting temporary file: {e}")

        if not sentiment:
            return jsonify({"error": "No face detected or invalid image", "sentiment": ""}), 200

        # Append the sentiment to final.txt
        with open(PREFERENCES_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{sentiment}\n")

        return jsonify({"status": "Sentiment analyzed successfully", "sentiment": sentiment}), 200
    
    except Exception as e:
        print(f"Error analyzing face: {e}")
        return jsonify({"error": "Failed to analyze image"}), 500

@app.route('/gen', methods=['POST'])
def generate_music():
    try:
        # Call the main() function from generatemusic.py
        generate_music_main()
        
        # Find the latest file in the music folder
        music_folder = MUSIC_FOLDER
        if os.path.exists(music_folder):
            files = [os.path.join(music_folder, f) for f in os.listdir(music_folder) if os.path.isfile(os.path.join(music_folder, f))]
            if files:
                latest_file = max(files, key=os.path.getctime)
                filename = os.path.basename(latest_file)
                # Clear user.txt and final.txt
                with open(USER_FILE, 'w', encoding='utf-8') as f:
                    pass  # Truncate to empty
                with open(PREFERENCES_FILE, 'w', encoding='utf-8') as f:
                    pass  # Truncate to empty
                return jsonify({"status": "Music generated successfully", "filepath": latest_file, "filename": filename}), 200
        
        return jsonify({"error": "Music generation completed, but no file found"}), 200
    
    except FileNotFoundError as e:
        print(f"Error generating music: {e}")
        return jsonify({"error": str(e)}), 400
    except ValueError as e:
        print(f"Error generating music: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Error generating music: {e}")
        return jsonify({"error": "Failed to generate music"}), 500

@app.route('/music/<filename>')
def serve_music(filename):
    try:
        return send_from_directory(MUSIC_FOLDER, filename)
    except Exception as e:
        print(f"Error serving music file: {e}")
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    # Ensure the user.txt file exists
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, 'w', encoding='utf-8') as f:
            pass
    # Ensure the final.txt file exists
    if not os.path.exists(PREFERENCES_FILE):
        with open(PREFERENCES_FILE, 'w', encoding='utf-8') as f:
            pass
    # Ensure the music folder exists
    if not os.path.exists(MUSIC_FOLDER):
        os.makedirs(MUSIC_FOLDER)
    app.run(debug=True, host='0.0.0.0', port=5000)