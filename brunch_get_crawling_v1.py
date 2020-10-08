from brunch_get_url_v1 import get_url

import requests
from bs4 import BeautifulSoup
import urllib.request as req
import urllib
import re
import os
import pandas as pd
import time

def get_crawling(data):
    dict = {}  # 전체 크롤링 데이터를 담을 그릇

    # Aug 08.12 이런식으로 날짜가 출력되서 변환할 dict
    month_dict = {'Jan':1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}

    number = len(data)

    for i in range(0, number): 
        # 글 띄우기
        url = data['url'][i]
        res = req.urlopen(url)
        soup = BeautifulSoup(res, "html.parser")
        # 크롤링
        
        try : 

            target_info = {}
            
            # 제목 크롤링 시작
            title = soup.find('title').text
            
            # 글쓴이 크롤링 시작
            writers = soup.select('span > a')
            tmp_writer = []
            for name in writers:
                tmp_writer.append(name.text)
            writer = tmp_writer[0]
            del tmp_writer, writers

            # 날짜 크롤링
            date = soup.find(class_='f_l date').text
            if date[:3] in month_dict:
                month = month_dict[date[:3]]
            day = date.split(" ")[1]
            year = date.split(" ")[2]
            days = str(year)+"."+str(month)+"."+str(day)
            
            
            # 내용 크롤링
            contents = soup.select('p')
            contents
            tmp_content = []
            for content in contents:
                tmp_content.append(content.text)

            tmp = ' '.join(tmp_content)
            tmp = tmp.replace('  ',' ')
            tmp = tmp.replace('You can make anythingby writing - C.S.Lewis - ','')
            contents = tmp
            
            # 이미지 크롤링
            try:
                if not(os.path.isdir(title)):
                    os.makedirs(os.path.join(title))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    print("Failed to create directory!")
                    raise

            images = soup.select("div > img")
            img_list = []
            cnt = 0

            for img in images:
                src = 'https:'+img['src']
                urllib.request.urlretrieve(src, './'+title+'/'+str(i)+'_'+str(cnt)+'.jpg')
                cnt+=1
        
            target_info['writer'] = writer
            target_info['datetime'] = days
            target_info['title'] = title
            target_info['content'] = contents
            
            dict[i] = target_info
            time.sleep(1)
            
            print(writer, days, title, contents[:10], "사진수:",cnt)
            
            if i % 10 == 0:
                reuslt_df = pd.DataFrame.from_dict(dict, 'index')
                reuslt_df.to_excel('brunch_crawling_test.xlsx')
                time.sleep(3)
            
        
        # 에러나면 현재 크롬창 닫고 다음 글(i+1)로 이동
        except:
            time.sleep(1)
            continue
            
    result_df = pd.DataFrame.from_dict(dict, 'index')
    result_df.to_excel('brunch_crawling_v1.xlsx')


try:
    url_load = pd.read_excel("brunch_blog_url2.xlsx")
except FileNotFoundError:
    print("파일을 찾을 수 없습니다.")
    data = input("저장하고자 하는 파일명을 입력해주세요.")
    tmp_time = input("크롤링할 시간을 입력해주세요.")
    get_url(data, int(tmp_time))
    data = pd.read_excel(data+".xlsx")
    get_crawling(data)