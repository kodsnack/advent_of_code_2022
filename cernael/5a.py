def solve(lines):
    crates, moves = [], []
    phase = True
    for l in lines:
        if l:
            if phase:
                crates.append(l)
            else:
                moves.append(l)
        else:
            phase = False

    crates = [[row[n:n+4].strip('[] ') for n in range(0, len(row), 4)] for row in crates]
    crates = {
        stack[0]: list(filter(lambda x: x, stack[1:]))
        for stack in [
            [
                crates[
                    len(crates)-r-1
                ][c]
                for r in range(len(crates))
            ]
            for c in range(len(crates[0]))
        ]
    }

    for m in moves:
        n, fr, to = m.split()[1::2]
        for _ in range(int(n)):
            crates[to].append(
                crates[fr].pop())

    return ''.join([crates[str(stack+1)][-1] for stack in range(len(crates.keys()))])

if __name__ == '__main__':
    lines = []
    with open('5.txt') as f:
        for line in f.readlines():
            line = line.strip('\n')
            lines.append(line)
    print(solve(lines))
