from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import re

# blogUrl = ["https://blog.naver.com/kspak56/222091720797"]
blogUrl = ["https://blog.naver.com/madforsea/221599848467", "https://blog.naver.com/man9855/222091707584", "https://blog.naver.com/eriogena/222091698014", "https://blog.naver.com/roaltlf/222080818752", "https://blog.naver.com/ksb115205/222091689941", "https://blog.naver.com/ksb115205/222091689941", "https://blog.naver.com/kdsdb/222091711487", "https://blog.naver.com/ximetal/222090869712", "https://blog.naver.com/dambi18/222091565231", "https://blog.naver.com/myday2227/222091497863", "https://blog.naver.com/bsj880502/222091481245", "https://blog.naver.com/jeju3377/222091647116", "https://blog.naver.com/cuperman/222090005878", "https://blog.naver.com/pcrock/222089770358", "https://blog.naver.com/rockyu205/222082339705", "https://blog.naver.com/rockyu205/222082339705"]
web_driver = webdriver.Chrome('./driver/ver85/chromedriver')
web_driver.implicitly_wait(3)
for url in blogUrl:
    web_driver.get(url)



    iframes = web_driver.find_elements_by_tag_name("iframe")
    web_driver.switch_to.frame(iframes[0])

    #iframe내의 html 추출
    pageSource = web_driver.page_source
    try:
        pattern = re.compile(r'\n|\r')
        bsObject = bs(pageSource, "html.parser")
        if bsObject.find("div", {"class": "pcol1"}) == None:
            title = bsObject.find("span", {"class": "pcol1 itemSubjectBoldfont"}).text
            title = re.sub(pattern, '', title)
            blogDate = bsObject.find("p", {"class": "date fil5 pcol2 _postAddDate"}).text
            blogMainContant = bsObject.find("div", {"id": "postViewArea"})
        else:
            title = bsObject.find("div", {"class": "pcol1"}).text
            title = re.sub(pattern, '', title)
            blogDate = bsObject.find("span", {"class": "se_publishDate pcol2"}).text
            blogMainContant = bsObject.find("div", {"class": "se-main-container"})

        blogImages = blogMainContant.find_all("img")
        blogImageList = []

        for blogImage in blogImages:
            url = blogImage.attrs['src']
            blogImageList.append(url)

        blogMainContant = re.sub(pattern, '', blogMainContant.text)

        print(title)
        print("=" * 50)
        print(blogUrl)
        print("=" * 50)
        print(blogDate)
        print("=" * 50)
        print(blogMainContant)
        print("=" * 50)
        print(blogImageList)
    except AttributeError:

        pass



web_driver.close()