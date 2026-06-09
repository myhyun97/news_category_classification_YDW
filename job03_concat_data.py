import pandas as pd
import datetime

df = pd.read_csv('./data/naver_news_section_World_20260608.csv')
print(df.head())

df_temp = pd.read_csv('./data/naver_news_section_IT_20260608.csv')
print(df_temp.head())

df = pd.concat([df, df_temp], ignore_index=True)
df_temp = pd.read_csv('./data/naver_news_section_Economic_20260608.csv')
df = pd.concat([df, df_temp], ignore_index=True)
df_temp = pd.read_csv('./data/naver_news_section_Politics_20260608.csv')
df = pd.concat([df, df_temp], ignore_index=True)
df_temp = pd.read_csv('./data/naver_news_section_Social_20260608.csv')
df = pd.concat([df, df_temp], ignore_index=True)
df_temp = pd.read_csv('./data/naver_news_section_Culture_20260608.csv')
df = pd.concat([df, df_temp], ignore_index=True)
df_temp = pd.read_csv('./data/naver_headline_news_20260608.csv')
df = pd.concat([df, df_temp], ignore_index=True)
df.info()
# 겹치는 데이터 삭제
df = df.drop_duplicates()
print(df.category.value_counts())
print(df.isnull().sum())
df.info()
df.to_csv('./data/news_titles_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index=False)

# df = pd.read_csv('./data/news_titles.csv')
# df_temp = pd.read_csv('./data/news_titles_20260608.csv')
# df = pd.concat([df, df_temp], ignore_index=True)
# print(df.category.value_counts())
# print(df.isnull().sum())
# df.info()
# df.to_csv('./data/news_titles_total.csv', index=False)