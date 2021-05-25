import requests
from bs4 import BeautifulSoup
def add_item(list, item, refer):
    for i in list:
        if refer in i:
            i.append(item)
def grab(url):
    chunk_list = []
#    dict = {}
    wait = 0
    res = ''
    r = requests.get(url)
    t = BeautifulSoup(r.text,'html.parser')
    table = t.find('table', id="puzzle0")
    for i in range(9):
        for j in range(9):
            try:
                res = table.find(id = "tdp0r"+str(i)+"c"+str(j)).get_text()[1:]
            except AttributeError:
                continue
            if res != '':
                chunk_list.append([int(res),(i,j)])
                wait = 0
            else:
                sty = table.find(id = "p0r"+str(i)+"c"+str(j)).get('style')
                if not "margin-top" in sty:
                    add_item(chunk_list,(i,j),(i-1,j))
                    for q in range(wait):
                        add_item(chunk_list,(i,j-q-1),(i-1,j))
                    wait = 0
                elif not "margin-left" in sty:
                    if wait == 0:
                        add_item(chunk_list,(i,j),(i,j-1))
                    else:
                        wait += 1
                elif not "margin-right" in sty:
                    wait += 1
                else:
                    if j>1 and "margin-left" in table.find(id = "p0r"+str(i)+"c"+str(j-1)).get('style') and "margin-right" in table.find(id = "p0r"+str(i)+"c"+str(j-1)).get('style'):
                        add_item(rlist,(i,j),(i,j-2))
                    else:
                        print('ERROR, SHAPE UNDETECTABLE')
                        break
    return chunk_list
#    for i in range(len(chunk_list)):
#        for j in chunk_list[i]:
#            dict[j] = i
#    print(dict)
#print(grab(input()))
'''
#FORMAT
chunk_list = [[sum_chunk_1,(x1,y1),(x2,y2),...],[condition2],....]
----------------
line 9,47~50
dict[(x,y)] = (x,y) in chunk index
(x,y) in chunk_list[ dict[(x,y)] ] == True
'''
