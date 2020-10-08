from selenium import webdriver
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib import parse
from bs4 import BeautifulSoup as bs
import csv, re, os


# blogUrl = "https://section.blog.naver.com/ThemePost.nhn?directoryNo=27&activeDirectorySeq=3&currentPage=1"


# Q&A페이지 이동
def pageMoving():
    blogURLList = ["https://blog.naver.com/kbbang81/222088873024", "https://blog.naver.com/jeju3377/222089726112", "https://blog.naver.com/kbbang81/222088873024", "https://blog.naver.com/kbbang81/222088873024", "https://blog.naver.com/kbbang81/222088873024"]


    web_driver = webdriver.Chrome('./driver/ver85/chromedriver')
    web_driver.implicitly_wait(3)
    for blogurl in blogURLList:
        web_driver.get(blogurl)

        iframes = web_driver.find_elements_by_tag_name("iframe")

        web_driver.switch_to.frame(iframes[0])

        # iframe내의 html 추출

        crawlingData, blogImageList = blogCrawling(web_driver.page_source, blogurl)
        print(type(crawlingData),'====',crawlingData)
        print(type(blogImageList),'====',blogImageList)


        if crawlingData == None:
            print("오류블로그 : ", blogurl)
        else:
            print(crawlingData[0])
            print("=" * 50)
            print(crawlingData[1])
            print("=" * 50)
            print(crawlingData[2])
            print("=" * 50)
            print(crawlingData[3])
            print("=" * 50)
            print(blogImageList)

        print('=' * 50)

    web_driver.close()


def blogCrawling(pageSource, blogURL):
    bsObject = bs(pageSource, "html.parser")
    # print(bsObject)
    try:
        pattern = re.compile(r'\n|\r')
        title = bsObject.find("div", {"class": "pcol1"}).text
        reTitle = re.sub(pattern, '', title)
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
    except AttributeError:

        return None, None

    return crawlingData, blogImageList


def imageSave(blogImageList, blogTitle):
    title = re.sub('/', '', blogTitle)
    for i, blogImage in enumerate(blogImageList):
        if not os.path.exists('./imageData/' + title):
            os.makedirs('./imageData/' + title)
        try:
            urlretrieve(parse.quote(blogImage.encode('utf8'), '/:'),
                        './imageData/' + title + '/' + title + str(i + 1) + '.jpg')
        except:
            pass
    print("image save")


if __name__ == "__main__":

    pageMoving()



