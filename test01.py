from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchDriverException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime
import requests
from bs4 import BeautifulSoup

category = ['Action', "Comedy", 'Drama', 'Melo', 'Thriller', 'Fantasy',
            'Animation', 'Documentary']
options = ChromeOptions()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
options.add_argument('user_agent=' + user_agent)
options.add_argument('lang=ko_KR')
#headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}


service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
genres = ['action', 'comedy', 'drama', 'horror', 'sf_fantasy', 'animation', 'documentary']
df_titles = pd.DataFrame()

for genre in genres:
    url = 'https://serieson.naver.com/v3/movie/products/{}?sortType=UPDATE_DESC&price=all'.format(genre)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    title_tags = soup.select('.sh_text_headline')
    titles = []
    # for title_tag in title_tags:
    #     titles.append(re_title.sub(' ', title_tag.text))
    # df_section_titles = pd.DataFrame(titles, columns=['titles'])
    # df_section_titles['category'] = category[i]
    # df_titles = pd.concat([df_titles, df_section_titles], axis = 'rows',
    #                       ignore_index=True)