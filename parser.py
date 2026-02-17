"""
HTML Parser for extracting text and identifying important words
"""
import json
from bs4 import BeautifulSoup
from typing import Dict, List, Tuple

class HTMLParser:
    """Parses HTML content and extracts tokens with importance weights"""
    
    def __init__(self):
        # Tags that indicate important words
        self.important_tags = {'b', 'strong', 'h1', 'h2', 'h3', 'title'}
    
    def parse_json_file(self, filepath: str) -> Dict:
        """
        Parse a JSON file containing URL, content, and encoding
        Returns: dict with 'url' and 'content' keys
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"Error parsing {filepath}: {e}")
            return None
    
    def extract_text_with_importance(self, html_content: str) -> Tuple[List[str], List[str]]:
        """
        Extract text from HTML, separating normal and important words
        Returns: (normal_words, important_words)
        """
        if not html_content:
            return [], []
        
        try:
            soup = BeautifulSoup(html_content, 'lxml')
        except:
            # Fallback to html.parser if lxml fails
            soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extract important words (from bold, headings, title tags)
        important_words = []
        for tag in soup.find_all(self.important_tags):
            text = tag.get_text(separator=' ', strip=True)
            important_words.extend(text.split())
        
        # Extract all text
        all_text = soup.get_text(separator=' ', strip=True)
        all_words = all_text.split()
        
        # Normal words are all words (we'll handle importance by boosting in indexer)
        return all_words, important_words
    
    def parse_document(self, filepath: str) -> Tuple[str, List[str], List[str]]:
        """
        Parse a document and return URL and words
        Returns: (url, normal_words, important_words)
        """
        data = self.parse_json_file(filepath)
        if not data:
            return None, [], []
        
        url = data.get('url', '')
        html_content = data.get('content', '')
        
        normal_words, important_words = self.extract_text_with_importance(html_content)
        
        return url, normal_words, important_words
