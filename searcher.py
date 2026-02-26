import json
from nltk.stem import PorterStemmer

class Searcher:
    def __init__(self, index_dir: str = "index_data"):
        self.index_dir =self._loader_index(index_dir)
        self.url_map = self._load_mapper(index_dir)
    def _loader_index(self, filename: str):
        with open(f"{filename}/final_index.json", "r") as f:
            return json.load(f)
    def _load_mapper(self, filename: str):
        with open(f"{filename}/url_map.json", "r") as f:
            return json.load(f)
    def search(self, query: str, top_x=5):
        #THIS IS WHAT WE NEED TO DO
        #get the smallest length index so its fastest
        string_split_lower = [word.lower() for word in query.split("")]
        lowest_word = ""
        len_lowest = 9999999999999999999999
        for words in string_split_lower:
            stemmer = PorterStemmer()
            new_word = stemmer.stem(words)
            if len(self.index_dir[new_word]) < len_lowest:
                lowest_word = new_word
                len_lowest = len(self.index_dir[new_word])
        if not lowest_word:
            return []
        #THIS HOLDS THE SET OF DOCS THAT HAVE THE WORD
        searched_first = set(doc_id for doc_id, tf_idf in self.index_dir[lowest_word])
        for words in string_split_lower:
            stemmer = PorterStemmer()
            new_word = stemmer.stem(words)
            if new_word == lowest_word or word not in self.index_dir:
                continue
            docs_found = set(doc_id for doc_id, tf_idf in self.index_dir[new_word])
            searched_first &= docs_found
        return list(searched_first)[:top_x]

    def

