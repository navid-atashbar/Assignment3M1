import json
from nltk.stem import PorterStemmer

class Searcher:
    def __init__(self, index_dir: str = "index_data"):
        # self.index_dir =self._loader_index(index_dir)
        self.url_map = self._load_mapper(index_dir)
        self.lexicon = self._loader_lexicon(index_dir)
        self.index_file = open(f"{index_dir}/index.txt", "r")
    def _loader_lexicon(self, index_dir: str):
        with open(f"{index_dir}/lexicon.json", "r") as f:
            return json.load(f)
    def _posting(self, word):
        if word not in self.lexicon:
            return {}
        offset = self.lexicon[word]
        self.index_file.seek(offset)
        line = self.index_file.readline()
        return json.loads(line)
    # def _loader_index(self, filename: str):
    #     with open(f"{filename}/final_index.json", "r") as f:
    #         return json.load(f)
    def _load_mapper(self, filename: str):
        with open(f"{filename}/url_map.json", "r") as f:
            return json.load(f)
    def search(self, query: str, top_x=5):
        #THIS IS WHAT WE NEED TO DO
        #get the smallest length index so its fastest
        string_split_lower = [word.lower() for word in query.split()]
        lowest_word = ""
        len_lowest = 9999999999999999999999
        for words in string_split_lower:
            stemmer = PorterStemmer()
            new_word = stemmer.stem(words)
            post = self._posting(new_word)
            if post and len(post) < len_lowest:
                lowest_word = new_word
                len_lowest = len(post)
        if not lowest_word:
            return []
        #THIS HOLDS THE SET OF DOCS THAT HAVE THE WORD
        searched_first = set(self._posting(lowest_word).keys())
        for words in string_split_lower:
            stemmer = PorterStemmer()
            new_word = stemmer.stem(words)
            if new_word == lowest_word:
                continue
            post = self._posting(new_word)
            if not post:
                return []
            searched_first &= set(post.keys())
            print(len(searched_first))
        return list(searched_first)[:top_x]

    def id_to_links(self, list_ids: list):
        links = []
        for doc_id in list_ids:
            links.append(self.url_map[doc_id])
        return links
