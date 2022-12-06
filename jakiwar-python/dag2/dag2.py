filepath = 'input'

points=0
with open(filepath) as fp:
    line = fp.readline()
    while line:
        # print(line)
        if len(line)>0:
            pos1=line[0]
            pos2=line[2]
            if pos2=='X':
                points+=1
                if pos1=='A':
                    points+=3
                elif pos1=='B':
                    points+=0
                elif pos1=='C':
                    points+=6
                # print(points)
            elif pos2=='Y':
                points+=2
                if pos1=='A':
                    points+=6
                elif pos1=='B':
                    points+=3
                elif pos1=='C':
                    points+=0
                # print(points)
            elif pos2=='Z':
                points+=3
                if pos1=='A':
                    points+=0
                elif pos1=='B':
                    points+=6
                elif pos1=='C':
                    points+=3
                # print(points)
        line = fp.readline().strip()

            
print(points)
            
            