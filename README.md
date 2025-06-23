# grammar-error-correction

A grammar correction application that detects and fixes sentence structure, subject-verb agreement, punctuation, and word usage errors.
Built with **Flask** and **Python**, this project uses a corpus-based language model (trained on JFLEG) to perform grammar correction through a simple web interface.

---

## Features

* Corpus-driven grammar correction (no hardcoded rules)
* N-gram language model built from the JFLEG dataset
* Interactive web interface for testing corrections
* Supports both direct text input and file upload

---

## Prerequisites

* Python 3.8 or above
* pip (Python package installer)

---

## Step 1: Install Dependencies

You can optionally create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

Then install the dependencies:

```bash
pip install -r requirements.txt
```

Your `requirements.txt` should contain:

```
Flask
pandas
torch
spacy
git+https://github.com/PrithivirajDamodaran/Gramformer.git
```

After that, download the spaCy English language model:

```bash
python -m spacy download en_core_web_sm
```

---

## Step 2: Prepare the Corpus

Download the [JFLEG corpus](https://www.kaggle.com/datasets/thedevastator/jfleg-english-grammatical-error-benchmark) from Kaggle.
Place the file in the following location:

```
./corpus/jfleg.csv
```

If the `corpus` directory does not exist, create it and add the CSV file there.

---

## Step 3: Run the Flask Server

Launch the backend server:

```bash
python backend.py
```

You should see an output similar to:

```
Running on http://127.0.0.1:5000/
```

Open this link in your browser.

---

## Step 4: Use the Web Interface

The interface supports:

* Typing a sentence in the textbox (e.g., *He came to saw me*) and submitting it
* Uploading a `.txt` file for correction

Corrected output is returned in the same interface.

---

## Customization

To modify the correction logic, edit the `checkGrammar(data)` function in `backend.py`.
This function uses a statistical language model trained on the corpus to evaluate and correct grammar in user input.

---

## Troubleshooting

If you encounter issues during installation or execution, verify that:

* All dependencies installed successfully using `pip install -r requirements.txt`
* The `en_core_web_sm` model was downloaded using `python -m spacy download en_core_web_sm`
* The `corpus/jfleg.csv` file exists in the correct path
* The Flask server has access to required model files and data

---

## Examples

### Example 1: Direct Text Input

**Input:**

```
He came to saw me
```

**Corrected Output:**

```
He came to see me.
```

---

### Example 2: Uploading a Text File

**File Content (example.txt):**

```
I is baking today
He came to saw me
```

**Corrected Output:**

```
I am baking today.
He came to see me.
```

---
