def solve(lines):
    rope = [[0,0] for _ in range(10)]
    tailpos = {(0,0)}
    for l in lines:
        d, n = l.split()
        for _ in range(int(n)):
            if d == 'R':
                rope[0][0] += 1
            elif d == 'L':
                rope[0][0] -= 1
            elif d == 'U':
                rope[0][1] += 1
            elif d == 'D':
                rope[0][1] -= 1

            for i in range(len(rope)-1):
                if (abs(rope[i][0]-rope[i+1][0]) > 1
                 or abs(rope[i][1]-rope[i+1][1]) > 1):
                    if rope[i][0] > rope[i+1][0]:
                        rope[i+1][0] += 1
                    elif rope[i][0] < rope[i+1][0]:
                        rope[i+1][0] -= 1

                    if rope[i][1] > rope[i+1][1]:
                        rope[i+1][1] += 1
                    elif rope[i][1] < rope[i+1][1]:
                        rope[i+1][1] -= 1

            tailpos.add(tuple(rope[-1]))

    return len(tailpos)

if __name__ == '__main__':
    lines = []
    with open('9.txt') as f:
        for line in f.readlines():
            line = line.strip()
            lines.append(line)
    print(solve(lines))
