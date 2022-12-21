def solve(lines):
    res, i = 0, 0
    while lines:
        l = eval(lines[0])
        r = eval(lines[1])
        del lines[:3]
        i += 1
        if compare((l, r)):
            res += i
    return res

def compare(z):
    l,r = z
    if isinstance(l, int) and isinstance(r, int):
        return None if l == r else l < r
    if isinstance(l, int) and isinstance(r, list):
        return compare(([l], r))
    if isinstance(l, list) and isinstance(r, int):
        return compare((l, [r]))
    if isinstance(l, list) and isinstance(r, list):
        res = list(filter(lambda x:x is not None, map(compare,zip(l,r))))
        if len(res):
            return res[0]
        return None if len(l) == len(r) else len(l) < len(r)



if __name__ == '__main__':
    lines = []
    with open('13.txt') as f:
        for line in f.readlines():
            line = line.strip()
            lines.append(line)
    print(solve(lines))
