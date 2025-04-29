import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from transformers import pipeline
from collections import defaultdict

def analyze_dominant_sentiment(file_path="user.txt"):
    """
    Reads a text file, performs sentiment analysis on each line,
    and determines the top 3 dominant sentiments based on the sum of probabilities.
    Results are saved into 'final.txt'.
    
    Args:
        file_path (str): The path to the text file containing the chat log.
    """
    try:
        # Try a model specifically trained for emotions
        sentiment_pipeline = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions")
        sentiment_probabilities = defaultdict(float)
        total_lines = 0

        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    result = sentiment_pipeline(line)[0]
                    sentiment = result['label']
                    probability = result['score']
                    sentiment_probabilities[sentiment] += probability
                    total_lines += 1

        if total_lines > 0:
            # Sort sentiments by their total probability, descending
            sorted_sentiments = sorted(sentiment_probabilities.items(), key=lambda x: x[1], reverse=True)
            top_3_sentiments = sorted_sentiments[:3]

            # Write to final.txt
            with open('final.txt', 'a', encoding='utf-8') as output_file:
                for sentiment, total_probability in top_3_sentiments:
                    output_file.write(f"{sentiment}\n")

            # Print to console
            for sentiment, _ in top_3_sentiments:
                print(sentiment)

        else:
            print("The file is empty or contains only empty lines.")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")