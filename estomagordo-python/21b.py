from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import adjacent, chunks, chunks_with_overlap, columns, custsort, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(lines):
    def prepmonkeys():
        monkeys = {}

        for line in lines:
            parts = line.split()

            monkey = parts[0][:-1]
            pieces = []

            if len(parts) == 2:
                pieces.append(int(parts[1]))
            else:
                pieces += parts[1:]

            monkeys[monkey] = pieces

        haschanged = True
        while haschanged:
            haschanged = False

            for k in monkeys.keys():
                if k == 'humn':
                    continue

                v = monkeys[k]

                if len(v) == 1:
                    continue

                if not isinstance(v[0], int) and v[0] != 'humn':
                    if len(monkeys[v[0]]) == 1:
                        haschanged = True
                        v[0] = monkeys[v[0]][0]
                if not isinstance(v[2], int) and v[2] != 'humn':
                    if len(monkeys[v[2]]) == 1:
                        haschanged = True
                        v[2] = monkeys[v[2]][0]

                op = v[1]

                if isinstance(v[0], int) and isinstance(v[2], int):
                    a = v[0]
                    b = v[2]
                    val = 0

                    if op == '+':
                        val = a+b
                    elif op == '-':
                        val = a-b
                    elif op == '/':
                        val = a//b
                    else:
                        val = a*b

                    monkeys[k] = [val]

        return monkeys    

    def humn(donemonkeys, changemonkeys, n):
        donemonkeys['humn'] = [n]
        changemonkeys['root'][1] = '='

        while not (isinstance(changemonkeys['root'][0], int) and isinstance(changemonkeys['root'][2], int)):
            for k in changemonkeys.keys():
                v = changemonkeys[k]

                if len(v) == 1:
                    continue

                if not isinstance(v[0], int):
                    if v[0] in donemonkeys or len(changemonkeys[v[0]]) == 1:
                        v[0] = donemonkeys[v[0]][0] if v[0] in donemonkeys else changemonkeys[v[0]][0]
                if not isinstance(v[2], int):
                    if v[2] in donemonkeys or len(changemonkeys[v[2]]) == 1:
                        v[2] = donemonkeys[v[2]][0] if v[2] in donemonkeys else changemonkeys[v[2]][0]

                op = v[1]

                if isinstance(v[0], int) and isinstance(v[2], int) and k != 'root':
                    a = v[0]
                    b = v[2]
                    val = 0

                    if op == '+':
                        val = a+b
                    elif op == '-':
                        val = a-b
                    elif op == '/':
                        val = a//b
                    elif op == '*':
                        val = a*b
                    else:
                        val = a==b

                    changemonkeys[k] = [val]

        return changemonkeys['root'][0] == changemonkeys['root'][2]

    n = 280000
    basemonkeys = prepmonkeys()
    
    donemonkeys = {k: [el for el in v] for k, v in basemonkeys.items() if len(v) == 1}
    changemonkeys = {k: [el for el in v] for k, v in basemonkeys.items() if len(v) == 3}

    res = [v for v in changemonkeys['root'] if isinstance(v, int)][0]
    symbol = [v for v in changemonkeys['root'][0:3:2] if isinstance(v, str)][0]

    while symbol != 'humn':
        monkey = changemonkeys[symbol]
        val = [v for v in monkey if isinstance(v, int)][0]
        print(symbol, monkey)
        symbol = [v for v in monkey[0:3:2] if isinstance(v, str) and v != '+'][0]
        op = monkey[1]

        if op == '+':
            res -= val
        elif op == '-':
            res += val
        elif op == '/':
            res *= val
        else:
            res //= val

    return res

    # def eqfor(symb):
    #     return '(' + ''.join(str(val) for val in changemonkeys[symb]) + ')'

    # def extractsymb(eq):
    #     return ''.join(c for c in eq if c.isalpha())
    
    # equation = eqfor('root')
    # lastsymb = extractsymb(equation)

    # while lastsymb != 'humn':
    #     equation = equation.replace(lastsymb, eqfor(lastsymb))
    #     lastsymb = extractsymb(equation)
    
    # return equation
    
    if 'humn' in changemonkeys:
        del changemonkeys['humn']

    while True:
        morphmonkeys = {k: [el for el in v] for k, v in changemonkeys.items()}
        
        if n % 10000 == 0:
            print(n)

        res = humn(donemonkeys, morphmonkeys, n)

        if res:
            return n

        n += 1


def main():
    lines = []

    with open('21.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())

# 8401064794714