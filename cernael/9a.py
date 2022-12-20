def solve(lines):
    hx, hy, tx, ty = 0,0,0,0
    tailpos = {(0,0)}
    for l in lines:
        d, n = l.split()
        for _ in range(int(n)):
            if d == 'R':
                hx += 1
            elif d == 'L':
                hx -= 1
            elif d == 'U':
                hy += 1
            elif d == 'D':
                hy -= 1
            
            # check move tail
            if abs(hx-tx) > 1 or abs(hy-ty) > 1:
                if hx > tx: tx += 1
                elif hx < tx: tx -= 1
                if hy > ty: ty += 1
                elif hy < ty: ty -= 1
                tailpos.add((tx,ty))
    
    return len(tailpos)

if __name__ == '__main__':
    lines = []
    with open('9.txt') as f:
        for line in f.readlines():
            line = line.strip()
            lines.append(line)
    print(solve(lines))
