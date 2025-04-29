***Konkani Poem Next Word Prediction***
  
Overview
The Konkani Poem Next Word Prediction project harnesses artificial intelligence to preserve and generate poetry in Konkani, a culturally rich Indo-Aryan language spoken primarily in Goa, India. By fine-tuning a GPT-2 language model on the Konkani Sentiment Analysis Corpus, this project enables the creation of coherent poetic sequences and the prediction of the next word in a given prompt. Built with Hugging Face Transformers, PyTorch, and Python in a Google Colab environment, the system achieves a perplexity of 4.2243 and supports creative text generation with varying temperatures. The project aims to bridge the gap in digital tools for Konkani literature, fostering its revitalization and accessibility for enthusiasts and researchers.

Fine-tune GPT-2 for Konkani poetry generation and next-word prediction.
Preprocess a dataset of Konkani poems for training.
Evaluate model performance using perplexity and loss.
Demonstrate creative text generation with varying temperatures.
Provide a reproducible codebase for academic evaluation.

Fine-tuned GPT-2 model for Konkani poetry.
Generates poetic sequences from user prompts.
Predicts the next word in a given sequence.
Supports temperature variation (0.7, 0.9, 1.0, 1.3) for creative outputs.
Evaluated with perplexity (4.2243) and training loss (1.6310).

Dataset
The dataset comprises 54 Konkani poems from the Konkani Sentiment Analysis Corpus. Preprocessing steps:

Extracted text from .docx files using python-docx.
Removed metadata (e.g., poet names, sentiment counts).
Saved cleaned poems as .txt files.
Split: 70% training (38 poems), 15% validation (8 poems), 15% test (9 poems).

Installation
Prerequisites

Python 3.8+
Google Colab (recommended for assignment demo) or local environment with GPU
https://colab.research.google.com/drive/1g6aMtE3B8qDbMulMqg5OMy7bxycs6-Yh?usp=sharing
Git

Setup Instructions

Install Dependencies:Install required packages:
pip install transformers torch datasets python-docx


Obtain the Dataset:

Download the Konkani Sentiment Analysis Corpus from Annie Dhempe’s repository.
Place the .docx files in the data/ directory or modify the preprocessing script to point to your dataset location.

Usage
Running in Google Colab

Upload the repository files to Google Colab.
Install dependencies:!pip install transformers torch datasets python-docx

Use the provided notebook (trial_1.ipynb) or run scripts directly.

Generating Poetry
Run the following code to generate a poetic sequence:
from transformers import GPT2LMHeadModel, GPT2Tokenizer

Results

Training Loss: 1.6310 (after 3 epochs)
Evaluation Loss: 1.4409
Perplexity: 4.2243 (indicating good predictive performance for a small dataset)
Sample Output:Prompt: तुझें दिल म्हजें आकाश
Output: तुझें दिल म्हजें आकाश्ं वकरे तायां म्हां
        शव्ली मुकाश्ं दिल म्ह


Team Members: 

Sharvari Naik (24P0620008)

Zainab Rajabali (24P0620015)

Date: 28 April 2025




Preserving Konkani Poetry through Artificial Intelligence.
