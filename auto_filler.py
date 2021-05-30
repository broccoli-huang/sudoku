from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import subprocess
import os
#driver initialize
driver = webdriver.Chrome() #open Chrome
driver.maximize_window()    #max window
wait = WebDriverWait(driver,10)
actions = ActionChains(driver)
wd = os.getcwd()
def fill_in(d,li):
	for i in range(len(li)):
		for j in range(len(li)):
			actions.reset_actions()
			e = d.find_element_by_id("p0r"+str(i)+'c'+str(j))
			e.click()
			actions.send_keys(str(li[i][j]))
			actions.perform()
	time.sleep(2)
	return 0
#read "login_info.txt" for alias and password
txt = open("login_info.txt",'r')
alias = txt.readline()[:-1]
password = txt.readline()[:-1]
txt.close()
#login
driver.get("https://www.calcudoku.org/ops/login/en")
e_alias = wait.until(EC.presence_of_element_located((By.ID,'alias')))
e_password = driver.find_element_by_id("password")
e_alias.send_keys(alias)
e_password.send_keys(password)
driver.find_element_by_id("login_button").click()
wait.until(EC.presence_of_element_located((By.ID,'inner_container')))
#fill in
url_list = ['https://www.calcudoku.org/en/\n']
for i in driver.find_elements_by_class_name("newtab"):
	url = i.get_attribute("onclick")
	try:
	    print(url[url.find('\'')+1:url.rfind('\'')])
	    url_list.append(url[url.find('\'')+1:url.rfind('\'')]+'\n')
	except AttributeError:
	    continue
for i in url_list:
	list1 = []
	driver.get(i)
	wait.until(EC.presence_of_element_located((By.ID,'inner_container')))
	if 'for subscribers only' in driver.find_element_by_id('puzzles').get_attribute("innerText"):
		continue
	elif 'Killer' in driver.find_element_by_id("puzzle_rating_info").get_attribute("innerText"):
		os.chdir('./killer')
		p1 = subprocess.Popen(['python3', 'tocnf.py'],stdin=subprocess.PIPE)
		p1.communicate(input=i.encode('utf-8'))
		p2 = subprocess.run(['minisat', 'killer.cnf', 'solution.txt'])
		p3 = subprocess.run(['python3', 'final.py'], capture_output = True)
		result = str(p3.stdout.decode('utf-8'))
		list0 =result.split(' \n')
		for j in list0[:-1]:
			list1.append(j.split(' '))
		os.chdir(wd)
	elif 'Sudoku' in driver.find_element_by_id("puzzle_rating_info").get_attribute("innerText"):
		continue
	else:
		try:
			driver.find_element_by_id('twin_info')
			continue
		except NoSuchElementException:
			pass
		os.chdir('./calcudoku')
		p1 = subprocess.Popen(['python3', 'begin.py'],stdin=subprocess.PIPE)
		p1.communicate(input=i.encode('utf-8'))
		p2 = subprocess.Popen(['./abc'],stdin=subprocess.PIPE)
		p2.communicate(input='read_eqn begin.eqn\nstrash\nwrite_eqn middle.eqn'.encode('utf-8'))
		time.sleep(5)
		p2.terminate()
		p3 = subprocess.run(['python3', 'middle.py'])
		p4 = subprocess.run(['minisat', 'middle.cnf', 'solution.txt'])
		p5 = subprocess.run(['python3', 'end.py'], capture_output = True)
		result = str(p5.stdout.decode('utf-8'))
		list0 =result.split(' \n')
		for j in list0[:-1]:
			list1.append(j.split(' '))
		os.chdir(wd)
	time.sleep(5)
	fill_in(driver,list1)
