def solve(lines):
    res = 0
    for l in lines:
        (a,b) = (l[0], l[2])
        if b == "X": # lose
            res = res + 0
            if a == "A":
                res = res + 3
            elif a == 'B':
                res = res + 1
            elif a == 'C':
                res = res + 2
        elif b == 'Y': # draw
            res = res + 3
            if a == "A":
                res = res + 1
            elif a == 'B':
                res = res + 2
            elif a == 'C':
                res = res + 3
        elif b == 'Z': # win
            res = res + 6
            if a == "A":
                res = res + 2
            elif a == 'B':
                res = res + 3
            elif a == 'C':
                res = res + 1
    return res

if __name__ == '__main__':
    lines = []
    with open('2.txt') as f:
        for line in f.readlines():
            line.strip()
            lines.append(line)
    print(solve(lines))
