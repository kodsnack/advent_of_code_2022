class Dir:
    def __init__(self, name):
        self.children = {}
        self.files = []
        self.name = name

    def add_file(self, name, size):
        self.files.append(File(name, size))

    def add_child(self, name):
        self.children[name] = Dir(name)

    def tell_size(self):
        return sum([c.tell_size() for c in list(self.children.values()) + self.files])

    def traverse_tree(self, path = '/'):
        ret = [(path, self.tell_size())]
        for c in self.children.values():
            ret.extend(c.traverse_tree(path + self.name + '/'))
        for f in self.files:
            pass
        return ret


class File:
    def __init__(self, name, size):
        self.size = size
        self.name = name

    def tell_size(self):
        return self.size

def solve(lines):
    stack = [Dir('/')]
    for l in lines:
        print(l)
        l = l.split()
        if l[0] == '$':
            if l[1] == 'cd':
                if l[2] == '/':
                    del stack[1:]
                elif l[2] == '..':
                    stack.pop()
                else:
                    stack.append(stack[-1].children[l[2]])
            elif l[1] == 'ls':
                pass
        elif l[0] == 'dir':
            stack[-1].add_child(l[1])
        else:
            stack[-1].add_file(l[1], int(l[0]))
    return sum(map(lambda i: i[1] if i[1] <= 100000 else 0, stack[0].traverse_tree()))

if __name__ == '__main__':
    lines = []
    with open('7.txt') as f:
    #with open('7test.txt') as f:
        for line in f.readlines():
            line = line.strip()
            lines.append(line)
    print(solve(lines))
