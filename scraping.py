import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import requests,re,time

class Search:

    company_count = 0
    title = ''
    company_title = ''
    content = []
    content_data =''
    post_title = []
    
    def set_post_data(self, content_data):
        self.content_data += content_data

    def get_post_data(self):
        return self.content_data

    def set_post_title(self, post_title):
        self.post_title.append(post_title)

    def get_post_title(self):
        return self.post_title

    def set_content(self, content):
        self.content.append(content)

    def get_content(self):
        return self.content

    def set_company_count(self, count):
        self.company_count = count + 1

    def get_company_count(self):
        return self.company_count

    def set_title(self,title):
        self.title = title

    def get_title(self):
        return self.title

    def set_company_title(self, company_title):
        self.company_title = company_title

    def get_company_title(self):
        return self.company_title

    # 웹 창 실행
    def driver_run(self, url):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome('C:/Users/Youngwoo/Downloads/chromedriver_win32/chromedriver.exe', options=options)
        driver.get(url)
        driver.implicitly_wait(10)

        return driver
    # 다음 증권에서 업종을 찾는다
    def find_category(self):
        url = 'https://finance.daum.net/domestic/sectors'
        driver = self.driver_run(url)
        url_list = []
        # 상위 10 업종까지
        for i in range(0, 10):
            try:
                target_url = driver.find_elements_by_class_name('lAlign a')
                extract_url = target_url[i].get_attribute('href')
                self.set_title(target_url[i].text)
                url_list.append(extract_url)
                print(extract_url)
                print(self.get_title())
                self.find_CompanyInfo(extract_url)
                print("============================한종목 끝==================================")
            except exceptions.StaleElementReferenceException as e:
                print(e)
                pass
        driver.quit()
        # try:
        #     # gsr 이라는 요소를 10초안에 찾을때까지 대기. 시간내에 찾지못하면 TimeoutException 에러가 나든 말든 드라이버 닫힘
        #     element = WebDriverWait(driver,10).until(EC.presence_of_element_located(By.ID, "myDynamicElement"))
        # finally:
        #     driver.quit()

    # 찾은 업종 관련주 이름과 id를 가져온다
    def find_CompanyInfo(self, url):
        driver = self.driver_run(url)
        try:
            target_url = driver.find_elements(By.CLASS_NAME, 'txt')
            self.set_company_count(len(target_url))
            url_list = []
            for i in range(0, len(target_url)):
                try:
                    target_url = driver.find_elements(By.CLASS_NAME, 'txt')
                    extract_url = target_url[i].get_attribute('href')
                    self.set_company_title(target_url[i].text)
                    final_url = "https://comp.fnguide.com/SVO2/ASP/SVD_main_chosunbiz.asp?pGB=1&gicode=" + \
                                extract_url.split('/')[4]
                    capture_url = "https://finance.daum.net/quotes/" + extract_url.split('/')[4]
                    print(final_url)
                    print(self.get_company_title())
                    url_list.append(extract_url)
                    self.screenshotimg(capture_url)
                    self.get_Companyinfo(final_url)
                except exceptions.StaleElementReferenceException as e:
                    print("카테고리 = ", e)
                    pass
            print("url_list = ", url_list)
        except:
            return
        driver.quit()

    # 회사의 주식정보 사진을 캡쳐한다.
    def screenshotimg(self, url):
        driver = self.driver_run(url)
        driver.set_window_size(1500, 1500)
        time.sleep(3)
        driver.get(url)
        try :
            element = driver.find_element_by_class_name("detailStk")
            element_png = element.screenshot_as_png
            with open('media/'+ self.get_company_title() + '.png', "wb") as file:
                file.write(element_png)

        except:
            print("사진 정보 없음")
        driver.quit()

    # 회사 텍스트정보를 가져온다.
    def get_Companyinfo(self,url):
        driver = self.driver_run(url)
        data=[]
        try:
            # text_element = driver.find_element_by_class_name('um_bssummary')
            text_element = driver.find_element_by_id('bizSummaryContent')
            splittext = str(text_element.text).split('\n')
            print(splittext)
            # splittext.pop(0)
            # splittext2 = str(splittext).split('.')
            for i in range(0, len(splittext)):
                data.append(splittext[i])
                # print(i, splittext[i])
            self.tempWriteData(data, self.get_title(), self.get_company_title())
        except:
            # 우량주 주식은 정보가 없음
            print("정보 없음")

        driver.quit()

    # 이미지 파일 업로드
    def fileupload(self, path):
        blogName = 'leo-developer'
        access_token = '6bdb25ea80edb1f461e16e34dd4d7201_86d9ee0008c0d2ea96ef18ca21e880de'

        files = {'uploadedfile':open(path,'rb')}
        params = {'access_token': access_token, 'blogName': blogName, 'targetUrl': blogName, 'output':'json'}
        rd = requests.post('https://www.tistory.com/apis/post/attach', params=params, files=files)

        try:
            item = json.loads(rd.text)
            print(json.dumps(item,indent=4))
            print("-------------------------------")
            print(item["tistory"]["replacer"])
            print(item["tistory"]["url"])
            print(item["tistory"]["status"])
        except:
            print("Failed")

        return item["tistory"]["replacer"]

    # 글올릴 자료 저장
    def tempWriteData(self, data, title, companytitle):
        #관련 종목
        post_title = title + ' 관련주 ' + str(self.get_company_count()) + '종목'
        #주식 이름
        post_company_title = companytitle +' ('+ title + ' 관련 주식)'
        #주식 소개
        company_intro = data[0].split('.')

        html_content = '<div><span>'+ title +' 관련주 기업 실적 및 기업 개요를 알아보도록 하겠습니다. </span></div>'
        html_content += '<h2><span>'+ post_company_title + '</span></h2>'
        html_content += self.fileupload('media/'+self.get_company_title()+'.png')
        html_content += '<h3><span> -주식 기업소개</span></h3>'
        html_content += '<ul>'
        for i in range(0,len(company_intro)-1):
            html_content += '<li>' + company_intro[i] + '</li>'
        html_content += '</ul>'
        html_content += '<h3><span> -주식 기업실적 </span></h3>'
        html_content += '<ul><li>' + data[1] + '</li></ul>'
        html_content +='<p> &nbsp; </p>'
        self.set_post_data(html_content)
        self.set_post_title(post_title)
        # print(html_content)
        # print('title = ',post_title)
        # print('companytitle = ',post_company_title)
        # print('data = ',data)


class BlogPost:
    # 포스팅하기
    def postWrite(self, title, content):
        visibility = 3
        category = 1092282
        url = 'https://www.tistory.com/apis/post/write?'
        tag = 'test'
        data = {
            'access_token': self.readjson('access_token'),
            'output': self.readjson('output'),
            'blogName': self.readjson('blogName'),
            'title': title,
            'content': content,
            'visibility': visibility,
            'category': category,
            'tag': tag,
        }
        r = requests.post(url, data=data)
        print(r.text)

    def readjson(self, key):
        file_path = "blogkey.txt"
        with open(file_path, "r") as json_file:
            json_data = json.load(json_file)
            print(json_data[key])
            return json_data[key]
