from selenium import webdriver
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib import parse
from bs4 import BeautifulSoup as bs
import csv, re, os
# blogUrl = "https://section.blog.naver.com/ThemePost.nhn?directoryNo=27&activeDirectorySeq=3&currentPage=1"


# Q&A페이지 이동
def pageMoving(pageNoUrl):
    web_driver = webdriver.Chrome('./driver/ver85/chromedriver')
    web_driver.implicitly_wait(3)
    web_driver.get(pageNoUrl)

    with open('./blogCrawlingData.csv', 'a', encoding='utf-8', newline='') as writer_csv:
        writer = csv.writer(writer_csv, delimiter=',')
    # writer.writerow(["title", "blogurl", "writedate", "maincontant"])

        for blogNo in range(1, 11):
            web_driver.implicitly_wait(3)
            blogURL = web_driver.find_element_by_xpath("""//*[@id="content"]/section/div[2]/div[""" + str(blogNo) + """]/div/div[1]/div[1]/a[1]""").get_attribute('href')
            web_driver.get(blogURL)
            print(blogURL)
            iframes = web_driver.find_elements_by_tag_name("iframe")

            web_driver.switch_to.frame(iframes[0])



            # iframe내의 html 추출
            crawlingData, blogImageList = blogCrawling(web_driver.page_source, blogURL)
            writer.writerow(crawlingData)
            imageSave(blogImageList, crawlingData[0])

            print(pageNoUrl)
            web_driver.get(pageNoUrl)
            print('=' * 50)

    web_driver.close()

def blogCrawling(pageSource, blogURL):

    bsObject = bs(pageSource, "html.parser")
    # print(bsObject)

    pattern = re.compile(r'\n|\r')
    title = bsObject.find("div", {"class": "pcol1"})
    reTitle = re.sub(pattern, '', title.text)
    blogDate = bsObject.find("span", {"class": "se_publishDate pcol2"}).text
    blogMainContant = bsObject.find("div", {"class": "se-main-container"})
    blogImages = blogMainContant.find_all("img")
    blogImageList = []

    for blogImage in blogImages:
        url = blogImage.attrs['src']
        blogImageList.append(url)

    reBlogMainContant = re.sub(pattern, '', blogMainContant.text)

    crawlingData = [reTitle, blogURL, blogDate, reBlogMainContant]

    print(len(blogImageList))

    print("crawling save")
    return crawlingData, blogImageList

def imageSave(blogImageList, blogTitle):
    for i, blogImage in enumerate(blogImageList):
        if not os.path.exists('./imageData/' + blogTitle):
            os.makedirs('./imageData/' + blogTitle)
        try:
            urlretrieve(parse.quote(blogImage.encode('utf8'), '/:'), './imageData/'+ blogTitle + '/'+ blogTitle + str(i+1)+'.jpg')
        except:
            pass
    print("image save")


if __name__ == "__main__":

    # 블로그 게시판 페이지 이동
    for pageNo in range(1, 5):
        print(pageNo)
        print('='*50)
        pageMoving("https://section.blog.naver.com/ThemePost.nhn?directoryNo=27&activeDirectorySeq=3&currentPage=" + str(pageNo))



