import json


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
        pass