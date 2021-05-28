import json
from begin import translate

def parse(eqn):
    ret=['','','p','','p',''] # 'l = r1 + !r2;' => ['l','or','p','r1','n','r2']
    wait=[]
    for char in eqn:
        if char == ' ':
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


def newvar():
    global var_no
    var_no += 1
    return var_no



if __name__ == '__main__':

    with open('info.json') as f:
        data = json.load(f)
        size = data['size']

    f = open("middle.eqn", "r")
    eqn_content = f.read()
    f.close()

    f = open("begin.cnf", "r")
    cnf_content = f.read()
    f.close()

    var_no = 4*size**2

    eqn_splt = eqn_content.split('\n')
    start_line = 0
    while not eqn_splt[start_line].startswith('new'):   # possibly starts with f?
        start_line += 1
    eqn_lst = eqn_splt[start_line:]

    DICT = dict()
    for i in range(1,4*size**2+1):
        DICT['a'+str(i)] = i

    must_true = []

    for eqn in eqn_lst:
        parsed = parse(eqn) # ['l','or','p','r1','n','r2']
        if parsed[0] in DICT.keys():
            X = DICT[parsed[0]]
        else:
            nv = newvar()
            DICT[parsed[0]] = nv
            X = nv
            if parsed[0].startswith('f'):
                must_true.append([X])
        if parsed[3] in DICT.keys():
            Y = DICT[parsed[3]]
        else:
            nv = newvar()
            DICT[parsed[3]] = nv
            Y = nv
            if parsed[3].startswith('f'):
                must_true.append([Y])
        if parsed[5] in DICT.keys():
            Z = DICT[parsed[5]]
        else:
            nv = newvar()
            DICT[parsed[5]] = nv
            Z = nv
            if parsed[5].startswith('f'):
                must_true.append([Z])

        if (parsed[1],parsed[2],parsed[4]) == ('and','p','p'):
            cnf_content += cnfy1(X,Y,Z)
        elif (parsed[1],parsed[2],parsed[4]) == ('and','n','p'):
            cnf_content += cnfy2(X,Y,Z)
        elif (parsed[1],parsed[2],parsed[4]) == ('and','p','n'):
            cnf_content += cnfy3(X,Y,Z)
        elif (parsed[1],parsed[2],parsed[4]) == ('and','n','n'):
            cnf_content += cnfy4(X,Y,Z)
        elif (parsed[1],parsed[2],parsed[4]) == ('or','p','p'):
            cnf_content += cnfy5(X,Y,Z)
        elif (parsed[1],parsed[2],parsed[4]) == ('or','n','p'):
            cnf_content += cnfy6(X,Y,Z)
        elif (parsed[1],parsed[2],parsed[4]) == ('or','p','n'):
            cnf_content += cnfy7(X,Y,Z)
        elif (parsed[1],parsed[2],parsed[4]) == ('or','n','n'):
            cnf_content += cnfy8(X,Y,Z)


    cnf_content += translate(must_true)

    num_of_vars = var_no
    num_of_clauses = cnf_content.count('\n')
    cnf_pre = 'p cnf '+str(num_of_vars)+' '+str(num_of_clauses)+'\n'

    f = open("middle.cnf", "w")
    f.write(cnf_pre + cnf_content)
    f.close()
