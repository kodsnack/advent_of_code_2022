class Loc:
    def __init__(self, x, y, h):
        self.x = x
        self.y = y
        self.dist_to_goal = -1
        self.special = h

        if h == 'S':
            self.h = ord('a')
        elif h == 'E':
            self.h = ord('z')
            self.dist_to_goal = 0
        else:
            self.h = ord(h)
            self.special = None

def solve(lines):
    terr, queue, starts, dists = [], [], [], []
    for y in range(len(lines)):
        terr.append([])
        for x in range(len(lines[0])):
            h = lines[y][x]
            terr[-1].append(Loc(x, y, h))
            if h == 'E':
                queue.append((x,y))
            elif h in ['S','a']:
                starts.append((x,y))

    while queue:
        p = queue.pop(0)
        p = terr[p[1]][p[0]]
        ns = [(p.x+n[0],p.y+n[1]) for n in [(0,1), (0,-1), (1,0), (-1,0)]]
        for n in ns:
            if ( 0 <= n[1] < len(terr) and 0 <= n[0] < len(terr[0])):
                n = terr[n[1]][n[0]]
                if ( p.h <= n.h + 1 and n.dist_to_goal == -1):
                    queue.append((n.x, n.y))
                    n.dist_to_goal = p.dist_to_goal + 1
                    if (n.x, n.y) in starts:
                        dists.append(n.dist_to_goal)
    return min(dists)

if __name__ == '__main__':
    lines = []
    with open('12.txt') as f:
        for line in f.readlines():
            line = line.strip()
            lines.append(line)
    print(solve(lines))
