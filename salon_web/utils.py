import random
import string

def generate_referral_code():
    return ''.join(random.choices(string.digits, k=6))

#ML modeli
# ml_utils.py
from textblob import TextBlob

def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0.1:
        return 'positive'
    elif polarity < -0.1:
        return 'negative'
    else:
        return 'neutral'
