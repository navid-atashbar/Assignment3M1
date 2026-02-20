
"""
Main script for building the inverted index from DEV folder
Usage: python main.py
"""

import os
import time
from parser import HTMLParser
from tokenizer import Tokenizer
from inverted_index import InvertedIndex

start_time = time.time()
def build_index(data_dir: str = "DEV", index_dir: str = "index_data"):
    """
    Walk through the DEV folder and index all documents.
    The DEV folder contains subfolders per domain (e.g. aiclub_ics_uci_edu/),
    each containing hash-named JSON files with no extension.
    """
    parser = HTMLParser()
    tokenizer = Tokenizer()
    index = InvertedIndex(index_dir=index_dir, memory_threshold=10000)

    print(f"Starting indexing from '{data_dir}'...\n")

    # Collect all files recursively
    all_files = []
    for root, dirs, files in os.walk(data_dir):
        for filename in files:
            all_files.append(os.path.join(root, filename))

    total_files = len(all_files)
    print(f"Found {total_files} files to index.\n")

    for i, filepath in enumerate(all_files):
        # Parse the document
        url, normal_words, important_words = parser.parse_document(filepath)

        # Skip invalid or empty documents
        if not url or not normal_words:
            continue

        # Tokenize and stem
        tokens = tokenizer.tokenize_and_stem_words(normal_words)
        important_tokens = tokenizer.tokenize_and_stem_words(important_words)

        # Skip if no valid tokens
        if not tokens:
            continue

        # Add to index
        index.add_document(url, tokens, important_tokens)

        # Progress update every 1000 docs
        if (i + 1) % 1000 == 0:
            print(f"Processed {i + 1}/{total_files} files...")

    # Finalize: flush remaining memory, merge partials, save stats
    print("\nFinalizing index...")
    index.finalize()

    # Print index size
    size_kb = index.get_index_size_kb()
    print(f"\n--- Index Summary ---")
    print(f"Documents indexed : {index.total_docs}")
    print(f"Unique tokens     : {len(index.unique_tokens)}")
    print(f"Index size on disk: {size_kb:.2f} KB")
    print(f"Index saved to    : {os.path.abspath(index_dir)}/")
    print(f"Time took building : {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    build_index(data_dir="./DEV")