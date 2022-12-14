# print("testa python")
filepath = 'input'
cals = []
with open(filepath) as fp:
    line = fp.readline()
    cnt = 1
    cal = 0
    while line:
        val = line.strip()
        if len(val)>0:
            cal += int(val)
        else:
            cals.append(cal)
            # print(cal)
            cal =0

        # print(len(line.strip()))
        line = fp.readline()
        cnt += 1
# print(cals)
print("Del1")
print(max(cals))

cals.sort(reverse=True)
calsSlice = cals[0:3]
# print(calsSlice)
print("Del2")
print(sum(calsSlice))