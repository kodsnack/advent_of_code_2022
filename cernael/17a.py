def solve(line):
    rocks = [
        {(0,0),(1,0),(2,0),(3,0)},
        {(1,0),(0,1),(1,1),(2,1),(1,2)},
        {(0,0),(1,0),(2,0),(2,1),(2,2)},
        {(0,0),(0,1),(0,2),(0,3)},
        {(0,0),(1,0),(0,1),(1,1)},
    ]
    t, n, tower = 0, 0, []
    while n < 2022:
        x,y = 2,3
        rock = {(x+p[0],y+p[1]+len(tower)) for p in rocks[ n % 5 ]}
        # grow tower
        tower.extend([[' ' for _ in range(7)] for _ in range(10)])
        n += 1
        while True:
            blow = 1 if line[t % len(line)] == '>' else -1
            t += 1
            for r in rock:
                if blow == -1 and (r[0] == 0 or tower[r[1]][r[0]-1] != ' '):
                    blow = False
                    break
                elif blow == 1 and (r[0] == 6 or tower[r[1]][r[0]+1] != ' '):
                    blow = False
                    break
            if blow:
                rock = {(p[0]+blow,p[1]) for p in rock}
            fall = 1
            for r in rock:
                if tower[r[1]-fall][r[0]] != ' ' or r[1] == 0:
                    fall = False
                    break
            if fall:
                rock = {(p[0],p[1]-fall) for p in rock}
            else:
                for r in rock:
                    tower[r[1]][r[0]] = '#'
                break
        # shrink tower
        while ''.join(tower[-1]) == '       ':
            tower.pop()
    return len(tower)

if __name__ == '__main__':
    lines = []
    with open('17.txt') as f:
        for line in f.readlines():
            line = line.strip()
            lines.append(line)
    print(solve(lines[0]))
