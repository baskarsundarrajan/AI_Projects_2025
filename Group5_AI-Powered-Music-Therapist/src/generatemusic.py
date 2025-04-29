import requests
import time
import os

# Placeholder for analyze_dominant_sentiment (not provided)
def analyze_dominant_sentiment():
    # Placeholder: Assuming this function is not critical for music generation
    print("analyze_dominant_sentiment called (placeholder)")
    pass

# --- Ollama Settings ---
OLLAMA_API_URL = 'http://localhost:11434/api/generate'
OLLAMA_MODEL = 'gemma2:2b'
TEXT_FILE_PATH = 'final.txt'  # This is your text input file

# --- Beatoven Settings ---
API_TOKEN = 'YhF266ZWSoq8ET1I_MNbUA'  # <<<--- PUT YOUR TOKEN HERE
BASE_URL = 'https://public-api.beatoven.ai'

# Set headers for Beatoven
HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}

# --- Step 0: Generate the Prompt using Ollama ---
def generate_final_prompt(file_path=TEXT_FILE_PATH):
    """Reads final.txt and generates a prompt using Ollama."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'File "{file_path}" not found!')

    with open(file_path, 'r', encoding='utf-8') as f:
        text_data = f.read().strip()

    if not text_data:
        raise ValueError('Input text file is empty!')

    prompt = f'based on this "{text_data}" generate a text prompt (example: peaceful lo-fi chill hop track) to lift up the mood. only give me the text prompt as output and nothing else.'

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()

    response_data = response.json()
    final_prompt = response_data.get('response', '').strip()
    
    if not final_prompt:
        raise ValueError('Failed to generate a prompt from Ollama!')

    print(f'📜 Generated final prompt: "{final_prompt}"')
    return final_prompt

# --- Beatoven Functions (Same as yours) ---
def create_track(prompt_text):
    url = f'{BASE_URL}/api/v1/tracks'
    payload = {
        "prompt": {
            "text": prompt_text
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    track_id = response.json()['tracks'][0]
    print(f'✅ Track created with ID: {track_id}')
    return track_id

def compose_track(track_id, format='wav', looping=False):
    url = f'{BASE_URL}/api/v1/tracks/compose/{track_id}'
    payload = {
        "format": format,
        "looping": looping
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    task_id = response.json()['task_id']
    print(f'🎶 Composition started with Task ID: {task_id}')
    return task_id

def check_task_status(task_id):
    url = f'{BASE_URL}/api/v1/tasks/{task_id}'
    while True:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        status = data['status']
        print(f'🔄 Task status: {status}')
        
        if status == 'composed':
            return data['meta']
        elif status in ['composing', 'running']:
            time.sleep(5)
        else:
            raise Exception(f'❗ Unexpected task status: {status}')

def download_file(file_url, folder='music'):
    print(f'⬇️ Downloading track...')
    os.makedirs(folder, exist_ok=True)
    base_url = file_url.split('?')[0]
    filename_only = base_url.split('/')[-1]
    filepath = os.path.join(folder, filename_only)

    response = requests.get(file_url, stream=True)
    response.raise_for_status()
    
    with open(filepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f'✅ Download completed: {filepath}')
    return filepath

# --- Main Program ---
def main():
    try:
        analyze_dominant_sentiment()
        # Step 0: Generate prompt from final.txt via Ollama
        final_prompt = generate_final_prompt()
        
        # Step 1: Create track using generated prompt
        track_id = create_track(final_prompt)
        
        # Step 2: Compose the track
        task_id = compose_track(track_id)
        
        # Step 3: Wait until it's composed
        meta = check_task_status(task_id)
        
        # Step 4: Download the composed music
        print("\n🎉 Track successfully composed!")
        track_url = meta['track_url']
        print(f"Track URL: {track_url}")
        
        filepath = download_file(track_url, folder='music')
        return filepath
    
    except Exception as e:
        print(f'❌ Error: {e}')
        raise

if __name__ == '__main__':
    main()