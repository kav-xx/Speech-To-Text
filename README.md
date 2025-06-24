# 🗣️ Speech-to-Text Web App (with Live Postprocessing)

A lightweight, browser-based speech-to-text web app powered by **Flask**. It leverages **Web Speech API** for real-time speech recognition and integrates advanced NLP pipelines (punctuation restoration, spell correction, grammar correction) for clean, formatted transcripts. Transcripts are editable and downloadable.

## 🚀 Features

* 🎙️ Real-time speech recognition (Web Speech API)
* ✨ Automatic:

  * Punctuation restoration (via `deepmultilingualpunctuation`)
  * Spell correction (via `pyspellchecker`)
  * Grammar correction (via `language-tool-python`)
* 📝 Editable transcript area
* ↩️ Undo/Redo support (`Ctrl+Z`, `Ctrl+Y`)
* ⬇️ One-click download of final, cleaned transcript
* 🗑️ Clear/reset transcript
* ⏱️ Auto-stop after 30s silence detection
* 🎨 Stylish, responsive UI with animated wave visualization

## 🧠 Tech Stack

| Layer      | Tools/Frameworks                                                        |
| ---------- | ----------------------------------------------------------------------- |
| Frontend   | HTML, CSS, JavaScript (Vanilla), Web Speech API                         |
| Backend    | Flask, Python                                                           |
| NLP Models | `deepmultilingualpunctuation`, `pyspellchecker`, `language-tool-python` |
| Others     | NLTK (for sentence splitting), threading lock for safety                |

## 📦 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourname/speech-to-text-app.git
cd speech-to-text-app
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Flask app

```bash
python app.py
```

The app will run at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📄 File Structure

```
├── app.py                 # Flask backend
├── templates/
│   └── index.html         # Web interface
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## 🔍 Sample Output

```text
Recognized Speech ➜ "the patient is stable now and will be discharged tomorrow"

Postprocessed ➜
The patient is stable now.
He will be discharged tomorrow.
```
