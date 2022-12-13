def solve(lines):
    c, x, screen = 0, 1, [[]]
    for line in lines:
        screen[-1].append('#' if x-1 <= c%40 <= x+1 else '.')
        c += 1
        if c % 40 == 0:
            screen.append([])
        if len(line) == 4:
            continue
        val = int(line[5:])
        if val:
            screen[-1].append('#' if x-1 <= c%40 <= x+1 else '.')
            c += 1
            if c % 40 == 0:
                screen.append([])
            x += val
    return screen

if __name__ == '__main__':
    lines = []
    with open('10.txt') as f:
        for line in f.readlines():
            line = line.strip()
            lines.append(line)
    for l in solve(lines):
        #print(l)
        print(''.join(l))
