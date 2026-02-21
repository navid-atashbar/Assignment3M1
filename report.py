"""
generates da report
"""
import json

from pathlib import Path
def generate(output):
    out = (output)
    true_path = Path(out) / "statistics.json"
    with open(true_path) as f:
        loaded = json.load(f)
        report = f"""
-------------------------------------------
         Assignment 3: M1 Report
-------------------------------------------
Group Members: 
    Navid Atashbar
    Tawann Alvarez
    Ryan Sahyoun

Data: 

    Number of Indexed docs            - {loaded['num_documents']}
    Number of Unique tokens           - {loaded['num_unique_tokens']}
    Number of Partial Indexes Created - {loaded['num_partial_indexes_created']}
    Total index size (KB)             - {loaded['index_size_kb']}
-------------------------------------------"""

    report_path = Path(out) / "report.txt"
    with open(report_path, "w") as f:
        f.write(report)
    print("Saved the report!")

if __name__ == "__main__":
    generate('./index_data')