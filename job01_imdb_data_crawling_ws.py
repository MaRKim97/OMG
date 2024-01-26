from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchDriverException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

driver = webdriver.Chrome()
options = ChromeOptions()

category = ['action', 'animation', 'comedy', 'crime', 'drama',
          'fantasy', 'romance', 'war', 'thriller']

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
genres = ['action', 'animation', 'comedy', 'crime', 'drama',
          'fantasy', 'romance', 'war', 'thriller']

df_titles = pd.DataFrame()
df_plots = pd.DataFrame()


for genre in genres:
    section_url = 'https://www.imdb.com/search/title/?title_type=feature&genres={}&sort=num_votes,desc'.format(genre)
    driver.get(section_url)
    titles = []
    plots = []
    for i in range(51):
        driver.find_element('xpath',
                            '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/div[2]/div/span/button')
        time.sleep(0.5)
