from functools import cmp_to_key

def solve(lines):
    lines.extend([[[2]],[[6]]])
    for l in lines: print(l)
    [lines[0], lines[1]].sort(key=cmp_to_key(compare))
    return

def compare(l,r):
    if isinstance(l, int) and isinstance(r, int):
        if l == r:
            return 0
        elif l < r:
            return -1
        return 1
    if isinstance(l, int) and isinstance(r, list):
        return compare([l], r)
    if isinstance(l, list) and isinstance(r, int):
        return compare(l, [r])
    if isinstance(l, list) and isinstance(r, list):
        res = list(filter(lambda x:x != 0, map(lambda z: compare(z[0],z[1]),zip(l,r))))
        if len(res):
            r = res[0]
            if r == 1:
                return 1
            elif r == -1:
                return -1
            else:
                return 0
        if len(l) == len(r):
            return 0
        elif len(l) < len(r):
            return -1
        return 1



if __name__ == '__main__':
    lines = []
    with open('13test.txt') as f:
        for line in f.readlines():
            line = line.strip()
            if line: lines.append(line)
    print(solve(lines))
