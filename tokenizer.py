"""
Tokenizer for processing text into tokens with stemming
"""
import re
from nltk.stem import PorterStemmer

class Tokenizer:
    """Handles tokenization and stemming of text"""
    
    def __init__(self):
        self.stemmer = PorterStemmer()
        # Pattern to match alphanumeric sequences
        self.token_pattern = re.compile(r'[a-zA-Z0-9]+')
    
    def tokenize(self, text: str) -> list:
        """
        Extract alphanumeric tokens from text
        Args:
            text: raw text string
        Returns:
            list of tokens (lowercase, no stemming yet)
        """
        if not text:
            return []
        
        # Extract all alphanumeric sequences
        tokens = self.token_pattern.findall(text)
        
        # Convert to lowercase
        tokens = [token.lower() for token in tokens]
        
        return tokens
    
    def tokenize_and_stem(self, text: str) -> list:
        """
        Extract and stem tokens from text
        Args:
            text: raw text string
        Returns:
            list of stemmed tokens
        """
        tokens = self.tokenize(text)
        
        # Apply stemming
        stemmed_tokens = [self.stemmer.stem(token) for token in tokens]
        
        return stemmed_tokens
    
    def tokenize_words(self, words: list) -> list:
        """
        Tokenize a list of words (from parser)
        Args:
            words: list of word strings
        Returns:
            list of tokens
        """
        tokens = []
        for word in words:
            tokens.extend(self.tokenize(word))
        return tokens
    
    def tokenize_and_stem_words(self, words: list) -> list:
        """
        Tokenize and stem a list of words (from parser)
        Args:
            words: list of word strings
        Returns:
            list of stemmed tokens
        """
        tokens = []
        for word in words:
            word_tokens = self.tokenize(word)
            stemmed = [self.stemmer.stem(token) for token in word_tokens]
            tokens.extend(stemmed)
        return tokens
