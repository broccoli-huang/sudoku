# generate .cnf template

def translate(lst):
    '''
    lst:[[1,2],[-1,-2],[1,2,-3]]
    return:
    1 2 0
    -1 -2 0
    1 2 -3 0
    '''
    str_lst=[map(lambda l:str(l),clause) for clause in lst]
    content=''
    for clause in str_lst:
        content+=' '.join(clause)
        content+=' 0\n'
    return content

def neq(x,y):  #x,y:block_no
    a,b,c,d=4*x-3,4*x-2,4*x-1,4*x
    e,f,g,h=4*y-3,4*y-2,4*y-1,4*y
    lst=[
        [-a,b,c,-d,-e,f,g,-h],
        [-a,b,c,d,-e,f,g,h],
        [a,-b,-c,-d,e,-f,-g,-h],
        [a,-b,-c,d,e,-f,-g,h],
        [a,-b,c,-d,e,-f,g,-h],
        [a,-b,c,d,e,-f,g,h],
        [a,b,-c,-d,e,f,-g,-h],
        [a,b,-c,d,e,f,-g,h],
        [a,b,c,-d,e,f,g,-h]
    ]
    return translate(lst)


# Main

content='p cnf ? ?\n'

#block value range 1-9
for block_no in range(1,82):
    a,b,c,d= 4*block_no-3, 4*block_no-2, 4*block_no-1, 4*block_no
    lst=[
        [-a,-c],
        [-a,-b],
        [a,b,c,d]
    ]
    content+=translate(lst)

neq_lst=[]
#row
for row in range(9):
    for col_1 in range(8):
        for col_2 in range(col_1+1,9):
            neq_lst.append((9*row+col_1+1,9*row+col_2+1))
#column
for col in range(9):
    for row_1 in range(8):
        for row_2 in range(row_1+1,9):
            neq_lst.append((9*row_1+col+1,9*row_2+col+1))
#big block
pos=[1,2,3,10,11,12,19,20,21]
for bb in range(9):
    for index_1 in range(8):
        for index_2 in range(index_1+1,9):
            new=(pos[index_1],pos[index_2])
            if new not in neq_lst:
                neq_lst.append(new)
    if bb%3==2:
        pos=[no+21 for no in pos]
    else:
        pos=[no+3 for no in pos]

for pair in neq_lst:
    content+=neq(pair[0],pair[1])


f = open("template.txt", "w")
f.write(content)
f.close()
