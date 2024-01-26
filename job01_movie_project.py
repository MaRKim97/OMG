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

categorys = ['action']

options = ChromeOptions()
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


df_titles = pd.DataFrame()
for category in categorys:
    section_url = 'https://serieson.naver.com/v3/movie/products/{}?sortType=UPDATE_DESC&price=all'.format(category)
    titles = []
    texts = []
    try:
        driver.get(section_url)
        time.sleep(0.5)
    except:
        print('driver.get', category)

    for i in range(2, 4):
        try:
            title = driver.find_element('xpath', '//*[@id="content"]/div[1]/ul/li[{}]/a'.format(i)).get_attribute('href')
            print(title)
            driver1 = webdriver.Chrome(service=service, options=options)
            driver1.get(title)
            time.sleep(0.5)
            print(title)
            text = driver1.find_element('xpath', '//*[@id="content"]/div[2]/ul/li[1]/div[3]/p').text
            texts.append(text)
            print(texts)
            driver1.close()
        except:
            print('find element', category, i)
driver.close()