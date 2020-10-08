from selenium import webdriver
import csv, os, datetime

today = datetime.datetime.today()
today = today.strftime('%Y%m%d')

# 블로그 게시판 페이지 URL 수집.
def blogURLCrawling():
    blogURLList = []
    for pageNo in range(1, 51):
        # print(pageNo,'='*50)
        web_driver.get(
            "https://section.blog.naver.com/ThemePost.nhn?directoryNo=27&activeDirectorySeq=3&currentPage={0}".format(pageNo))

        for blogNo in range(1, 11):
            web_driver.implicitly_wait(3)
            blogURL = web_driver.find_element_by_xpath("""//*[@id="content"]/section/div[2]/div[""" + str(
                blogNo) + """]/div/div[1]/div[1]/a[1]""").get_attribute('href')
            blogURLList.append(blogURL)
    return blogURLList


if __name__ == "__main__":
    web_driver = webdriver.Chrome('./driver/ver85/chromedriver')
    web_driver.implicitly_wait(3)


    if os.path.isfile('./blogURLData_'+ today +'.csv') == False:
        with open('./blogURLData_'+ today +'.csv', 'a', encoding='utf-8', newline='') as writer_csv:
            writer = csv.writer(writer_csv)
            writer.writerow(["blogurl"])
            blogURLList = blogURLCrawling()
            for blogURL in blogURLList:
                writer.writerow([blogURL])

    else:
        with open('./blogURLData_'+ today +'.csv', 'a', encoding='utf-8', newline='') as writer_csv:
            writer = csv.writer(writer_csv, delimiter=',')
            blogURLList = blogURLCrawling()

            for blogURL in blogURLList:
                writer.writerow([blogURL])

    web_driver.close()