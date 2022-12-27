from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import requests,re,time

# 다음 증권에서 업종을 찾는다
def result_url():
    url = 'https://finance.daum.net/domestic/sectors'
    driver = driver_run(url)
    url_list = []
    # 상위 10 업종까지
    for i in range(0,10):
        try :
            target_url = driver.find_elements_by_class_name('lAlign a')
            extract_url=target_url[i].get_attribute('href')
            extract_title = target_url[i].text
            url_list.append(extract_url)
            print(extract_url)
            print(extract_title)
            # contents_extract(url_list[i])
            # time.sleep(5)
            catregory_url(extract_url)
        except exceptions.StaleElementReferenceException as e:
            print(e)
            pass
    print("url_list = ", url_list)
    driver.quit()
    # try:
    #     # gsr 이라는 요소를 10초안에 찾을때까지 대기. 시간내에 찾지못하면 TimeoutException 에러가 나든 말든 드라이버 닫힘
    #     element = WebDriverWait(driver,10).until(EC.presence_of_element_located(By.ID, "myDynamicElement"))
    # finally:
    #     driver.quit()

# 찾은 업종 관련주 이름과 id를 가져온다
def catregory_url(url):
    driver = driver_run(url)
    target_url = driver.find_elements(By.CLASS_NAME, 'txt')
    url_list = []
    for i in range(0,len(target_url)):
        try:
            target_url = driver.find_elements(By.CLASS_NAME, 'txt')
            extract_url = target_url[i].get_attribute('href')
            extract_title = target_url[i].text
            final_url = "https://comp.fnguide.com/SVO2/ASP/SVD_main_chosunbiz.asp?pGB=1&gicode=" + extract_url.split('/')[4]
            capture_url = "https://finance.daum.net/quotes/" + extract_url.split('/')[4]
            print(final_url)
            print(extract_title)
            url_list.append(extract_url)
            # time.sleep(5)
            # screenshotimg(capture_url,extract_title)
            extract_info(final_url)
            # contents_extract(url_list[i])
        except exceptions.StaleElementReferenceException as e:
            print("카테고리 = ",e)
            pass
    print("url_list = ", url_list)
    driver.quit()

# 회사의 주식정보 사진을 캡쳐한다.
def screenshotimg(url,title):
    driver = driver_run(url)
    driver.set_window_size(1500,1500)
    time.sleep(3)
    driver.get(url)
    element = driver.find_element_by_class_name("detailStk")
    element_png = element.screenshot_as_png
    with open(title+'.png',"wb") as file:
        file.write(element_png)
    driver.quit()

# 회사 텍스트정보를 가져온다.
def extract_info(url):
    driver = driver_run(url)
    try:
        text_element = driver.find_element_by_class_name('um_bssummary')
        splittext = str(text_element.text).split('\n')
        splittext.pop(0)
        # splittext2 = str(splittext).split('.')
        for i in range(0,len(splittext)):
            print(i,splittext[i])
            # print(i,splittext2[i].replace("[","").replace("]", ""))
        # result_text =str(str(splittext2).replace('[', "")).replace(']', "")
    except :
        # 우량주 주식은 정보가 없음
        print("해당 없음")
    driver.quit()

# 웹 창 실행
def driver_run(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome('C:/Users/Youngwoo/Downloads/chromedriver_win32/chromedriver.exe', options=options)
    driver.get(url)
    driver.implicitly_wait(10)

    return driver