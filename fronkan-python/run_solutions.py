from pathlib import Path
import os

for p in Path().iterdir():
    if p.is_dir() and p.name.startswith("day"):
        solution = str(p / "solution.py")
        os.system(f"python {solution}")
        print("-------------------------------------")
