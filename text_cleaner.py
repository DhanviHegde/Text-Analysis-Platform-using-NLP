import re
import spacy

def clean_text(text):
    text = text.lower()   # Lowercase conversion
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)  # URL removal
    text = re.sub(r'<.*?>', '', text)  # HTML tag removal
    text = re.sub(r'[^a-z\s]', '', text)  # Special character removal
    text = re.sub(r'\s+', ' ', text).strip()  # Extra whitespace removal
    text = re.sub(r'\S+@\S+\.\S+', '', text)  # Email removal
    text = re.sub(r'[^\w\s]', '', text)  # Punctuation removal
    text = re.sub(r'(.)\1{2,}', r'\1', text)  # Repeated characters
    text = re.sub(r'#', '', text)  # Hashtags
    text = re.sub(r'@\w+', '', text)  # Mentions
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Non-ASCII (emoji, foreign chars)
    return text

def clean_text_spacy(text):
    nlp= spacy.load("en_core_web_sm")
    doc= nlp(text)
    word=[]
    for token in doc:
        if not token.is_stop and not token.is_punct:
            word.append(token.lemma_)
    return word

