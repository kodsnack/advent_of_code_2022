from functools import cmp_to_key

def solve(lines):
    lines.extend([[[2]],[[6]]])
    #for l in lines: print(l)
    #lines = lines[-2:]
    lines.sort(key=cmp_to_key(compare))
    return (lines.index([[2]]) + 1) * (lines.index([[6]]) + 1)

def compare(l,r):
#    print(0,type(l),type(r))
    if isinstance(l, int) and isinstance(r, int):
 #       print('ii', l,r)
        if l == r:
            return 0
        elif l < r:
            return -1
        return 1
    elif isinstance(l, int) and isinstance(r, list):
  #      print('il', l,r)
        return compare([l], r)
    elif isinstance(l, list) and isinstance(r, int):
   #     print('li', l,r)
        return compare(l, [r])
    elif isinstance(l, list) and isinstance(r, list):
    #    print('ll', l,r)
        res = list(filter(lambda x:x != 0, map(lambda z: compare(z[0],z[1]),zip(l,r))))
        if len(res):
            return int(res[0])//abs(int(res[0]))
        if len(l) == len(r):
            return 0
        elif len(l) < len(r):
            return -1
        return 1
    return 0



if __name__ == '__main__':
    lines = []
    with open('13.txt') as f:
        for line in f.readlines():
            line = line.strip()
            if line:
                line = eval(line)
                lines.append(line)
    print(solve(lines))
