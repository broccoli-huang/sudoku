import json

with open('info.json') as f:
    data = json.load(f)
    size = data['size']
    num_min = data['num_min']
    num_max = data['num_max']

f = open("solution.txt", "r")
solution_str = f.read()
f.close()

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
    bin_to_num[bin_form] = num
    index += 1

solution = solution_str.split('\n')[1].split(' ')[:4*size**2]
solution.insert(0,'')

ans_lst = []
for row in range(size):
    row_ans_lst = []
    for col in range(size):
        block_no = size * row + col + 1
        bit1 = 0 if solution[4*block_no-3].startswith('-') else 1
        bit2 = 0 if solution[4*block_no-2].startswith('-') else 1
        bit3 = 0 if solution[4*block_no-1].startswith('-') else 1
        bit4 = 0 if solution[4*block_no].startswith('-') else 1
        val = bin_to_num[ (bit1,bit2,bit3,bit4) ]
        row_ans_lst.append(val)
    ans_lst.append(row_ans_lst)


for i in range(len(ans_lst)):
    for j in range(len(ans_lst)):
    	print(ans_lst[i][j],end = ' ')
    print('\n',end = '')
