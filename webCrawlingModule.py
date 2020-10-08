from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib import parse
from bs4 import BeautifulSoup as bs
import csv, re, os, datetime, platform
import pandas as pd

class Crawler:
    def __init__(self, blogURL, page_source):
        self.blogURL = blogURL
        self.page_source = page_source

    def selenium_crawling(self):
        osName = platform.system()
        driverPathVer = './driver/ver85'

        if (osName == 'Windows'):
            chromeDriver = "chromedriver.exe"
            web_driver = webdriver.Chrome(os.path.join(driverPathVer, 'windows',chromeDriver))
        elif (osName == 'Linux'):
            chromeDriver = "chromedriver"
            web_driver = webdriver.Chrome(os.path.join(driverPathVer, 'linux',chromeDriver))
        else:
            chromeDriver = "chromedriver"
            web_driver = webdriver.Chrome(os.path.join(driverPathVer, 'mac',chromeDriver))


        web_driver.implicitly_wait(3)
        # iframe내의 html 추출
        web_driver.get(self.blogURL)
        iframes = web_driver.find_elements_by_tag_name("iframe")

        web_driver.switch_to.frame(iframes[0])

        # craling 데이터와 이미지데이터 반환
        crawlingData, blogImageList = self.beautifulsoupcrawling(web_driver.page_source, self.blogURL)


        if crawlingData == None:
            print("오류블로그 : ", self.blogURL)
            return None
        else:
            return crawlingData
            # imageSave(blogImageList, crawlingData[0])


    def beautifulsoupcrawling(self, titleTag, titleClassValue, dateTag, dateClassValue, contantTag, contantClassValue):
        bsObject = bs(self.page_source, "html.parser")

        today = datetime.datetime.today()
        # print(bsObject)
        try:
            #정규식으로 공백제거
            pattern = re.compile(r'\n|\r')
            if bsObject.find(titleTag, {"class": titleClassValue}) == None:
                #타이틀 크로링
                title = bsObject.find("span", {"class": "pcol1 itemSubjectBoldfont"}).text
                reTitle = re.sub(pattern, '', title)
                # 날짜 크로링
                blogDate = bsObject.find("p", {"class": "date fil5 pcol2 _postAddDate"}).text
                # if not len(blogDate.split('시간')) == 1:
                #     blogDate = today - datetime.timedelta(hours=int(blogDate.split('시간')[0]))
                # 블로그 본 크로링
                blogMainContant = bsObject.find("div", {"id": "postViewArea"})
            else:
                #타이틀 크로링
                title = bsObject.find(titleTag, {"class": titleClassValue}).text
                reTitle = re.sub(pattern, '', title)
                # 날짜 크로링
                blogDate = bsObject.find(dateTag, {"class": dateClassValue}).text

                # if not len(blogDate.split('시간')) == 1:
                #     blogDate = today - datetime.timedelta(hours=int(blogDate.split('시간')[0]))

                # 블로그 본 크로링
                blogMainContant = bsObject.find(contantTag, {"class": contantClassValue})
            # 이미지주소 크로링
            blogImages = blogMainContant.find_all("img")
            blogImageList = []

            for blogImage in blogImages:
                url = blogImage.attrs['src']
                blogImageList.append(url)

            reBlogMainContant = re.sub(pattern, '', blogMainContant.text)

            crawlingData = [reTitle, self.blogURL, blogDate, reBlogMainContant]

            # print(len(blogImageList))

            # print("crawling save")
        except AttributeError as err:
            print(err)
            return None, None

        except UnexpectedAlertPresentException as err:
            print(err)
            return None, None

        return crawlingData, blogImageList