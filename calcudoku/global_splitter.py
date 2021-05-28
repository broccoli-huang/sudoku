from bs4 import BeautifulSoup
import requests
import time
def add_item(list, item, refer):
    for i in list:
        try:
            if refer in i:
                i.append(item)
        except TypeError:
            continue
def grab(url):
    rlist = []
    h = BeautifulSoup('','html.parser')
    while True:
        try:
            h = BeautifulSoup(requests.get(url).text,'html.parser')
            break
        except TimeoutError:    #prevent Time Out
            print("ConnectionError")
    info = h.find(id = 'puzzle_rating_info').b.get_text()   #info text
    if 'Killer' in info:
        rlist.append(1)     #Killer:1
        table = h.find('table', id="puzzle0")
        wait = 0
        for i in range(9):
            for j in range(9):
                try:
                    chunk_result = table.find(id = "tdp0r"+str(i)+"c"+str(j)).get_text()[1:]
                except AttributeError:
                    continue
                if chunk_result != '':
                    rlist.append([[int(chunk_result),'+'],(i,j)])
                    wait = 0
                else:
                    sty = table.find(id = "p0r"+str(i)+"c"+str(j)).get('style')
                    if not "margin-top" in sty:
                        add_item(rlist,(i,j),(i-1,j))
                        for q in range(wait):
                            add_item(rlist,(i,j-q-1),(i-1,j))
                        wait = 0
                    elif not "margin-left" in sty:
                        if wait == 0:
                            add_item(rlist,(i,j),(i,j-1))
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
        return rlist
    elif 'Sudoku' in info:
        rlist.append(2)     #Sudoku:2
        table = h.find('table', id="puzzle0")
        for i in range(9):
            rlist.append([])
            for j in range(9):
                    if table.find(id = 'p0r'+str(i)+'c'+str(j)).get_text() == '':
                        rlist[p+1].append(0)
                    else:
                        rlist[p+1].append(int(table.find(id = 'p0r'+str(i)+'c'+str(j)).get_text()))
        return rlist
    else:
        try:
            n = int(info[info.find('× ')+2:])
        except:
            print("Info Detect Error")
        for i in h.find_all('font',size = "-1"):
            if "1-"+str(n) in i.get_text():
                rlist.append([n,[]])
                j = i.get_text().replace(' to ','-')
                for c in range(len(j)):
                    if j[c]=='-':
                        if j[c-1] != ' ':
                            j = j[:c] + '*' + j[c+1:]
                            break
                k = j.split()
                l = k[k.index("instead")-1].split('*')
                rlist[0][1] += [int(l[0]),int(l[1])]
        if rlist == []:
            rlist.append([n,[1,n]])
        if not h.find(id = 'twin_info'):
            table = h.find('table', id="puzzle0")
            wait = 0
            for i in range(n):
                for j in range(n):
                    try:
                        chunk_result = table.find(id = "p0r"+str(i)+"c"+str(j)).get_text()[1:]
                    except AttributeError:
                        continue
                    if chunk_result != '':
                        if chunk_result[-1] in '+-×:^':
                            rlist.append([[int(chunk_result[:-1]),chunk_result[-1]],(i,j)])
                        elif "mod" in chunk_result:
                            rlist.append([[int(chunk_result[:-4]),"mod"],(i,j)])
                        else:
                            rlist.append([[int(chunk_result),"_"],(i,j)])
                        wait = 0
                    else:
                        sty = table.find(id = "p0r"+str(i)+"c"+str(j)).get('style')
                        if not "border-top" in sty:
                            add_item(rlist,(i,j),(i-1,j))
                            for q in range(wait):
                                add_item(rlist,(i,j-q-1),(i-1,j))
                                wait = 0
                        elif not "border-left" in sty:
                            if wait == 0:
                                add_item(rlist,(i,j),(i,j-1))
                            else:
                                wait += 1
                        elif not "border-right" in sty:
                            wait += 1
                        else:
                            if j>1 and "border-left" in table.find(id = "p0r"+str(i)+"c"+str(j-1)).get('style') and "border-right" in table.find(id = "p0r"+str(i)+"c"+str(j-1)).get('style'):
                                add_item(rlist,(i,j),(i,j-2))
                            else:
                                print('ERROR, SHAPE UNDETECTABLE')
                                break
        else:
            for p in range(2):
                rlist.append([])
                table = h.find('table', id="puzzle"+str(p))
                wait = 0
                for i in range(n):
                    for j in range(n):

                        chunk_result = table.find(id = "p"+str(p)+"r"+str(i)+"c"+str(j)).get_text()[1:]
                        if chunk_result != '':
                            if chunk_result[-1] in '+-×:^':
                                rlist[p+1].append([[int(chunk_result[:-1]),chunk_result[-1]],(i,j)])
                            elif "mod" in chunk_result:
                                rlist[p+1].append([[int(chunk_result[:-4]),"mod"],(i,j)])
                            else:
                                rlist[p+1].append([[int(chunk_result),"_"],(i,j)])
                            wait = 0
                        else:
                            sty = table.find(id = "p"+str(p)+"r"+str(i)+"c"+str(j)).get('style')
                            if not "border-top" in sty:
                                add_item(rlist[p+1],(i,j),(i-1,j))
                                for q in range(wait):
                                    add_item(rlist[p+1],(i,j-q-1),(i-1,j))
                                    wait = 0
                            elif not "border-left" in sty:
                                if wait == 0:
                                    add_item(rlist[p+1],(i,j),(i,j-1))
                                else:
                                    wait += 1
                            elif not "border-right" in sty:
                                wait += 1
                            else:
                                if j>1 and "border-left" in table.find(id = "p"+str(p)+"r"+str(i)+"c"+str(j-1)).get('style') and "border-right" in table.find(id = "p"+str(p)+"r"+str(i)+"c"+str(j-1)).get('style'):
                                    add_item(rlist[p+1],(i,j),(i,j-2))
                                else:
                                    print('ERROR, SHAPE UNDETECTABLE')
                                    break
        return rlist
