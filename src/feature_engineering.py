import re
import numpy as np
import math
from sklearn.base import BaseEstimator, TransformerMixin
from bs4 import BeautifulSoup
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string

# Download required NLTK resources
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
    nltk.download('stopwords')

class TextPreprocessor(BaseEstimator, TransformerMixin):
    """
    Cleans HTML, lowercases, removes punctuation, lemmatizes, and removes stopwords.
    """
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        cleaned_X = []
        for text in X:
            # 1. Remove HTML
            text = BeautifulSoup(text, "html.parser").get_text(separator=" ")
            # 2. Lowercase
            text = text.lower()
            # 3. Remove punctuation
            text = text.translate(str.maketrans('', '', string.punctuation))
            # 4. Tokenize and lemmatize
            words = text.split()
            words = [self.lemmatizer.lemmatize(w) for w in words if w not in self.stop_words]
            cleaned_X.append(" ".join(words))
        return cleaned_X


class HandcraftedFeatureExtractor(BaseEstimator, TransformerMixin):
    """
    Extracts handcrafted dense features from raw email text.
    """
    def __init__(self):
        self.suspicious_exts = ['.exe', '.zip', '.scr', '.bat', '.js']
        self.urgent_words = ['urgent', 'immediate', 'action', 'required', 'suspended', 'alert', 'verify', 'account']
        self.brands = ['paypal', 'microsoft', 'google', 'amazon', 'bank', 'apple', 'netflix', 'chase', 'wellsfargo']
        self.shorteners = ['bit.ly', 'goo.gl', 't.co', 'tinyurl', 'ow.ly', 'is.gd']
        
    def fit(self, X, y=None):
        return self
        
    def _entropy(self, string):
        prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
        return entropy
        
    def transform(self, X):
        features = []
        for text in X:
            text_str = str(text)
            text_lower = text_str.lower()
            
            # URL extraction
            urls = re.findall(r'(https?://[^\s]+)', text_lower)
            num_urls = len(urls)
            
            # HTML tags
            num_html = len(re.findall(r'<[^>]+>', text_str))
            
            # Special chars
            num_exclamation = text_str.count('!')
            num_special = sum([text_str.count(c) for c in '@#$%^&*'])
            
            # Uppercase ratio
            num_upper = sum(1 for c in text_str if c.isupper())
            upper_ratio = num_upper / max(len(text_str), 1)
            
            # Suspicious attachments
            has_suspicious_att = int(any(ext in text_lower for ext in self.suspicious_exts))
            
            # Urgency
            urgency_score = sum(text_lower.count(w) for w in self.urgent_words)
            
            # Brand impersonation
            brand_impersonation = sum(text_lower.count(b) for b in self.brands)
            
            # IP based URL
            has_ip_url = int(any(re.search(r'\d+\.\d+\.\d+\.\d+', u) for u in urls))
            
            # Shortened URL
            has_shortened = int(any(s in u for u in urls for s in self.shorteners))
            
            # Average URL entropy
            url_entropy = np.mean([self._entropy(u) for u in urls]) if urls else 0.0
            
            features.append([
                num_urls, num_html, num_exclamation, num_special, upper_ratio,
                has_suspicious_att, urgency_score, brand_impersonation, has_ip_url,
                has_shortened, url_entropy
            ])
            
        return np.array(features)
