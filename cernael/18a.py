def solve(lines):
    #Plan: parse input into something searchable, then iterate through input again, adding the number of sides not connected to another cubelet to a global accumulator.
    # might be the wrong approach here
    res = {a:{b:{c:True}} for (a,b,c) in map(lambda x:x.split(','),lines)}
    return res

if __name__ == '__main__':
    lines = []
    with open('18test.txt') as f:
        for line in f.readlines():
            line = line.strip()
            lines.append(line)
    print(solve(lines))
