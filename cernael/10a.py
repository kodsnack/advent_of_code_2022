def solve(lines):
    c, x, res = 0, 1, 0
    for line in lines:
        c += 1
        if c % 40 == 20:
            res += c*x
        if len(line) == 4:
            continue
        val = int(line[5:])
        if val:
            c += 1
            if c % 40 == 20:
                res += c*x
            x += val
    return res

if __name__ == '__main__':
    lines = []
    with open('10.txt') as f:
        for line in f.readlines():
            line = line.strip()
            lines.append(line)
    print(solve(lines))
