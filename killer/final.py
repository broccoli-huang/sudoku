#Input = "sat.txt" (line 15)
n = -1
list = []
txt = open("solution.txt", "r")
txt.readline()
t = txt.readline()
for i in range(9):
    list.append([])
    for j in range(9):
        bi = ''
        for k in range(4):
            bi += str((t[n+1] != '-')*1)
            n=t.find(' ',n+1)
        list[i].append(int(bi,2))
        if j % 3 == 0 and j != 0:
            print(" | ", end="")
        if j == 8:
            print(int(bi,2))
        else:
            print(str(int(bi,2)) + " ", end="")
    if i % 3 == 2 and i != 8:
        print("- - - - - - - - - - - - ")
txt.close()
