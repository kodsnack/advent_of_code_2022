filepath = 'input'

points=0
with open(filepath) as fp:
    line = fp.readline()
    while line:
        # print(line)
        if len(line)>0:
            pos1=line[0]
            pos2=line[2]
            if pos2=='X': #loose
                points+=0
                if pos1=='A':
                    points+=3
                elif pos1=='B':
                    points+=1
                elif pos1=='C':
                    points+=2
                # print(points)
            elif pos2=='Y': #draw
                points+=3
                if pos1=='A':
                    points+=1
                elif pos1=='B':
                    points+=2
                elif pos1=='C':
                    points+=3
                # print(points)
            elif pos2=='Z': #win
                points+=6
                if pos1=='A':
                    points+=2
                elif pos1=='B':
                    points+=3
                elif pos1=='C':
                    points+=1
                # print(points)
        line = fp.readline().strip()

            
print(points)
            
            