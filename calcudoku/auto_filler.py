from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
#driver initialize
driver = webdriver.Chrome() #open Chrome
driver.maximize_window()    #max window
wait = WebDriverWait(driver,10)
actions = ActionChains(driver)
def fill_in(d,li):
    for i in range(len(li)):
        for j in range(len(li)):
            e = d.find_element_by_id("p0r"+str(i)+'c'+str(j))
            e.click()
            actions.send_keys(str(li[i][j]))
            actions.perform()
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
#fill in
url_list = ['https://www.calcudoku.org/en/']
for i in driver.find_elements_by_class_name("newtab"):
    url = i.get_attribute("onclick")
    print(url[url.find('\'')+1:url.rfind('\'')])
    url_list.append(url[url.find('\'')+1:url.rfind('\'')])
for i in url_list:
    driver.get(i)
    wait.until(EC.presence_of_element_located((By.ID,'inner_container')))
    '''
    list = SOLVE[i]
    +
    Killer/Sudoku/Twin判定
    '''
    time.sleep(3)
    fill_in(driver,list1)
