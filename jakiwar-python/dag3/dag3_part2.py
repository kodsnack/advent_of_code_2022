filepath = 'input'
import string

points=0
with open(filepath) as fp:
    line = fp.readline()
    groupcount=0
    group=[]
    while line:
        line =line.strip()
        groupcount +=1
        group.append(line)

        if groupcount==3:
            overlap = set(group[0]) & set(group[1]) & set(group[2])
            # print(overlap)

            for cc in overlap:
                point=1
                # print(cc.isupper())
                if cc[0].isupper():
                    point+=26
                point+=string.ascii_lowercase.index(cc.lower())
                # print(point)
            points+=point
            groupcount=0
            group=[]

        line = fp.readline()
print(points)