# OMG에 오신 여러분 환영합니다
import numpy as np
from selenium import webdriver # selenium: 웹 애플리케이션 테스팅을 위한 프레임워크
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
# webdriver_manager라이브러리를 사용하면 현재 시스템의 Chrome 버전에 알맞은 ChromeDriver를 자동으로 다운로드하고 사용 할 수 있다
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

options = ChromeOptions()
service = ChromeService(executable_path=ChromeDriverManager().install())
# executable_path: 웹 드라이버 절대경로로 호출
driver = webdriver.Chrome(service=service, options=options)
# 크롬 드라이버 생성 / ChromeDriver는 Selenium이 명령을 내리면 Chrome브라우저에 전달을 하기 위한 중재자 역할을 한다.


categories = ['drama']

df_titles = pd.DataFrame()

for category in categories:
    section_url = 'https://serieson.naver.com/v3/movie/products/{}?sortType=POPULARITY_DESC&price=all'.format(category)
    titles = []
    movie_titles = []
    movie_synopsis = []
    try:
        driver.get(section_url) # section_url의 주소를 열겠다라는 의미
        time.sleep(0.5) # 열리는 시간 기다림

    except:
        print('driver.get', category)


    for j in range(33):
        driver.find_element('xpath', '//*[@id="content"]/div[2]/button').click() # 더보기 버튼(태그의 경로) 클릭
        time.sleep(0.5) # 열리는 시간 기다림

        for i in range(j*30+1, j*30+31):
            one_movie_driver = webdriver.Chrome(service=service, options=options)
            try:
                movie_url = driver.find_element('xpath', '//*[@id="content"]/div[1]/ul/li[{}]/a'.format(i)).get_attribute('href')
                # get_attribute: 요소에 지정된 속성값을 반환
                # href="/v2/movie/610671"
                print(movie_url)
                one_movie_driver.get(movie_url)
                time.sleep(0.5)


                title = one_movie_driver.find_element('xpath', '//*[@id="content"]/div[2]/div/div[1]/div[1]/strong').text

                print(title, i) # 오류 위치 확인

                text = one_movie_driver.find_element('xpath', '//*[@id="content"]/div[2]/ul/li[1]/div[3]/p').text
                text = re.compile('[^가-힇]').sub(' ', text)

                print('text', i) # 오류 위치 확인
                movie_titles.append(title)
                movie_synopsis.append(text)
                one_movie_driver.close()
            except:
                # 19금 영화는 따로 분류?
                movie_titles.append('NULL')
                movie_synopsis.append('NULL')
                print('find element', category, i)
                # try:
                #     text = one_movie_driver.find_element('xpath', '//*[@id="content"]/div[2]/ul/li[1]/div[2]/p').text
                #     text = re.compile('[^가-힇]').sub(' ', text)
                #     movie_synopsis.append(text)
                #     print('find element', category, i)
                # except:
                #     movie_synopsis.append('NULL')
                #     print('real NULL', category, i)
                one_movie_driver.close()

        print('debug03')
        df_section_titles = pd.DataFrame()
        print(len(movie_titles))
        print(len(movie_synopsis))
        df_section_titles["title"] = movie_titles
        df_section_titles["synopsis"] = movie_synopsis
        df_section_titles["category"] = category
        print('debug04')

        df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)
        print('debug05')
        # concat: 여러개의 동일한 DataFrame합치기
        # ignore_index: 기존 index무시
        df_titles.to_csv('./crawling_data/data_animation_{}.csv'.format(j*30+1))
        print('debug06')

        df_titles = pd.DataFrame()
        titles = []
        movie_titles = []
        movie_synopsis = []


driver.close()