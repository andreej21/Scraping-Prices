from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62'
PATH = 'C:\webdrivers\msedgedriver.exe'
edge_options = Options()
edge_options.add_experimental_option("detach",True)
edge_options.add_experimental_option("excludeSwitches", ["enable-logging"])
edge_options.add_argument(f'user_agent={user_agent}')
edge_service = Service(PATH)
driver = webdriver.Edge(options=edge_options,service=edge_service)

driver.get('https://gjirafa50.mk/shto-ima-novo')

i = 0

while i < 11:
    i+=1
    try:
        driver.find_element(By.XPATH,'/html/body/div[6]/div[4]/div/div[2]/div/div/div[2]/button').click()
        time.sleep(2)
    except:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        pass
        time.sleep(3)


items = driver.find_element(By.XPATH,'/html/body/div[6]/div[4]/div/div[2]/div/div/div[1]/div[2]/div[2]/div[1]') 

all_items = items.find_elements(By.XPATH,'div[@class="item-box"]')

item_names = []
item_prices = []
item_ids = []
item_discounts_percent = []
for item in all_items:
    item_name=item.find_element(By.XPATH,'.//a[@class="text-sm md:text-base product-title-lines hover:underline"]').text
    item_names.append(item_name)
    

    item_price = item.find_element(By.XPATH,'div/div[3]/div[1]/span[@class="price font-semibold text-gray-700 text-base md:text-xl"]').get_attribute('innerText')
    item_prices.append(item_price)


    item_id = item.find_element(By.XPATH,'./div').get_attribute("data-productid")
    item_ids.append(item_id)
    

    try:
        item_discount = item.find_element(By.XPATH,'./div/div[1]/div[@class="w-12 h-6 bg-primary discount__label flex justify-center items-center rounded absolute right-2 top-0"]/span').get_attribute('innerText')
        item_discounts_percent.append(item_discount)
    except:
        item_discounts_percent.append('No discount')



item_data  = pd.DataFrame({'ID':item_ids,
'Product':item_names,
'Price':item_prices,
'Discount':item_discounts_percent})

item_data.to_excel('Gjirafa50.xlsx',index=False)