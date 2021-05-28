from arithmetic import *
import copy
import json

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



if __name__ == '__main__':

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
        index += 1


    # MAIN
    cnf_content = ''


    # nonrepeat in row & col
    neq_lst=[]
    # row
    for row in range(size):
        for col_1 in range(size-1):
            for col_2 in range(col_1+1,size):
                neq_lst.append( ( rc_bn((row,col_1)), rc_bn((row,col_2)) ) )
    # column
    for col in range(size):
        for row_1 in range(size-1):
            for row_2 in range(row_1+1,size):
                neq_lst.append( ( rc_bn((row_1,col)),rc_bn((row_2,col)) ) )

    for pair in neq_lst:
        cnf_content += neq(pair[0],pair[1])


    # arithmetic restrictions
    eqn_out_count = 0
    eqn_out_lst = []

    eqn_content = ''

    for restriction in restrictions:
        possibilities = restriction[0]
        positions = restriction[1]

        block_no_lst = list( map( rc_bn , positions ))
        num_of_blocks = len(block_no_lst)
        block_var_lst = [ ['a'+str(4*bn-3),'a'+str(4*bn-2),'a'+str(4*bn-1),'a'+str(4*bn)] for bn in block_no_lst]

        eqn_out_count += 1
        func = 'f' + str(eqn_out_count)
        eqn_out_lst.append(func)

        eqn_content += func + ' = 0'

        for possibility in possibilities:
            eqn_content += ' + ('
            possi_bin = [num_to_bin[i] for i in possibility]
            for blk in range(num_of_blocks):
                for i in range(4):
                    V = block_var_lst[blk][i]
                    B = possi_bin[blk][i]
                    if B == 0:
                        eqn_content += '!'
                    eqn_content += V + ' * '
            eqn_content += '1)'

        eqn_content += ';\n'

    eqn_pre_1 = 'INORDER ='
    for i in range(1,4*size**2+1):
        eqn_pre_1 += ' a' + str(i)
    eqn_pre_1 += ';\n'

    eqn_pre_2 = 'OUTORDER = ' + ' '.join(eqn_out_lst)+';\n'


    data = {
        'size' : size,
        'num_min' : num_min,
        'num_max' : num_max
    }
    with open('info.json', 'w') as json_file:
        json.dump(data, json_file)

    f = open("begin.eqn", "w")
    f.write(eqn_pre_1 + eqn_pre_2 + eqn_content)
    f.close()

    f = open("begin.cnf", "w")
    f.write(cnf_content)
    f.close()
