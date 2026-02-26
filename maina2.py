from searcher import Searcher
import time

def main():

    searcher = Searcher()
    start_time = time.time()
    lists = searcher.search("artificial intelligence")
    print(f"Load time {time.time() - start_time} seconds")
    new_start_time = time.time()
    print(searcher.id_to_links(lists))
    print(f"Search time {time.time() - new_start_time} seconds")
    print(f"Took {time.time() - start_time} seconds")


if __name__ == "__main__":
    main()

