def solve(lines):
    maxscore, ver, hor = 0, len(lines), len(lines[0])
    for x in range(hor):
        if x == 0 or x == hor-1:
            continue
        for y in range(ver):
            if y == 0 or y == ver-1:
                continue
            w = lines[y][:x]
            e = lines[y][x+1:]
            n = [ lines[i][x] for i in range(0,y)]
            s = [ lines[i][x] for i in range(y+1,ver)]
            w.reverse()
            n.reverse()
            n = list(map(lambda i: i >= lines[y][x] ,n))
            s = list(map(lambda i: i >= lines[y][x] ,s))
            w = list(map(lambda i: i >= lines[y][x] ,w))
            e = list(map(lambda i: i >= lines[y][x] ,e))



            n = len(n) if True not in n else n.index(True)+1
            s = len(s) if True not in s else s.index(True)+1
            w = len(w) if True not in w else w.index(True)+1
            e = len(e) if True not in e else e.index(True)+1
            maxscore = max(maxscore, n*s*w*e)



    return maxscore

if __name__ == '__main__':
    lines = []
    with open('8.txt') as f:
        for line in f.readlines():
            line = line.strip()
            lines.append([int(x) for x in line])
    print(solve(lines))
