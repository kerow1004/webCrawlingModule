import sys
import os
import pandas as pd
import numpy as np
import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import tqdm
from tqdm.notebook import tqdm

from selenium.webdriver.common.keys import Keys
from selenium import webdriver

def get_url(FileName, tmp_time):
    query_txt = input('1.크롤링할 키워드는 무엇입니까?: ')

    # 검색 파트

    path = "chromedriver.exe"

    driver = webdriver.Chrome(path)

    driver.get('https://brunch.co.kr/')
    time.sleep(2)

    hidden_submenu = driver.find_element_by_css_selector('#btnServiceMenuSearch')

    actions = webdriver.ActionChains(driver)
    actions.click(hidden_submenu)

    actions.perform()

    time.sleep(2)

    user_search = driver.find_element_by_id("txt_search")

    user_search.clear()
    user_search.send_keys(query_txt)
    user_search.send_keys(Keys.RETURN)


    SCROLL_PAUSE_TIME = 2

    # 스크롤 파트 - 우선 30초, 수정 필요
    last_height = driver.execute_script("return document.body.scrollHeight")         

    start_time = time.time()
    while True:
        # Scroll down to bottom                                                      
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)                                              
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")  
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height           
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:                                               
            break
        
        last_height = new_height

        if time.time() - start_time >= tmp_time:
            break
        
    # 스크롤한 경과 나온 제목의 개수    
    page_cnt = len(driver.find_elements_by_class_name('tit_subject'))
    
    print("크롤링한 URL의 개수:", page_cnt)

    time.sleep(1)

    title = []
    url = []

    for i in range(1,page_cnt):
        num = '[' + str(i) + ']'
        a_path = '//*[@id="resultArticle"]/div/div[1]/div[2]/ul/li'+num+'/a'
        title_path = '//*[@id="resultArticle"]/div/div[1]/div[2]/ul/li'+num+'/a/div[1]/strong'
        tmp_title = driver.find_element_by_xpath(title_path)
        titles = tmp_title.text
        
        
        tmp_url = driver.find_element_by_xpath(a_path)
        urls = tmp_url.get_attribute("href")
        
        title.append(titles)
        url.append(urls)


    # dataframe 으로 제목, url 저장
    df = pd.DataFrame({'url':url, 'title':title})

    df.to_excel(FileName+'.xlsx')
