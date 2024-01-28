import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

link_to_auction = 'https://miamidade.realforeclose.com/index.cfm?zaction=AUCTION&zmethod=PREVIEW&AuctionDate=01/08/2024'
chrome_driver_path = 'Chrome_driver\chromedriver.exe'
service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome()
driver.get(link_to_auction)
time.sleep(5)

my_dict = {}

List_1 = []
pages = driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td[2]/div[3]/div[4]/div[3]/span[2]/span')
pages_num = int(pages.text)


def get_data_structure():
    Labels = driver.find_elements(By.CLASS_NAME, value="AD_LBL")
    Datas = driver.find_elements(By.CLASS_NAME, value="AD_DTA")
    lbl = [i.text for i in Labels]
    dta = [i.text for i in Datas]
    for (key, value) in zip(lbl, dta):
        my_dict[key] = []
    next_page = driver.find_element(By.XPATH, "/html/body/table/tbody/tr/td[2]/div[3]/div[4]/div[6]/span[3]/img")
    next_page.click()
    time.sleep(5)


def get_data():
    Labels = driver.find_elements(By.CLASS_NAME, value="AD_LBL")
    Datas = driver.find_elements(By.CLASS_NAME, value="AD_DTA")
    lbl = [i.text for i in Labels]
    dta = [i.text for i in Datas]
    for (key, value) in zip(lbl, dta):
        my_dict[key].append(value)
    next_page = driver.find_element(By.XPATH, "/html/body/table/tbody/tr/td[2]/div[3]/div[4]/div[6]/span[3]/img")
    next_page.click()
    time.sleep(5)


for _ in range(2):
    get_data_structure()
print(my_dict)

page_num = driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td[2]/div[3]/div[4]/div[6]/span[2]/input')
page_num.send_keys(Keys.BACKSPACE)
page_num.send_keys(1)
page_num.send_keys(Keys.ENTER)
time.sleep(3)

for _ in range(pages_num):
    get_data()

page_num = driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td[2]/div[3]/div[4]/div[6]/span[2]/input')
page_num.send_keys(Keys.BACKSPACE)
page_num.send_keys(1)
page_num.send_keys(Keys.ENTER)
time.sleep(3)
holding = []
for i in my_dict['Property Address:']:
    u = i + ' ' + my_dict[''][my_dict['Property Address:'].index(i)]
    holding.append(u)
my_dict['Property Address:'] = holding
del my_dict['']


def get_frame_of_data():
    global List_1
    time.sleep(5)
    a = driver.find_elements(By.CSS_SELECTOR, value=".ad_tab tbody")
    for v in a:
        List_1.append(v.text)
    next_page = driver.find_element(By.XPATH, "/html/body/table/tbody/tr/td[2]/div[3]/div[4]/div[6]/span[3]/img")
    next_page.click()


for n in range(pages_num):
    get_frame_of_data()
List_2 = []
for i in List_1:
    i = i.replace('\n', ':')
    List_2.append(i.split(':'))

for i in List_2:

    if not 'Assessed Value' in i:
        my_dict['Assessed Value:'].insert(List_2.index(i), 'N/A')

    if not 'Property Address' in i:
        my_dict['Property Address:'].insert(List_2.index(i), 'N/A')

name = input('Name Your CSV file:\n')
data = pd.DataFrame(my_dict)
data.to_csv(f'{name}.csv')

driver.quit()
