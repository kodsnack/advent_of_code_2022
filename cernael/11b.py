from functools import reduce
import operator

class Monkey:
    def __init__(self, lines, group):
        items = lines[1].split(':')
        items = [int(i) for i in items[1].split(',')]
        op = lines[2].split(':')

        self.inspect_count = 0
        self.items = items
        self.group = group
        self.mod = int(lines[3][-2:])
        self.t = int(lines[4][-1])
        self.f = int(lines[5][-1])

        self.inspect = self.def_op(op[1])

    def def_op(self, text):
        def op(self, old):
            self.inspect_count += 1
            t = text.split('=')
            return eval(t[1])

        return op

    def test(self, n):
        return not n % self.mod

    def catch(self, item):
        self.items.append(item)

    def toss(self):
        while self.items:
            item = self.items.pop(0)
            item = self.inspect(self,item)
            item %= self.group.prod_mods()
            if self.test(item):
                self.group.monkeys[self.t].catch(item)
            else:
                self.group.monkeys[self.f].catch(item)


class Monkeys:
    def __init__(self, lines):
        self.monkeys = []
        while lines:
            self.monkeys.append(Monkey(lines[:7], self))
            del lines[:7]

    def round(self):
        for m in self.monkeys:
            m.toss()

    def show_count(self):
        return [m.inspect_count for m in self.monkeys]

    def prod_mods(self):
        return reduce(operator.mul, [m.mod for m in self.monkeys])


def solve(lines):
    monkeys = Monkeys(lines)
    for _ in range(10000):
        monkeys.round()

    m = sorted(monkeys.show_count())[-2:]
    return reduce(operator.mul, m)

if __name__ == '__main__':
    lines = []
    with open('11.txt') as f:
        for line in f.readlines():
            line = line.strip()
            lines.append(line)
    print(solve(lines))
