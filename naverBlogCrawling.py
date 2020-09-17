from selenium import webdriver
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib import parse
from bs4 import BeautifulSoup as bs
import csv, re, os
# blogUrl = "https://section.blog.naver.com/ThemePost.nhn?directoryNo=27&activeDirectorySeq=3&currentPage=1"


# Q&A페이지 이동
def pageMoving(blogURLList):


    if os.path.isfile('./blogCrawlingData.csv') == False:
        with open('./blogCrawlingData.csv', 'a', encoding='utf-8', newline='') as writer_csv:
            writer = csv.writer(writer_csv, delimiter=',')
            writer.writerow(["title", "blogurl", "writedate", "maincontant"])

    with open('./blogCrawlingData.csv', 'a', encoding='utf-8', newline='') as writer_csv:
        writer = csv.writer(writer_csv, delimiter=',')



        # print(blogURLList)

        for blog_url in blogURLList:
            # iframe내의 html 추출
            web_driver.get(blog_url)
            iframes = web_driver.find_elements_by_tag_name("iframe")

            web_driver.switch_to.frame(iframes[0])

            # craling 데이터와 이미지데이터 반환
            crawlingData, blogImageList = blogCrawling(web_driver.page_source, blog_url)


            if crawlingData == None:
                print("오류블로그 : ", blog_url)
            else:
                writer.writerow(crawlingData)
                imageSave(blogImageList, crawlingData[0])

                # print(pageNoUrl)
                # web_driver.get(pageNoUrl)
                # print('=' * 50)

    web_driver.close()

def blogCrawling(pageSource, blogURL):

    bsObject = bs(pageSource, "html.parser")
    # print(bsObject)
    try:
        #정규식으로 공백제거
        pattern = re.compile(r'\n|\r')
        if bsObject.find("div", {"class": "pcol1"}) == None:
            title = bsObject.find("span", {"class": "pcol1 itemSubjectBoldfont"}).text
            reTitle = re.sub(pattern, '', title)
            blogDate = bsObject.find("p", {"class": "date fil5 pcol2 _postAddDate"}).text
            blogMainContant = bsObject.find("div", {"id": "postViewArea"})
        else:
            #타이틀 크로링
            title = bsObject.find("div", {"class": "pcol1"}).text
            reTitle = re.sub(pattern, '', title)
            # 날짜 크로링
            blogDate = bsObject.find("span", {"class": "se_publishDate pcol2"}).text
            # 블로그 본 크로링
            blogMainContant = bsObject.find("div", {"class": "se-main-container"})
        # 이미지주소 크로링
        blogImages = blogMainContant.find_all("img")
        blogImageList = []

        for blogImage in blogImages:
            url = blogImage.attrs['src']
            blogImageList.append(url)

        reBlogMainContant = re.sub(pattern, '', blogMainContant.text)

        crawlingData = [reTitle, blogURL, blogDate, reBlogMainContant]

        # print(len(blogImageList))

        # print("crawling save")
    except AttributeError as err:
        print(err)
        return None, None

    return crawlingData, blogImageList

#이미지 저장
def imageSave(blogImageList, blogTitle):
    title = re.sub('/', '', blogTitle)
    for i, blogImage in enumerate(blogImageList):
        if not os.path.exists('./imageData/' + title):
            os.makedirs('./imageData/' + title)
        # 한글포함된 URL 예외코드
        try:
            urlretrieve(blogImage, './imageData/'+ title + '/'+ title + str(i+1)+'.jpg')
        except UnicodeEncodeError:
            urlretrieve(parse.quote(blogImage.encode('utf8'), '/:'), './imageData/'+ title + '/'+ title + str(i+1)+'.jpg')
    # print("image save")


if __name__ == "__main__":
    web_driver = webdriver.Chrome('./driver/ver85/chromedriver')
    web_driver.implicitly_wait(3)

    blogURLList = []

    # 블로그 게시판 페이지 URL 수집
    for pageNo in range(1, 51):
        # print(pageNo,'='*50)
        web_driver.get("https://section.blog.naver.com/ThemePost.nhn?directoryNo=27&activeDirectorySeq=3&currentPage=" + str(pageNo))

        for blogNo in range(1, 11):
            web_driver.implicitly_wait(3)
            blogURL = web_driver.find_element_by_xpath("""//*[@id="content"]/section/div[2]/div[""" + str(blogNo) + """]/div/div[1]/div[1]/a[1]""").get_attribute('href')
            blogURLList.append(blogURL)

    pageMoving(blogURLList)

    # for i in blogURLList:
    #     print(i)




