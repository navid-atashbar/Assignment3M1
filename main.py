
import indexer
from report import generate
INDEX_PATH = '../index_data'

def main():
    indexer.build_index(data_dir="./DEV")
    generate(INDEX_PATH)


if __name__ == "__main__":
    main()


