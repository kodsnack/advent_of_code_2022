def solve(lines):
    return max([
                sum([
                    int(item)
                    for item in bag
                ])
                for bag in lines
            ])


if __name__ == '__main__':
    lines = [[]]
    with open('1.txt') as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                lines.append([])
            else:
                lines[-1].append(line)
    print(solve(lines))
