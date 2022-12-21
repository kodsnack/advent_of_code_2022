def solve(lines):
    res = 0
    for l in lines:
        (a,b) = (l[0], l[2])
        if b == "X":
            res = res + 1
            if a == "A":
                res = res + 3
            elif a == 'B':
                res = res + 0
            elif a == 'C':
                res = res + 6
        elif b == 'Y':
            res = res + 2
            if a == "A":
                res = res + 6
            elif a == 'B':
                res = res + 3
            elif a == 'C':
                res = res + 0
        elif b == 'Z':
            res = res + 3
            if a == "A":
                res = res + 0
            elif a == 'B':
                res = res + 6
            elif a == 'C':
                res = res + 3
    return res

if __name__ == '__main__':
    lines = []
    with open('2.txt') as f:
        for line in f.readlines():
            line.strip()
            lines.append(line)
    print(solve(lines))
