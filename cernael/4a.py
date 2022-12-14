import re
def solve(lines):

    return len(
        list(
            filter(
                fully_contains,
                map(
                    lambda x: re.split(',|-', x),
                    lines
                )
            )
        )
    )

def fully_contains(x):
    s1 = set(range(int(x[0]),int(x[1])+1))
    s2 = set(range(int(x[2]),int(x[3])+1))
    return s1 >= s2 or s1 <= s2

if __name__ == '__main__':
    lines = []
    with open('4.txt') as f:
        for line in f.readlines():
            line = line.strip()
            lines.append(line)
    print(solve(lines))
