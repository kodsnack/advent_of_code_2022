def solve(lines):
    visible, ver, hor = 0, len(lines), len(lines[0])
    for x in range(hor):
        if x == 0 or x == hor-1:
            visible += ver
        else:
            for y in range(ver):
                if y == 0 or y == ver-1:
                    visible += 1
                else:
                    n = max(lines[y][:x])
                    s = max(lines[y][x+1:])
                    w = max([lines [i][x] for i in range(0,y)])
                    e = max([lines [i][x] for i in range(y+1,ver)])

                    if min(n,s,w,e) < lines[y][x]:
                        visible += 1
    return visible

if __name__ == '__main__':
    lines = []
    with open('8.txt') as f:
        for line in f.readlines():
            line = line.strip()
            lines.append([int(x) for x in line])
    print(solve(lines))
