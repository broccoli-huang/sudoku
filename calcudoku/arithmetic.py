from global_splitter import grab
def add_rotation(li):
    if len(li) == 1:
        return [li]
    else:
        rlist = []
        for i in range(len(li)):
            if i > 0 and li[i] == li[i-1]:
                continue
            sli = li[:i] + li[i+1:]
            for j in add_rotation(sli):
                rlist.append([li[i]]+j)
        return rlist
def log(a,b):
    if b == 1:
        return 0
    result = 0
    while True:
        b //= a
        result += 1
        if b == 1:
            return result
        elif not(not b % a):
            return 0
def repeat_list(zone,blocks):
    if blocks == 1:
        return [[i] for i in zone]
    else:
        rli = []
        for i in range(len(zone)):
            for j in repeat_list(zone[i:],blocks-1):
                rli.append([zone[i]]+j)
        return rli
def possible_mod(zone,result):
    rli = []
    for i in range(len(zone)):
        for j in zone[i:]:
            if zone[i]%j == result or j%zone[i] == result:
                rli.append([i,j])
    return rli
def possible_plus(zone,blocks,result):
    if result < zone[0]*blocks or result > zone[-1]*blocks:
        return []
    elif blocks == 1:
        if result in zone:
            return [[result]]
        else:
            return []
    rli = []
    for i in range(zone[0],result//blocks+1):
        for j in possible_plus(range(i,zone[-1]+1),blocks-1,result-i):
            rli.append([i]+j)
    return rli
def possible_minus(zone,blocks,result):
    if result > len(zone)-1:
        return []
    rli = []
    for i in zone:
        for j in possible_plus(zone,blocks-1,i-result):
            rli.append(j+[i])
    return rli
def possible_multiply(zone,blocks,result):
    if blocks == 1:
        if result in zone:
            return [[result]]
        else:
            return []
    rli = []
    if result == 0:
        if 0 in zone:
            for i in repeat_list(zone,blocks-1):
                j = i+[0]
                j.sort()
                rli.append(j)
            return rli
        else:
            return []
    else:
        if 0 in zone:
            z = list(zone)
            z = z[:z.index(0)] + z[z.index(0)+1:]
        else:
            z = zone
            for i in z:
                if result%i == 0:
                    for j in possible_multiply(range(i,z[-1]+1),blocks-1,result//i):
                        rli.append([i]+j)
    return rli
def possible_divide(zone,blocks,result):
    rli = []
    if result == 0:
        li = repeat_list(zone,blocks-1)
        for j in li:
            if not 0 in j:
                t = [0]+j
                t.sort()
                rli.append(t)
    else:
        for i in zone:
            if i == 0:
                pass
            if i % result != 0:
                continue
            else:
                for j in possible_multiply(zone,blocks-1,i//result):
                    t = [i]+j
                    t.sort()
                    rli.append(t)
    return rli
def possible_power(zone,blocks,result):
    if blocks == 1:
        if result in zone:
            return [[result]]
        else:
            return []
    rli = []
    if result == 1:
        if 1 in zone:
            for i in repeat_list(zone,blocks-1):
                j = i+[1]
                j.sort()
                rli.append(j)
            return rli
        else:
            return []
    elif result == 0:
        if 0 in zone:
            for i in repeat_list(zone,blocks-1):
                j = i+[0]
                j.sort()
                rli.append(j)
            return rli
        else:
            return []
    else:
        z = list(zone)
        if 0 in zone:
            z.remove(0)
        if 1 in zone:
            z.remove(1)
        for i in z:
            if not result % i:
                if not not log(i,result):
                    for j in possible_power(zone,blocks-1,log(i,result)):
                        t = [i]+j
                        t.sort()
                        rli.append([i]+j)
        return rli
def add_all_rotation(li):
    rlist = []
    for i in li:
        rlist += add_rotation(i)
    return rlist
def condition_to_possibilities(zone,li):
    rlist = []
    if li[0][1] == '_':
        return([[[li[0][0]]],li[1:]])
    elif li[0][1] == '+':
        rlist = [add_all_rotation(possible_plus(zone,len(li)-1,li[0][0]))]
        rlist.append(li[1:])
        return rlist
    elif li[0][1] == '-':
        rlist = [add_all_rotation(possible_minus(zone,len(li)-1,li[0][0]))]
        rlist.append(li[1:])
        return rlist
    elif li[0][1] == '×':
        rlist = [add_all_rotation(possible_multiply(zone,len(li)-1,li[0][0]))]
        rlist.append(li[1:])
        return rlist
    elif li[0][1] == ':':
        rlist = [add_all_rotation(possible_divide(zone,len(li)-1,li[0][0]))]
        rlist.append(li[1:])
        return rlist
    elif li[0][1] == 'mod':
        rlist = [add_all_rotation(possible_mod(zone,li[0][0]))]
        rlist.append(li[1:])
        return rlist
    elif li[0][1] == '^':
        rlist = [add_all_rotation(possible_power(zone,len(li)-1,li[0][0]))]
        rlist.append(li[1:])
        return rlist

def get_info(url):
    condition_list = grab(url)
    result_list = []
    if len(condition_list) == 3:
        result_list = 'TWIN NOT AVAILABLE'
    elif isinstance(condition_list[0],list):
        zone1 = range(condition_list[0][1][0],condition_list[0][1][1]+1)
        result_list.append(condition_list[0])
        for i in condition_list[1:]:
            result_list.append(condition_to_possibilities(zone1,i))
    else:
        result_list = 'SUDOKU TYPE ERROR'
    return result_list

'''
while True:
    condition_list = grab(input("URL:"))
    result_list = []
    if len(condition_list) == 3:
        result_list = ['TWIN NOT AVAILABLE']
    elif isinstance(condition_list[0],list):
        zone1 = range(condition_list[0][1][0],condition_list[0][1][1]+1)
        result_list.append(condition_list[0])
        for i in condition_list[1:]:
            result_list.append(condition_to_possibilities(zone1,i))
    else:
        result_list = ['SUDOKU TYPE ERROR']
    print(result_list)
'''
'''
Simple Calcudoku Only (Killer, Sudoku, Twin not available yet)
Output:
[
    [size,[min,max(included)]],
    [
        [
            [1,2,4...],
            [possibility 2],
            [possibility 3], ...
        ],
        [
            (r1,c1),
            (r2,c2),...
        ],
    ],
    [
        [possible lists with different rotations],
        [chunk_position_tuples]
    ],
    [condition 3], ...
]
'''
