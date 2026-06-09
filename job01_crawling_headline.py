from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime


category = ['Politics', 'Economic', 'Social', 'Culture', 'World','IT']
df_titles = pd.DataFrame()

for i in range(6):
    url = 'https://news.naver.com/section/10{}'.format(i)
    resp = requests.get(url)
    # print(list(resp))

    # resp.text(HTML 문자열) -> html.parser(BeautifulSoup 객체)로 변환
    soup = BeautifulSoup(resp.text, 'html.parser')
    # print(soup)

    # HTML 문서 안에서 class가 sa_text_strong인 태그들을 전부 찾음
    title_tag = soup.select('.sa_text_strong')
    titles = []
    # .text를 사용하여 뉴스 제목 텍스트를 titles에 추가
    for title in title_tag:
        titles.append(title.text)
    print(titles)
    # 데이터 표 양식의 titles 부분 생성
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    # 데이터 표 양식의 category 부분 생성
    df_section_titles['category'] = category[i]
    # 각 카테고리별 DataFrame을 전체 DataFrame에 이어 붙이는 코드
    # 'ignore_index=True'는 기존 index를 무시하고 0부터 새로 번호를 매기라는 뜻
    df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)
# .head()는 앞의 5개 행을 나타냄
print(df_titles.head())
# .info()는 DataFrame의 정보(전체 데이터 개수, 컬럼 이름, 결측값 여부, 데이터 타입)를 보여줌
df_titles.info()
# .to_csv()는 DataFrame을 CSV 파일로 저장하는 코드
# 'index=False'는 DataFrame index를 CSV에 저장하지 않겠다는 뜻
df_titles.to_csv('./data/naver_headline_news_{}_2PM.csv'.format
                 (datetime.datetime.now().strftime('%Y%m%d')),index=False)
