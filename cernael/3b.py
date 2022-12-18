def solve(lines):
    res = [lines[n:n+3] for n in range(0, len(lines), 3)]

    return sum(
        map(
            lambda x:
                score((set(x[0]) &
                       set(x[1]) &
                       set(x[2])
                ).pop())
                ,
            res))

def score(c):
    if c.isupper():
        return ord(c) - 38
    return ord(c) - 96

if __name__ == '__main__':
    lines = []
    with open('3.txt') as f:
        for line in f.readlines():
            line = line.strip("\n")
            lines.append(line)
    test = ['vJrwpWtwJgWrhcsFMMfFFhFp','jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL','PmmdzqPrVvPwwTWBwg','wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn','ttgJtRGJQctTZtZT','CrZsJsPPZsGzwwsLwLmpwMDw']
    print(solve(lines))
    #print(solve(test))
