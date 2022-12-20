def solve(line):
    n, h = 0, []

    for c in line:
        n += 1
        h.append(c)
        if len(h) == 4:
            ret = True
            for i in range(1, len(h)):
                if h[i-1] in h[i:]:
                    ret = False
                    break
            if ret:
                return n
            h.pop(0)

if __name__ == '__main__':
    lines = []
    with open('6.txt') as f:
        for line in f.readlines():
            line.strip()
            lines.append(line)

    print(solve(lines[0]))
