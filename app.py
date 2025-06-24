from flask import Flask, render_template, jsonify, request
import threading
import re
import language_tool_python
from spellchecker import SpellChecker
from nltk.tokenize import sent_tokenize
from deepmultilingualpunctuation import PunctuationModel
import nltk

nltk.download('punkt')

# Initialize Flask app
app = Flask(__name__)
lock = threading.Lock()

# Load models
punct_model = PunctuationModel()
tool = language_tool_python.LanguageTool('en-US')
spell = SpellChecker()

# ---------- Text Postprocessing ----------
def postprocess_text(text):
    if not text:
        return ""

    # Step 1: Normalize whitespace and remove repeated words
    text = re.sub(r'\s+', ' ', text.strip())
    text = re.sub(r'\b(\w+)( \1\b)+', r'\1', text, flags=re.IGNORECASE)

    # Step 2: Punctuation restoration
    punctuated = punct_model.restore_punctuation(text)

    # Step 3: Capitalize first letters of sentences
    punctuated = re.sub(r'([.!?])\s+([a-z])', lambda m: m.group(1) + ' ' + m.group(2).upper(), punctuated)
    if punctuated:
        punctuated = punctuated[0].upper() + punctuated[1:]

    # Step 4: Spell correction
    words = punctuated.split()
    corrected_words = []
    for word in words:
        if word.lower() not in spell and word.isalpha() and not word.istitle():
            corrected_words.append(spell.correction(word) or word)
        else:
            corrected_words.append(word)
    spellchecked_text = ' '.join(corrected_words)

    # Step 5: Grammar correction
    matches = tool.check(spellchecked_text)
    grammar_corrected = language_tool_python.utils.correct(spellchecked_text, matches)

    # Step 6: Final cleanup
    grammar_corrected = re.sub(r'\s{2,}', ' ', grammar_corrected)
    grammar_corrected = re.sub(r'([.,!?])(?=\S)', r'\1 ', grammar_corrected)

    # Step 7: Sentence splitting
    sentences = sent_tokenize(grammar_corrected.strip())
    return "\n".join(sentence.strip() for sentence in sentences)

# ---------- Routes ----------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_transcript', methods=['POST'])
def save_transcript():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({'status': 'empty text'}), 400

    with lock:
        processed = postprocess_text(text)
    return jsonify({'status': 'saved', 'processed_text': processed})

@app.route('/download', methods=['POST'])
def download_transcript():
    data = request.get_json()
    content = data.get("corrected_text", "").strip()
    if not content:
        return jsonify({'status': 'no content'}), 400
    return jsonify({'content': content})

# ---------- Main ----------
if __name__ == '__main__':
    app.run(debug=True)
