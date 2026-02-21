
"""
Group Members: 
    Navid Atashbar 58919360
    Tawann Alvarez 44662328
    Ryan Sahyoun 22183231
Main script for building the inverted index from DEV folder
"""
import json
import os
import time
from parser import HTMLParser
from tokenizer import Tokenizer
from inverted_index import InvertedIndex
start_time = time.time()

def build_index(data_dir: str = "DEV", index_dir: str = "index_data"):
    """
    BUILD IT ALL FROM THE OTHER FILES
    """
    #GET All the stuff and intiialzie
    parser = HTMLParser()
    tokenizer = Tokenizer()
    index = InvertedIndex(index_dir=index_dir, memory_threshold=5000)

    print(f"Starting indexing from '{data_dir}'...\n")

    # get all files
    all_files = []
    for root, directs, files in os.walk(data_dir): #returns 3 directs is useless
        for filename in files:
            all_files.append(os.path.join(root, filename))

    total_files = len(all_files)
    print(f"Found {total_files} files to index...\n")
    i = 0
    for filepath in all_files:
        # Parse the document
        url, normal_words, important_words = parser.parse_document(filepath)
        if not url or not normal_words:
            continue
        # Tokenize and stem
        tokens = tokenizer.tokenize_and_stem_words(normal_words)
        important_tokens = tokenizer.tokenize_and_stem_words(important_words)
        if not tokens:
            continue
        index.add_document(url, tokens, important_tokens)
        # Progress update EVERY x docs
        if (i + 1) % 2500 == 0:
            print(f"Processed {i + 1}/{total_files} files...")
        i +=1

    print("\nFininishing index...")
    time_taken = time.time()
    index.finalize()
    total_time_taken = time.time() - start_time
    merging_time = time.time() - time_taken
    # Print data
    size_kb = index.get_index_size_kb()
    print(f"\n Summary DONE!")
    print(f"Documents indexed : {index.total_docs}")
    print(f"Unique tokens     : {index.unique_tokens}")
    print(f"Index size on disk: {size_kb:.2f} KB")
    print(f"Index saved to    : {os.path.abspath(index_dir)}/")
    print(f"Time took to run program : {time.time() - start_time:.2f} seconds")
    #Write
    with open("./index_data/statistics.json", "r") as f:
        stats = json.load(f)
    stats["time_taken"]= total_time_taken
    stats["Merge index time"] = merging_time
    with open("./index_data/statistics.json", "w") as f:
        json.dump(stats, f,indent=2)

if __name__ == "__main__":
    build_index(data_dir="./DEV")