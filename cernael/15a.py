import re
def solve(lines, n):
    cov = set()
    for l in lines:
        sx,sy,bx,by = [int(n) for n in re.split('[=:,]', l)[1::2]]
        mh = abs(sx-bx)+abs(sy-by)
        dy = abs(sy-n)
        rem = mh-dy
        [cov.add((n,y)) for y in range(sx - rem, sx + rem)]
    return len(cov)


if __name__ == '__main__':
    lines = []
    #t, n = '15test.txt', 10
    t, n = '15.txt', 2000000
    with open(t) as f:
        for line in f.readlines():
            line = line.strip()
            lines.append(line)
    print(solve(lines, n))
