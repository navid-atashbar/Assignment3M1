"""
Tokenizer for processing text into tokens with stemming
"""
import re
from nltk.stem import PorterStemmer

class Tokenizer:
    """
    Handles tokenization and stemming of text
    """
    
    def __init__(self):
        self.stemmer = PorterStemmer()
        # Pattern to match alphanumeric sequences (Assignment 3 spec: "all alphanumeric sequences")
        self.token_pattern = re.compile(r'[a-zA-Z0-9]+')
    
    def tokenize_and_stem_words(self, words: list) -> list:
        """
        Tokenize and stem a list of words from parser
        
        Process:
        - Extract alphanumeric sequences
        - Apply quality filters
        - Apply Porter stemming
        - No stop word removal (per assignment specs)
        
        Args:
            words: list of word strings from parser
        Returns:
            list of stemmed tokens
        """
        tokens = []
        
        for word in words:
            # Convert to lowercase
            word_clean = word.lower()
            
            # Extract alphanumeric sequences from this word
            alphanumeric_sequences = self.token_pattern.findall(word_clean)
            
            for token in alphanumeric_sequences:
                # Quality filters:
                
                # Skip if empty
                if not token:
                    continue
                
                # Skip if too short
                if len(token) < 3 and token not in ["am", "an", "as", "at", "be", "by", "do", "go", "he", "hi", "if", "in", "is", "it", "me", "my", "no", "of", "on", "or","ox", "so", "to", "up", "us", "we"]:
                    continue
                
                # Skip if digit-only
                if token.isdigit():
                    continue
                
                # Skip if too long (prevents weird strings/hashes)
                if len(token) > 30:
                    continue
                
                # Apply Porter stemming
                stemmed_token = self.stemmer.stem(token)
                
                tokens.append(stemmed_token)
        
        return tokens
