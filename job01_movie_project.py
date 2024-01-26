# OMG에 오신 여러분 환영합니다
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

categories = ['melo']

options = ChromeOptions()
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
df_titles = pd.DataFrame()
num = 0

for category in categories:
    section_url = 'https://serieson.naver.com/v3/movie/products/{}?sortType=POPULARITY_DESC&price=all'.format(category)
    titles = []
    titles_real = []
    texts = []
    try:
        driver.get(section_url)
        time.sleep(0.5)
        # for _ in range(35):
        #     driver.find_element('xpath', '//*[@id="content"]/div[2]/button').click()
        #     time.sleep(0.5)

    except:
        print('driver.get', category)

    for j in range(33):
        driver.find_element('xpath', '//*[@id="content"]/div[2]/button').click()
        time.sleep(0.5)
        for i in range(j*30+1, j*30+31):
            driver1 = webdriver.Chrome(service=service, options=options)
            try:
                title = driver.find_element('xpath', '//*[@id="content"]/div[1]/ul/li[{}]/a'.format(i)).get_attribute('href')
                print(title)
                driver1.get(title)
                time.sleep(0.5)
                temp = driver1.find_element('xpath', '//*[@id="content"]/div[2]/div/div[1]/div[1]/strong').text
                titles_real.append(temp)
                # titles.append(title)
                text = driver1.find_element('xpath', '//*[@id="content"]/div[2]/ul/li[1]/div[3]/p').text
                text = re.compile('[^가-힇]').sub(' ', text)
                texts.append(text)
                driver1.close()
            except:
                try:
                    text = driver1.find_element('xpath', '//*[@id="content"]/div[2]/ul/li[1]/div[2]/p').text
                    text = re.compile('[^가-힇]').sub(' ', text)
                    texts.append(text)
                    print('find element', category, i)
                except:
                    texts.append('NULL')
                    titles_real.append('NULL')
                    print('real NULL', category, i)
                driver1.close()

        # print(len(titles_real))
        # print(len(texts))
        df_section_titles = pd.DataFrame()
        df_section_titles["title"] = titles_real
        df_section_titles["text"] = texts
        df_section_titles["category"] = category

        # df_section_titles = pd.DataFrame({'title':titles_real, 'text':texts, 'category':categories})
        df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)
        df_titles.to_csv('./crawling_data/data_melo{}.csv'.format(num))
        num += 30

driver.close()
# print(texts)

# //*[@id="content"]/div[2]/ul/li[1]/div[2]/p

# //*[@id="content"]/div[1]/ul/li[32]/a

# for i in range(33)
#     for j in range(i*30+1, i*30+31)