def solve(line):
    rocks = [
        {(0,0),(1,0),(2,0),(3,0)},
        {(1,0),(0,1),(1,1),(2,1),(1,2)},
        {(0,0),(1,0),(2,0),(2,1),(2,2)},
        {(0,0),(0,1),(0,2),(0,3)},
        {(0,0),(1,0),(0,1),(1,1)},
    ]
    tick, n, tower, cycles, heights = 0, 0, [], [], []
    k, c = ord('a'), False
    while n < 20220:
        heights.append(len(tower))
        if n % 5 == 0 and tick % len(line) == 0:
            if len(cycles):
                pass
                # TODO: detect cycle; compare latest bunch to previous bunch of tower lines.
            cycles.append(tick, len(tower))
        bottom = len(tower)
        x,y,m = 2,3,chr(k)
        rock = {(x+p[0],y+p[1]+len(tower)) for p in rocks[ n % 5 ]}
        # grow tower
        tower.extend([[' ' for _ in range(7)] for _ in range(10)])
        while True:
            # blow
            #print('s', rock)
            blow = 1 if line[tick % len(line)] == '>' else -1
            tick += 1
            if tick % len(line) *5 == 0:
                k += 1
                m = chr(k)
                c = True
                print(tick,n,rock,len(tower), m,k)
            for r in rock:
                # these can be optimised to a single check, albeit less readable
                if blow == -1 and (r[0] == 0 or tower[r[1]][r[0]-1] != ' '):
                    blow = False
                    break
                elif blow == 1 and (r[0] == 6 or tower[r[1]][r[0]+1] != ' '):
                    blow = False
                    break
            if blow:
                rock = {(p[0]+blow,p[1]) for p in rock}
            #print('b',rock)
            # fall
            fall = 1
            for r in rock:
                if tower[r[1]-fall][r[0]] != ' ' or r[1] == 0:
                    fall = False
                    break
            if fall:
                rock = {(p[0],p[1]-fall) for p in rock}
            else:
                for r in rock:
                    if c:
                        print(m)
                        c = False
                    tower[r[1]][r[0]] = m
                    if bottom > r[1]:
                        bottom = r[1]
                break
        while ''.join(tower[-1]) == '       ':
            tower.pop()
        n += 1
        #if len(line)*5 == n-5:
        #    for l in list(reversed(tower))[:20]: print(l)
        #    print(len(tower),n,t)

    #for l in list(reversed(tower))[:100]: print(l)
    print(len(line), tick,n)
    occs = {c: [None,None] for c in 'abcdefghijklmnopq'}
    for i in range(len(tower)):
        for k,v in occs.items():
            if k in tower[i]:
                v[1] = i
                if v[0] == None:
                    v[0] = i
    for k,v in occs.items(): print(k, v, v[1]-v[0])
    return occs

if __name__ == '__main__':
    lines = []
    with open('17.txt') as f:
        for line in f.readlines():
            line = line.strip()
            lines.append(line)
    print(solve(lines[0]))
