# OMG에 오신 여러분 환영합니다
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re
import time
import datetime

options = ChromeOptions()
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

categories = ['action', 'comedy', 'drama', 'melo', 'horror', 'sf_fantasy', 'animation', 'documentary']
df_titles = pd.DataFrame()

# ↓ 시리즈온에서 제목, 줄거리, 카테고리를 포함한 데이터 크롤링 작업 ↓
for category in categories:
    section_url = 'https://serieson.naver.com/v3/movie/products/{}?sortType=POPULARITY_DESC&price=all'.format(category)
    titles = []
    movie_titles = []
    movie_synopsis = []
    try:
        driver.get(section_url)
        time.sleep(0.5)
    except:
        print('driver.get', category)

    for j in range(33):
        # ↓ 더보기 클릭 ↓
        driver.find_element('xpath', '//*[@id="content"]/div[2]/button').click()
        time.sleep(0.5)
        for i in range(j*30+1, j*30+31):
            one_movie_driver = webdriver.Chrome(service=service, options=options)
            try:
                # ↓ 영화 제목 및 줄거리 크롤링 ↓
                movie_url = driver.find_element('xpath', '//*[@id="content"]/div[1]/ul/li[{}]/a'.format(i)).get_attribute('href')
                one_movie_driver.get(movie_url)
                time.sleep(0.5)

                title = one_movie_driver.find_element('xpath', '//*[@id="content"]/div[2]/div/div[1]/div[1]/strong').text

                text = one_movie_driver.find_element('xpath', '//*[@id="content"]/div[2]/ul/li[1]/div[3]/p').text
                text = re.compile('[^가-힇]').sub(' ', text)

                movie_titles.append(title)
                movie_synopsis.append(text)

                one_movie_driver.close()
            except:
                movie_titles.append('NULL')
                movie_synopsis.append('NULL')
                print('find element', category, i)
                one_movie_driver.close()


        df_section_titles = pd.DataFrame()
        df_section_titles["title"] = movie_titles
        df_section_titles["synopsis"] = movie_synopsis
        df_section_titles["category"] = category

        df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)
        df_titles.to_csv('./crawling_data/data_animation_{}.csv'.format(j*30+1))
        df_titles = pd.DataFrame()
        titles = []
        movie_titles = []
        movie_synopsis = []

driver.close()
