from arithmetic import *
import copy

def translate(lst):
    '''
    lst:[[1,2],[-1,-2],[1,2,-3]]     (list of literals (form:int))
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

def neq(x,y):  # x, y: block_no
    a, b, c, d = 4*x-3, 4*x-2, 4*x-1, 4*x
    e, f, g, h = 4*y-3, 4*y-2, 4*y-1, 4*y
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

def rc_bn(rc):
    '''
    (row,col) -> block_no
    rc_bn( (row,col) )
    '''
    return size*rc[0]+rc[1]+1


URL = input('URL:')
info = get_info(URL)

if isinstance(info,str):
    print(info)
    exit()

basic_info = info[0]
restrictions = info[1:]

size = basic_info[0]
num_range = basic_info[1]
num_min = num_range[0]
num_max = num_range[1]

num_to_bin = dict()
bin_to_num = dict()
bin_source = [
    (0,0,0,0),
    (0,0,0,1),
    (0,0,1,0),
    (0,0,1,1),
    (0,1,0,0),
    (0,1,0,1),
    (0,1,1,0),
    (0,1,1,1),
    (1,0,0,0),
    (1,0,0,1),
    (1,0,1,0),
    (1,0,1,1),
    (1,1,0,0),
    (1,1,0,1),
    (1,1,1,0),
    (1,1,1,1),
]

# construct bin num mapping
index = 0
for num in range(num_min,num_max+1):
    bin_form = bin_source[index]
    num_to_bin[num] = bin_form
    bin_to_num[bin_form] = num
    index += 1


# MAIN
cnf_content = ''


# set num range (in eqn form)



# nonrepeat in row & col
neq_lst=[]
# row
for row in range(size):
    for col_1 in range(size-1):
        for col_2 in range(col_1+1,size):
            neq_lst.append( ( rc_bn(row,col_1), rc_bn(row,col2) ) )
# column
for col in range(size):
    for row_1 in range(size-1):
        for row_2 in range(row_1+1,size):
            neq_lst.append( ( rc_bn(row_1,col),rc_bn(row_2,col) ) )

for pair in neq_lst:
    cnf_content += neq(pair[0],pair[1])
