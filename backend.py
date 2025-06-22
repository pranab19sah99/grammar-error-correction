# All imports
from flask import Flask, render_template, request, jsonify
from gramformer import Gramformer
from werkzeug.utils import secure_filename
from nltk.util import ngrams
from collections import Counter, defaultdict
import pandas as pd
import os
import re
import warnings
import itertools
import heapq

# Simple regex-based tokenizer is enough for our use case
def simple_tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())

# Flask app
app = Flask(__name__)

# Load JFLEG CSV corpus and build a bigram model from corrected sentences only
CORPUS_CSV_PATH = "./corpus/jfleg.csv"  # Path to the JFLEG CSV file

# get the grammar check library up 
gf = Gramformer(models=1)  # only correction

try:
    # Read the corpus and get the bigrams probability up
    df = pd.read_csv(CORPUS_CSV_PATH)
    corrected_sentences = df['corrections'].astype(str).tolist()

    # Flatten list-of-stringified-lists into proper sentences
    flattened = []
    for text in corrected_sentences:
        text = text.strip("[]")
        candidates = re.split(r"'\s*'", text)
        for c in candidates:
            cleaned = re.sub(r"['\[\]]", "", c).strip()
            if cleaned:
                flattened.append(cleaned)

    corpus_text = " ".join(flattened).lower()
    tokens = simple_tokenize(corpus_text)
    bigrams = list(ngrams(tokens, 2))
    bigram_freq = Counter(bigrams)
    unigram_freq = Counter(tokens)
except Exception as e:
    warnings.warn(f"Failed to load or process corpus: {e}. Defaulting to empty model.")
    bigram_freq = Counter()
    unigram_freq = Counter()

# Score a sentence based on bigram probabilities
def score_sentence(tokens):
    score = 0.0
    for i in range(len(tokens) - 1):
        bg = (tokens[i], tokens[i + 1])
        bg_count = bigram_freq.get(bg, 1)
        ug_count = unigram_freq.get(tokens[i], 1)
        prob = bg_count / ug_count
        score += prob
    #print(score) This was to check the score and it was good
    return score

# Generate sentence variants by using python library Gramformer
def generate_corpus_variants(tokens, top_k=3):
    corrections = gf.correct(tokens)
    return corrections if corrections else list(text)

# Main correction logic using corpus-based suggestions for prob
def checkGrammar(data):
    input_tokens = simple_tokenize(data) 
    candidate_variants = generate_corpus_variants(data.lower().strip())
    best_variant = max(list(candidate_variants), key=score_sentence)
    return best_variant

# Serve the main file. We have stored this in templates directory
@app.route('/')
def index():
    return render_template('index.html')

# Handle user text input via fetch/JSON
@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.get_json()
    corrected_text = checkGrammar(data['value'])
    print(corrected_text)
    result = {"message": f"Corrected: {corrected_text}"}
    return jsonify(result)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
