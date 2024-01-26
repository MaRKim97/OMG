# OMG에 오신 여러분 환영합니다
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

categorys = ['action', 'comedy', 'drama', 'melo', 'horror','sf_fantasy', 'animation', 'documentary']

options = ChromeOptions()
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
df_titles = pd.DataFrame()
num = 0

for category in categorys:
    section_url = 'https://serieson.naver.com/v3/movie/products/{}?sortType=POPULARITY_DESC&price=all'.format(category)
    titles = []
    titles_real = []
    texts = []
    try:
        driver.get(section_url)
        time.sleep(0.5)
        for _ in range(35):
            driver.find_element('xpath', '//*[@id="content"]/div[2]/button').click()
            time.sleep(0.5)

    except:
        print('driver.get', category)
    for i in range(1000):
        try:
            title = driver.find_element('xpath', '//*[@id="content"]/div[1]/ul/li[{}]/a'.format(i)).get_attribute('href')
            print(title)
            driver1 = webdriver.Chrome(service=service, options=options)
            driver1.get(title)
            time.sleep(0.5)
            print(title)
            temp = driver1.find_element('xpath', '//*[@id="content"]/div[2]/div/div[1]/div[1]/strong').text
            titles_real.append(temp)
            text = driver1.find_element('xpath', '//*[@id="content"]/div[2]/ul/li[1]/div[3]/p').text
            text = re.compile('[^가-힇]').sub(' ', text)
            titles.append(title)
            texts.append(text)
            driver1.close()
        except:
            print('find element', category, i)
            driver1.close()


    df_section_titles = pd.DataFrame({'title':titles_real, 'text':texts})
    df_section_titles['category'] = categorys[num]
    num += 1
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)
df_titles.to_csv('./crawling_data/data.csv')

driver.close()
# print(texts)



# //*[@id="content"]/div[1]/ul/li[32]/a