filepath = 'input'
import string

points=0
with open(filepath) as fp:
    line = fp.readline()
    while line:
        line =line.strip()
        left = line.split(",")[0]
        leftStart = int(left.split("-")[0].strip())
        leftStop = int(left.split("-")[1].strip())
        leftRange = range(leftStart, leftStop+1)
        # print(leftRange)
        
        right = line.split(",")[1]
        rightStart = int(right.split("-")[0].strip())
        rightStop = int(right.split("-")[1].strip())
        rightRange = range(rightStart, rightStop+1)
        # print(rightRange)

        ls = set(leftRange) 
        rs = set(rightRange)
        overlap = ls & rs
        # print(len(overlap))

        if len(overlap)>0:
            points+=1

        line = fp.readline()
print(points)