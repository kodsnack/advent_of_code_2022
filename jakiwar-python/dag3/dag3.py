filepath = 'input'
import string

points=0
with open(filepath) as fp:
    line = fp.readline()
    while line:
        line =line.strip()
        firstStart =0
        firstStop = int(len(line)/2)
        # print(firstStop)
        firstHalf = line[firstStart:firstStop]

        secondStart=firstStop
        secondStop=int(len(line))
        # print(secondStart)
        # print(secondStop)
        secondHalf = line[secondStart:secondStop]
        # secondHalf = line[ len(line)/2 : len(line)]
        # print(firstHalf)
        # print(secondHalf)

        overlap2 = set(firstHalf) & set(secondHalf)
        # print(overlap2)

        for cc in overlap2:
            point=1
            # print(cc.isupper())
            if cc[0].isupper():
                point+=26
            point+=string.ascii_lowercase.index(cc.lower())
            # print(point)
        points+=point
        line = fp.readline()
print(points)