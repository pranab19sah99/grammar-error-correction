# grammar-error-correction
A grammar correction app that detects and fixes sentence structure, subject-verb agreement, punctuation, and word usage errors. Built with Flask and Python, featuring a simple web interface.



### Prerequisites

Ensure you have **Python** installed, either directly or through a **Miniconda** environment.

### Step 1: Install Flask

Open a terminal or command prompt and run:

```bash
pip install Flask
```

### Step 2: Set Up the Project

Copy all files into your working directory.

### Step 3: Launch the Backend Server

Run the following command:

```bash
python ./backend.py
```

You should see output similar to:

```
Running on http://127.0.0.1:5000
```

You can either **Ctrl+Click** the link or copy it into your browser to access the application.

### Step 4: Add Your Backend Logic

To extend the backend functionality, edit the `backend.py` file.
Specifically, modify the following function:

```python
def checkGrammar(data):
    # Your logic here
```

