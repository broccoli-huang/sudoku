# generate .cnf
from killer_crawler import grab
from generate_template import translate,neq

f = open("template.txt", "r")
content = f.read()
f.close()

chunk_list=grab(input())

var_no = 324

def newvar():
    global var_no
    var_no += 1
    return var_no

def map_to_big(pos):
    return (pos[0]//3,pos[1]//3)

def sumn(nb):
    f = open('sum'+str(nb)+'.txt','r')
    full = f.readlines()
    f.close()
    startline = {1:3,2:3,3:3,4:3,5:4,6:4,7:4,8:4,9:5}
    return full[startline[nb]:]

def parse(eqn):
    ret=['','','p','','p',''] # 'l = r1 + !r2;\n' => ['l','or','p','r1','n','r2']
    wait=[]
    for char in eqn:
        if char in [' ','\n']:
            continue
        elif char == '=':
            ret[0] = ''.join(wait)
            wait=[]
        elif char == '*':
            ret[1] = 'and'
            ret[3] = ''.join(wait)
            wait=[]
        elif char == '+':
            ret[1] = 'or'
            ret[3] = ''.join(wait)
            wait=[]
        elif char == '!':
            if ret[1] == '':
                ret[2] = 'n'
            else:
                ret[4] = 'n'
        elif char == ';':
            ret[5] = ''.join(wait)
            wait=[]
        else:
            wait.append(char)
    return ret

def cnfy1(X,Y,Z):
    return translate([[-X,Y],[-X,Z],[X,-Y,-Z]])

def cnfy2(X,Y,Z):
    return translate([[-X,-Y],[-X,Z],[X,Y,-Z]])

def cnfy3(X,Y,Z):
    return translate([[-X,Y],[-X,-Z],[X,-Y,Z]])

def cnfy4(X,Y,Z):
    return translate([[-X,-Y],[-X,-Z],[X,Y,Z]])

def cnfy5(X,Y,Z):
    return translate([[X,-Y],[X,-Z],[-X,Y,Z]])

def cnfy6(X,Y,Z):
    return translate([[X,Y],[X,-Z],[-X,-Y,Z]])

def cnfy7(X,Y,Z):
    return translate([[X,-Y],[X,Z],[-X,Y,-Z]])

def cnfy8(X,Y,Z):
    return translate([[X,Y],[X,Z],[-X,-Y,-Z]])

def to_bin(summ):
    ret=[0,0,0,0,0,0]
    if summ//32 == 1:
        ret[0] = 1
        summ -= 32
    if summ//16 == 1:
        ret[1] = 1
        summ -= 16
    if summ//8 == 1:
        ret[2] = 1
        summ -= 8
    if summ//4 == 1:
        ret[3] = 1
        summ -= 4
    if summ//2 == 1:
        ret[4] = 1
        summ -= 2
    ret[5] = summ
    return ret

#main
for chunk in chunk_list:
    summ = chunk[0]
    blocks = chunk[1:]
    nb = len(blocks)
    for i in range(nb-1):
        for j in range(i+1,nb):
            if blocks[i][0] != blocks[j][0] and blocks[i][1] != blocks[j][1] and map_to_big(blocks[i]) != map_to_big(blocks[j]):
                content += neq( 9*blocks[i][0]+blocks[i][1]+1 , 9*blocks[j][0]+blocks[j][1]+1 )

    DICT = dict()
    for i in range(nb):
        block = blocks[i]
        block_no = 9*block[0] + block[1] + 1
        DICT['a'+str(i)+'0'] = 4*block_no - 3
        DICT['a'+str(i)+'1'] = 4*block_no - 2
        DICT['a'+str(i)+'2'] = 4*block_no - 1
        DICT['a'+str(i)+'3'] = 4*block_no

    eqns = sumn(nb)
    for eqn in eqns:
        parsed = parse(eqn) #['l','or','p','r1','n','r2']
        if parsed[0] in DICT.keys():
            X = DICT[parsed[0]]
        else:
            nv = newvar()
            DICT[parsed[0]] = nv
            X = nv
        if parsed[3] in DICT.keys():
            Y = DICT[parsed[3]]
        else:
            nv = newvar()
            DICT[parsed[3]] = nv
            Y = nv
        if parsed[5] in DICT.keys():
            Z = DICT[parsed[5]]
        else:
            nv = newvar()
            DICT[parsed[5]] = nv
            Z = nv

        if (parsed[1],parsed[2],parsed[4]) == ('and','p','p'):
            content += cnfy1(X,Y,Z)
        elif (parsed[1],parsed[2],parsed[4]) == ('and','n','p'):
            content += cnfy2(X,Y,Z)
        elif (parsed[1],parsed[2],parsed[4]) == ('and','p','n'):
            content += cnfy3(X,Y,Z)
        elif (parsed[1],parsed[2],parsed[4]) == ('and','n','n'):
            content += cnfy4(X,Y,Z)
        elif (parsed[1],parsed[2],parsed[4]) == ('or','p','p'):
            content += cnfy5(X,Y,Z)
        elif (parsed[1],parsed[2],parsed[4]) == ('or','n','p'):
            content += cnfy6(X,Y,Z)
        elif (parsed[1],parsed[2],parsed[4]) == ('or','p','n'):
            content += cnfy7(X,Y,Z)
        elif (parsed[1],parsed[2],parsed[4]) == ('or','n','n'):
            content += cnfy8(X,Y,Z)

    fis = to_bin(summ)
    f_val=[]
    for i in range(6):
        if fis[i] == 1:
            f_val.append([DICT['f0'+str(i)]])
        else:
            f_val.append([(-1)*DICT['f0'+str(i)]])
    content += translate(f_val)

num_of_vars = var_no
num_of_clauses = content.count('\n')-1
content2 = content.replace('? ?',str(num_of_vars)+' '+str(num_of_clauses))

f = open("killer.cnf", "w")
f.write(content2)
f.close()
