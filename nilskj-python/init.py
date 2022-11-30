# Initializer from @estomagordo https://github.com/estomagordo
from os import path
from sys import argv

dayfile = (
    lambda day: f"""
def solve(lines):
    pass

def main():
    lines = []
    with open('{day}.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)

if __name__ == '__main__':
    print(main())
"""
)

if __name__ == "__main__":
    day = argv[1]

    daya = f"day{day}a.py"
    dayb = f"day{day}b.py"
    inp = f"{day}.txt"

    if not path.isfile(daya):
        with open(daya, "w") as g:
            g.write(dayfile(day))
    if not path.isfile(dayb):
        with open(dayb, "w") as g:
            g.write(dayfile(day))
    if not path.isfile(inp):
        with open(inp, "w") as g:
            g.write("")
