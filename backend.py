# All imports
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from nltk.util import ngrams
from collections import Counter, defaultdict
import pandas as pd
import os
import re
import warnings
import itertools
import heapq

# Simple regex-based tokenizer (avoids nltk's punkt)
def simple_tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())

# Flask app
app = Flask(__name__)

# Load JFLEG CSV corpus and build a bigram model from corrected sentences only
CORPUS_CSV_PATH = "./corpus/jfleg.csv"  # Path to the JFLEG CSV file

try:
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
    return score

# Generate sentence variants by replacing low-probability tokens
def generate_corpus_variants(tokens, top_k=3):
    variants = [tokens[:]]

    for i in range(len(tokens) - 1):
        context = tokens[i], tokens[i + 1]
        bg = (tokens[i], tokens[i + 1])
        prob = bigram_freq.get(bg, 0) / (unigram_freq.get(tokens[i], 1))

        # If bigram is rare, try alternatives
        if prob < 0.01:
            prefix = tokens[i]
            candidates = [(bg[1], freq) for (w1, w2), freq in bigram_freq.items() if w1 == prefix]
            top_candidates = heapq.nlargest(top_k, candidates, key=lambda x: x[1])

            for word, _ in top_candidates:
                new_tokens = tokens[:i+1] + [word] + tokens[i+2:]
                variants.append(new_tokens)

    return variants

# Main correction logic using corpus-based suggestions
def checkGrammar(data):
    input_tokens = simple_tokenize(data)
    candidate_variants = generate_corpus_variants(input_tokens)
    best_variant = max(candidate_variants, key=score_sentence)
    return " " .join(best_variant)

# Serve the main file. We have stored this in templates directory
@app.route('/')
def index():
    return render_template('index.html')

# Handle user text input via fetch/JSON
@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.get_json()
    corrected_text = checkGrammar(data['value'])
    result = {"message": f"Corrected: {corrected_text}"}
    return jsonify(result)

# Handle file upload
@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        content = file.read().decode('utf-8')
        corrected = checkGrammar(content)
        return jsonify({"corrected": corrected})

    return jsonify({"error": "Invalid file"}), 400

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
