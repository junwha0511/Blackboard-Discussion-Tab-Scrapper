from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
import time
import os 

def save_screenshot(driver, path):
    original_size = driver.get_window_size()
    required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(required_width, required_height)
    driver.find_element_by_tag_name('body').screenshot(path)  # avoids scrollbar
    driver.set_window_size(original_size['width'], original_size['height'])

id =  input('ID: ')
pw = input('PW: ')
discussionTab = input('Input The Address of Final Exam Session of Discussion Tab : ')
path = os.path.dirname(os.path.abspath( __file__ ))+'/chromedriver.exe'
driver = webdriver.Chrome(path)

driver.get('https://blackboard.unist.ac.kr')
time.sleep(1)
el = driver.find_element_by_class_name('button-1')
el.click()

time.sleep(1)
el = driver.find_element_by_id("user_id")
el.send_keys(id)
el = driver.find_element_by_id("password")
el.send_keys(pw)
el.send_keys(Keys.RETURN)
#https://blackboard.unist.ac.kr/webapps/discussionboard/do/forum?action=list_threads&course_id=_3810_1&nav=discussion_board_entry&conf_id=_4536_1&forum_id=_2834_1
driver.get(discussionTab)
soup = BeautifulSoup(driver.page_source, 'html.parser')
urls = [a['href'] for a in soup.find('tbody', {'id':'listContainer_databody'}).find_all('a')]
try:
    os.mkdir('./cps')
except:
    pass
qNum = 1
for u in urls:
    if u != '#contextMenu':
        driver.execute_script('javascript:expandAllMessagesInTheTree();')
        driver.get('https://blackboard.unist.ac.kr/webapps/discussionboard/do/'+u.replace('amp;',''))
        time.sleep(1)
        save_screenshot(driver, 'cps/'+str(qNum)+'.png')
        qNum += 1
driver.close()