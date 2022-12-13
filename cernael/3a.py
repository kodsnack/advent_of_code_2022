def solve(lines):
    return sum(list(
        map(
            lambda x:
                score((set(x[:int(len(x)/2) ]) &
                 set(x[ int(len(x)/2):])
                ).pop())
                ,
            lines)))
#  return list(map(lambda x: len(x)/2, lines))

def score(c):
    if c.isupper():
        return ord(c) - 38
    return ord(c) - 96

if __name__ == '__main__':
    lines = []
    with open('3.txt') as f:
        for line in f.readlines():
            line.strip()
            lines.append(line)
    test = ['vJrwpWtwJgWrhcsFMMfFFhFp','jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL','PmmdzqPrVvPwwTWBwg','wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn','ttgJtRGJQctTZtZT','CrZsJsPPZsGzwwsLwLmpwMDw']
    print(solve(lines))
    #print(solve(test))
