import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time


category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
df_titles = pd.DataFrame()

options = ChromeOptions()
# 브라우저 언어를 한국어로 설정
options.add_argument('lang=ko_KR')
# 브라우저 창을 화면에 띄우지 않고 백그라운드에서 실행, 주석처리하면 반대 동작
options.add_argument('headless')

# 현재 설치된 크롬 버전에 맞는 ChromeDriver를 자동으로 설치하거나 탐색
service = ChromeService(executable_path=ChromeDriverManager().install())
# 실제 자동 조작할 브라우저 객체를 생성
driver = webdriver.Chrome(service=service, options=options)
# 크롬에서 'Developer Tools'에 들어가 Ctrl+Shift+C를 누르고
# 기사 더보기 영역을 누르고 복사하면 링크를 얻을 수 있음
# @@ 단, Ecomonic은 div[4] -> div[5]로 값이 다름 @@
button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]/a'

# World(104), IT(105)
# (4, 'World'), (5, 'IT')로 반복하여 SECTION, CATEGORY에 대입
for SECTION, CATEGORY in zip(range(4, 6), category[4:6]):
    url = 'https://news.naver.com/section/10{}'.format(SECTION)
    # 브라우저가 해당 페이지에 접속
    driver.get(url)

    # 더보기 클릭
    for i in range(30):
        driver.find_element(By.XPATH, button_xpath).click()
        time.sleep(0.5)

    titles = []
    # j = 기사 묶음 번호, k = 묶음 안의 기사 번호
    for j in range(1, 180):
        for k in range(1, 7):
            try:
                # @@ 단, Ecomonic은 div[4] -> div[5]로 값이 다름 @@
                title_xpath = '//*[@id="newsct"]/div[4]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(j, k)
                # driver.find_element(...)로 해당 XPath의 요소를 찾고, .text로 제목 텍스트만 수집
                title = driver.find_element(By.XPATH, title_xpath).text
                titles.append(title)
            except:
                print('error', j, k)

    # 데이터 표 양식의 titles 부분 생성
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    # 데이터 표 양식의 category 부분 생성
    df_section_titles['category'] = CATEGORY

    # 각 카테고리별 DataFrame을 전체 DataFrame에 이어 붙이는 코드
    # 'ignore_index=True'는 기존 index를 무시하고 0부터 새로 번호를 매기라는 뜻
    df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)

# Selenium 브라우저를 종료
driver.quit()
# 앞 5개 행 출력
print(df_titles.head())
# DataFrame 정보 출력
df_titles.info()
# CSV 파일로 저장
df_titles.to_csv('./data/naver_news_section.csv', index=False)