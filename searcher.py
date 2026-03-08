import json
from nltk.stem import PorterStemmer
import math
import re

class Searcher:
    def __init__(self, index_dir: str = "index_data"):
        # self.index_dir =self._loader_index(index_dir)
        self.url_map = self._load_mapper(index_dir)
        self.lexicon = self._loader_lexicon(index_dir)
        self.index_file = open(f"{index_dir}/index.txt", "r")
        self.stemmer = PorterStemmer()
        with open(f"{index_dir}/statistics.json", "r") as f:
            self.statistics = json.load(f)
        self.total_n = self.statistics["num_documents"]
        
        # M3 Enhancement: Stop words and query expansion
        self.stop_words = {
            'uci', 'ics', 'university', 'california', 'irvine',
            'information', 'computer', 'science', 'page', 'web',
            'https', 'http', 'www', 'edu', 'html'
        }
        self.query_expansions = {
            'ai': ['ai', 'artificial', 'intelligence'],
            'ml': ['ml', 'machine', 'learning'],
            'se': ['se', 'software', 'engineering'],
            'cs': ['cs', 'computer', 'science'],
            'hci': ['hci', 'human', 'computer', 'interaction'],
            'nlp': ['nlp', 'natural', 'language', 'processing'],
        }
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
    def _expand_query(self, query_terms):
        """M3 Enhancement: Expand acronyms to include full terms"""
        expanded = []
        for term in query_terms:
            term_lower = term.lower()
            expanded.append(term_lower)
            if term_lower in self.query_expansions:
                expanded.extend(self.query_expansions[term_lower])
        return list(set(expanded))
    
    def _normalize_course_code(self, query):
        """M3 Enhancement: Handle course codes like 'cs 122' -> 'cs122'"""
        pattern = r'(\w+)\s+(\d+)'
        matches = re.findall(pattern, query.lower())
        additional_terms = []
        for dept, num in matches:
            additional_terms.append(f"{dept}{num}")
        return additional_terms

    def search(self, query: str, top_x=5):
        # M3 Enhancement: Process query with expansions and normalization
        query_terms = query.lower().split()
        additional_terms = self._normalize_course_code(query)
        expanded_terms = self._expand_query(query_terms)
        all_terms = list(set(query_terms + additional_terms + expanded_terms))
        
        # Stem all terms
        string_split_lower = [self.stemmer.stem(term) for term in all_terms if term]
        original_stemmed = [self.stemmer.stem(t) for t in query_terms]
        
        if not string_split_lower:
            return []
        
        # Find smallest posting list for optimization
        lowest_word = ""
        len_lowest = 9999999999999999999999
        postings = {}
        
        for words in string_split_lower:
            post = self._posting(words)
            postings[words] = post
            if post and len(post) < len_lowest:
                lowest_word = words
                len_lowest = len(post)
        
        if not lowest_word or not postings[lowest_word]:
            return []
        
        # M3 Enhancement: Smart intersection - only require non-stop-words
        searched_first = set(postings[lowest_word].keys())
        required_terms = [t for t in original_stemmed if t not in self.stop_words]
        
        if required_terms:
            for words in required_terms:
                if words == lowest_word or words not in postings:
                    continue
                post = postings[words]
                if not post:
                    return []
                searched_first &= set(post.keys())
        
        # If intersection is empty, use union for stop-word-heavy queries
        if not searched_first:
            searched_first = set()
            for words in string_split_lower:
                if postings[words]:
                    searched_first.update(postings[words].keys())
        
        candidate_docs = searched_first
        scores = {}

        for words in string_split_lower:
            posts = postings[words]
            if not posts:
                continue
            
            df = len(posts)
            if df > 0:
                idf = math.log(self.total_n / df)
            else:
                idf = 0
            
            # M3 Enhancement: Down-weight stop words
            if words in self.stop_words:
                idf *= 0.3
            
            for docs_id in candidate_docs:
                if docs_id not in posts:
                    continue
                entry = posts[docs_id]
                
                if entry["tf"] > 0:
                    tf = 1 + math.log(entry["tf"])
                else:
                    tf = 0
                
                # M3 Enhancement: Increased importance boost
                if entry.get("important", False):
                    boosts = 2.5  # Changed from 2.0
                else:
                    boosts = 1.0
                
                # M3 Enhancement: Weight original query terms higher
                term_weight = 1.5 if words in original_stemmed else 1.0
                
                scores[docs_id] = scores.get(docs_id, 0) + (tf * boosts * idf * term_weight)
        
        # M3 Enhancement: Document length normalization
        for doc_id in scores:
            total_terms = sum(postings[w].get(doc_id, {}).get("tf", 0) for w in string_split_lower if postings[w])
            if total_terms > 100:
                length_penalty = 1.0 / (1.0 + math.log(total_terms / 100))
                scores[doc_id] *= length_penalty
        
        rank = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_x]
        res = []
        for doc_id, score in rank:
            url = self.url_map[doc_id]
            res.append((url, score))
        return res


    def id_to_links(self, list_ids: list):
        links = []
        for doc_id in list_ids:
            links.append(self.url_map[doc_id])
        return links
