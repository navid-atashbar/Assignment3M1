"""
Inverted Index with disk-based offloading for large-scale indexing
"""
import json
import os
from collections import defaultdict
from typing import Dict, List, Set
import pickle
#test

class InvertedIndex:
    """
    Inverted index that offloads to disk during construction
    Designed for the developer option with 56K+ documents
    """
    
    def __init__(self, index_dir: str = "index_data", memory_threshold: int = 5000): #changed to 5000 from 10k can cahnge later
        """
        Args:
            index_dir: directory to store index files
            memory_threshold: number of documents to process before offloading
        """
        self.index_dir = index_dir
        self.memory_threshold = memory_threshold
        
        # In-memory index: {term: {doc_id: {'tf': count, 'important': bool}}}
        self.index = defaultdict(lambda: defaultdict(dict))
        
        # Document counter and URL mapping
        self.doc_id = 0
        self.url_map = {}  # {doc_id: url}
        
        # Track partial indexes
        self.partial_index_count = 0
        self.partial_indexes = []
        
        # Statistics
        self.total_docs = 0
        self.unique_tokens = 0
        self.size_on_disk = 0
        
        # Create index directory
        os.makedirs(self.index_dir, exist_ok=True)
    
    def add_document(self, url: str, tokens: List[str], important_tokens: List[str]):
        """
        Add a document to the index
        Args:
            url: document URL
            tokens: list of stemmed tokens from document
            important_tokens: list of stemmed tokens from important elements
        """
        # Assign document ID
        current_doc_id = self.doc_id
        self.url_map[current_doc_id] = url
        self.doc_id += 1
        self.total_docs += 1
        
        # Count term frequencies for normal tokens
        token_freq = defaultdict(int)
        for token in tokens:
            token_freq[token] += 1
            # self.unique_tokens.add(token)
        
        # Track which tokens are important
        important_set = set(important_tokens)
        
        # Add to inverted index
        for token, freq in token_freq.items():
            self.index[token][current_doc_id] = {
                'tf': freq,
                'important': token in important_set
            }
        
        # Check if we need to offload to disk
        if self.total_docs % self.memory_threshold == 0:
            self._offload_to_disk()
    
    def _offload_to_disk(self):
        """
        Offload current in-memory index to disk as a partial index
        This is required for the developer option (at least 3 times)
        """
        if not self.index:
            return
        
        partial_filename = os.path.join(
            self.index_dir, 
            f"partial_index_{self.partial_index_count}.json"
        )
        
        print(f"Offloading partial index {self.partial_index_count} to disk "
              f"(docs processed: {self.total_docs})...")
        
        # Convert defaultdict to regular dict for JSON serialization
        index_to_save = {}
        for term, postings in self.index.items():
            index_to_save[term] = dict(postings)
        
        # Save to disk
        with open(partial_filename, 'w', encoding='utf-8') as f:
            json.dump(index_to_save, f)
        
        self.partial_indexes.append(partial_filename)
        self.partial_index_count += 1
        
        # Clear in-memory index
        self.index.clear()
        print(f"Partial index {self.partial_index_count - 1} saved. Memory cleared.")
    
    def finalize(self):
        """
        Finalize the index: offload any remaining data and merge all partial indexes
        """
        # Offload any remaining data
        if self.index:
            self._offload_to_disk()
        
        # Save URL mapping
        url_map_file = os.path.join(self.index_dir, "url_map.json")
        with open(url_map_file, 'w', encoding='utf-8') as f:
            json.dump(self.url_map, f)
        
        print(f"\nMerging {len(self.partial_indexes)} partial indexes...")
        
        # Merge all partial indexes
        if len(self.partial_indexes) > 0:
            self._merge_partial_indexes()
        
        # Save statistics
        self._save_statistics()
        
        # print(f"Index finalized!")
        # print(f"Total documents indexed: {self.total_docs}")
        # print(f"Unique tokens: {self.unique_tokens}")
    
    def _merge_partial_indexes(self):
        """
        Merge all partial indexes into a final index
        """
       #CHANGE
        merged = {}
        for partial_filename in self.partial_indexes:
            print(f"Merging partial index {partial_filename}")
            with open(partial_filename, 'r', encoding='utf-8') as f:
                partial_json = json.load(f)
            for term,posting in partial_json.items():
                if term in merged:
                    merged[term].update(posting)
                else:
                    merged[term] = posting
            del partial_json
        final_file = os.path.join(self.index_dir, "final_index.json")
        print(f"Merging final index {final_file}")
        with open(final_file, 'w', encoding='utf-8') as f:
            json.dump(merged, f, indent=2)
        del merged
        for partial_filename in self.partial_indexes:
            try:
                os.remove(partial_filename)
                print(f"removed partial index {partial_filename}")

            except:
                pass
    def _save_statistics(self):
        """
        Save statistics for the report
        """
        final_index = os.path.join(self.index_dir, "final_index.json")
        with open(final_index, 'r', encoding='utf-8') as f:
            len_final_json = json.load(f)
        count_tokens = len(len_final_json)
        del len_final_json
        stats = {
            'num_documents': self.total_docs,
            'num_unique_tokens': count_tokens,
            'num_partial_indexes_created': self.partial_index_count,
            'index_size_kb': self.get_index_size_kb()
        }
        
        stats_file = os.path.join(self.index_dir, "statistics.json")
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)
        
        print(f"\nStatistics saved to {stats_file}")
    
    def get_index_size_kb(self):
        """
        Calculate total size of index on disk in KB
        """
        total_size = 0
        for filename in os.listdir(self.index_dir):
            filepath = os.path.join(self.index_dir, filename)
            if os.path.isfile(filepath):
                total_size += os.path.getsize(filepath)
        
        return total_size / 1024  # Convert to KB
