from user_interface import run
from convert import convert
from report import generate
import os
import indexer

INDEX_PATH = './index_data'
def main():
    if not os.path.exists("index_data/final_index.json"):
        indexer.build_index(data_dir="./DEV")
        generate(INDEX_PATH)
    if not os.path.exists("index_data/lexicon.json"):
        print("Converting...")
        convert()
        print("Success: converted successfully")
    print("Running...")
    run()


if __name__ == "__main__":
    main()

#