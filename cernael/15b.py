import re
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def manhattan(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


class Line:
    def __init__(self, intercept, slope):
        self.intercept = intercept
        self.slope = slope

    def __eq__(self, other):
        return self.intercept == other.intercept and self.slope == other.slope

    def intersect(self, other):
        if self.slope == other.slope:
            return None
        y2 = (self.intercept + other.intercept)
        x2 = (self.intercept - other.intercept)*other.slope
        if x2 % 2 == 0 and y2 % 2 == 0:
            return Point( int(x2 // 2), int(y2 // 2) )

    def __repr__(self):
        return "Intercept: {}, slope: {}".format(self.intercept, self.slope)


class Segment:
    def __init__(self, line, xmin, xmax):
        self.line = line
        self.xmin = xmin
        self.xmax = xmax

    def intersect(self, other):
        p = self.line.intersect(other.line)
        if (p and self.xmin <= p.x <= self.xmax and other.xmin <= p.x <= other.xmax):
            #print(self, other, p)
            return p
        return None

    def overlap(self, other):
        if self.line == other.line:
            xmin, xmax = max(self.xmin, other.xmin), min(self.xmax, other.xmax)
            return Segment(self.line, xmin, xmax) if xmin - xmax <= 0 else None

    def __repr__(self):
        return "line: ({}), xmin: {}, xmax: {}".format(self.line, self.xmin, self.xmax)


class Box:
    def __init__(self, c, r, size):
        # calculate the lines that bound the edge of the sensor's range in (y = kx+m, min(x), max(x)) format
        self.c = Point(c,r)
        self.size = size
        self.edges = [
            Segment(Line((r-size-1) + c, -1), (c-size-1), c),
            Segment(Line((r-size-1) - c, +1), c, (c+size+1)),
            Segment(Line((r+size+1) + c, -1), c, (c+size+1)),
            Segment(Line((r+size+1) - c, +1), (c-size-1), c)
        ]

    def overlap(self, other):
        res = set()
        for oe in other.edges:
            for se in self.edges:
                o = oe.overlap(se)
                #print(o)
                if o and o.xmin != o.xmax:
                    res.add(o)
        return res

    def contains(self, point):
        return self.c.manhattan(point) <= self.size

def solve(lines, n):
    boxes = []
    for line in lines:
        sc,sr,bc,br = [int(n) for n in re.split('[=:,]', line)[1::2]]
        mh = abs(sc-bc)+abs(sr-br)
        boxes.append(Box(sc, sr, mh))

    overlaps = set()
    for i in range(len(boxes)):
        for j in range(i+1, len(boxes)):
            overlaps |= boxes[i].overlap(boxes[j])
    points = {p for p in {p.intersect(n)
        for p in {r for r in overlaps if r.line.slope == 1}
        for n in {r for r in overlaps if r.line.slope == -1}
         } if p and 0 <= p.x <= n and 0 <= p.y <= n}

    points2 = set()

    for p in points:
        points2.add(p)
        for b in boxes:
            if b.contains(p):
                points2.remove(p)

    return {p.x*4000000+p.y for p in points2}
if __name__ == '__main__':
    lines = []
    #t, n = '15test.txt', 20
    t, n = '15.txt', 4000000
    with open(t) as f:
        for line in f.readlines():
            line = line.strip()
            lines.append(line)
    res = solve(lines, n)
    for r in res: print(r)
    #print(solve(['Sensor at x=3, y=5: closest beacon is at x=3, y=6', 'Sensor at x=1, y=7: closest beacon is at x=1, y=6', 'Sensor at x=4, y=8: closest beacon is at x=5, y=8'], 10))