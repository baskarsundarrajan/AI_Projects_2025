# AI-Powered-Music-Therapist

# AI-Powered Therapist:Chatbot and Music Generation System


## **Project Overview**
This project is a Flask-based web application that simulates a therapeutic chatbot and generates personalized music to enhance user mood. Developed as a Master’s-level project, it integrates multiple AI technologies:

- **Therapist Chatbot**: Powered by Ollama’s gemma3:4b model, it engages users in empathetic dialogue, saving messages to `user.txt`.
- **Music Preferences Input**: Users specify genres/artists via a modal, saved to `final.txt`.
- **Facial Sentiment Analysis**: Uses the Facial Expression Recognition (FER) library to detect emotions from uploaded images, appending results to `final.txt`.
- **Music Generation**: Generates music prompts with Ollama’s gemma2:2b model, creates WAV tracks via the Beatoven API, and plays them in the browser.

The system, built with HTML, JavaScript, Tailwind CSS, and Python, demonstrates natural language processing (NLP), computer vision, and generative AI, showcasing their potential in mental health support and creative expression. Files (`user.txt`, `final.txt`) are cleared after successful music generation, ensuring a clean state for new interactions.


## **Installation Steps**
To set up the project, follow these steps:
## 1.Clone the Repository:
      ```bash
      git clone <repository-url>
      cd <repository-directory>

## 2.Set Up Python Environment:
- Use Python 3.8-3.10.
- Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

## 3.Install Dependencies:
- Install required Python libraries:
   ```bash
   pip install flask fer opencv-python requests tensorflow
   Note: fer requires TensorFlow. If installation issues occur, ensure compatibility or install TensorFlow separately: pip install tensorflow

## 4.Install and Configure Ollama:
- Download and install Ollama: [https://ollama.com/](https://ollama.com/)
- Pull the required models:
   ```bash
   ollama pull gemma3:4b
   ollama pull gemma2:2b

## 5.Obtain Beatoven API Token:
- Sign up at [https://beatoven.ai/](https://beatoven.ai/) and get an API token.
- Replace the placeholder token in `generatemusic.py` (`API_TOKEN = 'YhF266ZWSoq8ET1I_MNbUA'`) with your token.

## Project Structure:
- Ensure the following structure:
project_directory/
├── app.py
├── generatemusic.py
├── templates/
│ └── index.html
├── user.txt (created automatically)
├── final.txt (created automatically)
└── music/ (created automatically)

## **How to Run**
## 1.Start Ollama:
   - Run Ollama in a terminal:
     ```bash
     ollama serve
     
## 2.Run the Flask Application:
- From the project directory, execute:
     ```bash
     python app.py
- The server will start at http://localhost:5000.

## 3.Access the Application:
- Open a browser and navigate to [http://localhost:5000](http://localhost:5000).
- The UI displays a chat interface, preferences modal, face upload button, and music generation button.

## 4.Usage:
- **Chat**: Type messages to interact with the therapist chatbot (saved to `user.txt`).
- **Preferences**: Click “Preferences” (green button) to input music preferences (saved to `final.txt`).
- **Face Analysis**: Click “Face” (purple button) to upload an image for sentiment analysis (saved to `final.txt`).
- **Generate Music**: Click “Generate” (orange button) to create a music track based on `final.txt`. The track plays in the UI, and files are cleared.
- Check the `music/` folder for generated WAV files.

## **Examples**
Below are example interactions with the system:

## Examples

### Chat Interaction:
- **Input**: User types, “I’m feeling stressed.”
- **Output**: Chatbot responds, “I’m here to help. Can you share what’s been stressing you out?” (saved to `user.txt`).
- **UI**: Message appears in the chat history with a blue user bubble and gray bot bubble.

### Music Preferences:
- **Input**: User enters “Jazz, The Beatles” in the preferences modal.
- **Output**: Saved to `final.txt` as “[2025-04-27 10:15:23] Music Preferences: Jazz, The Beatles”.
- **UI**: Confirmation message: “Music preferences saved successfully!”

### Facial Sentiment Analysis:
- **Input**: User uploads a smiling face image.
- **Output**: FER detects “happy”, saved to `final.txt` as “[2025-04-27 10:16:45] Facial Sentiment: happy”.
- **UI**: Message: “Detected facial sentiment: happy”.

### Music Generation:
- **Input**: `final.txt` contains “Jazz, happy”.
- **Process**: gemma2:2b generates prompt “uplifting jazz fusion track”; Beatoven creates a WAV file.
- **Output**: Track saved to `music/track.wav`, playable in the UI with an `<audio>` player.
- **UI**: Message: “Music generated successfully!” with play/pause controls.

## **Team Members and Roles**

### Tanmay Parab:
- **Role**:Developer
- **Responsibilities**:
  - Designed and implemented the Flask application (`app.py`, `index.html`).
  - Integrated Ollama, FER, and Beatoven API for AI functionalities.
  - Developed music generation logic (`generatemusic.py`).
  - Conducted testing, debugging, and documentation.
  - Performed prompt engineering for chatbot and music prompts.

### Ramachandra Kaloji:
- **Role**:Developer
- **Responsibilities**:
  - Designed sentiment analysis code.
  - Developed the user interface (UI).
  - Created project documentation.
  - Developed music generation logic (`generatemusic.py`).
  - Conducted testing of the application.
  - Performed prompt engineering for AI models.

## **Additional Notes**
## Prerequisites:
- Ensure a stable internet connection for Beatoven API calls.
- Verify sufficient Beatoven API credits for music generation.

## Troubleshooting:
- If Ollama fails to connect, check [http://localhost:11434](http://localhost:11434) and restart the server.
- For FER errors, ensure TensorFlow compatibility and test with clear, single-face images.
- If music generation fails, verify the Beatoven token and `final.txt` content.

## Limitations:
- The chatbot is not a professional therapist; it simulates empathetic dialogue.
- FER may fail with poor lighting or multiple faces.
- Music generation requires a non-empty `final.txt`.


### License:None
