def solve(lines):
    res = [0,0,0]

    for bag in lines:
        cal = sum([int(item) for item in bag])
        if cal > res[0]:
            res.pop(0)
            res.append(cal)
            res.sort()
    return sum(res)


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