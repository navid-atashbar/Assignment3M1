from searcher import Searcher
import time

def run():
    start_time = time.time()
    searcher = Searcher()
    print(f"Load time {time.time() - start_time} seconds")
    print("Type exit to quit\n")
    while True:
        query = input("Enter query (or 'exit'): ").strip()
        if query.lower() == "exit":
            break
        if not query:
            print("enter valid query\n")
            continue
        new_start_time = time.time()
        lists = searcher.search(query)
        url = searcher.id_to_links(lists)
        search_time = time.time() - new_start_time
        if not url:
            print("No restults found \n")
            continue
        print(f"\nSearch completed in {search_time:.4f} seconds")
        i = 0
        for n in url:
            if i >= 5:
                break
            print(f"{i + 1}. {n}")
            i += 1

        print()

if __name__ == "__main__":
    run()