import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt, Komoran
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import re
import datetime

df = pd.read_csv('./data/news_titles_total.csv')
df.info()
print(df.head(30))
print(df.category.value_counts())

X = df.titles
Y = df.category
# print(X[0])
# okt = Okt()
## 한글이 아닌 문자를 공백으로 변환
# x = re.sub('[^가-힣]', ' ', X[0])
## 문장을 형태소 단위로 나눔
# okt_x = okt.morphs(x)
# print(okt_x)
## 'stem=True' - 어간 추출
# okt_x_stem = okt.morphs(x, stem=True)
# print(okt_x_stem)
#
## 한국어 형태소 분석기
## Okt - 비교적 사용하기 쉽고 SNS/일반 문장에 자주 사용
## Komoran - 형태소 분석이 비교적 세밀함
#
# komoran = Komoran()
# komoran_x = komoran.morphs(X[0])
# print(komoran_x)

# 문자로 된 카테고리를 숫자로 바꾸는 과정
encoder = LabelEncoder()
# 문자 카테고리를 숫자 라벨로 바꾸는 코드
labeled_y = encoder.fit_transform(Y)
print(labeled_y[:5])
# 숫자와 원래 카테고리 이름의 대응표를 저장
label = encoder.classes_
print(label)

# 학습 때 만든 LabelEncoder를 파일로 저장
with open('./data/encoder_{}.pkl'.format(
    datetime.datetime.now().strftime('%Y%m%d')), 'wb') as f:
    pickle.dump(encoder, f)

# one-hot 형태 ex)
# 0 → [1, 0, 0, 0, 0, 0]
# 1 → [0, 1, 0, 0, 0, 0]
# 2 → [0, 0, 1, 0, 0, 0]
# 3 → [0, 0, 0, 1, 0, 0]
# 4 → [0, 0, 0, 0, 1, 0]
# 5 → [0, 0, 0, 0, 0, 1]
onehot_y = to_categorical(labeled_y)
print(onehot_y[:5])

# cleaned_x = re.sub('[^가-힣]', '', X[0])
# print(X[0])
# print(cleaned_x)

# 한국어 형태소 분석기 객체 생성
okt = Okt()
# pandas Series 형태였던 X를 파이썬 리스트로 변환
X = list(X)
for i in range(len(X)):
    # 한글이 아닌 모든 문자를 공백으로 변환, strip()은 앞뒤 공백을 제거
    X[i] = re.sub('[^가-힣]', ' ', X[i]).strip()
    # 형태소 단위로 분리('stem=True' - 어간 추출을 적용)
    X[i] = okt.morphs(X[i], stem=True)
    if i % 1000 == 0:
        print(i)
print(X[:5])

# 길이 1 이하 단어 제거
for idx, sentence in enumerate(X):
    words = []
    for word in sentence:
        if len(word) > 1:
            words.append(word)
    # 단어 사이에 공백을 추가하여 단어 리스트를 다시 하나의 문자열로 합성
    # Keras Tokenizer가 보통 공백으로 구분된 문자열 목록을 입력으로 받기 때문
    X[idx] = ' '.join(words)
print(X[:5])

# Tokenizer - 단어를 숫자 index로 바꿔주는 도구
tokenizer = Tokenizer()
# 전체 문장에 등장한 단어들을 보고 단어마다 번호를 부여
tokenizer.fit_on_texts(X)
# 문장을 숫자 리스트로 변환
tokened_x = tokenizer.texts_to_sequences(X)
print(tokened_x)
# tokenizer.word_index - 단어와 번호의 매핑 딕셔너리
# +1을 하는 이유는 보통 index 0을 padding 용도로 사용하기 때문
wordsize = len(tokenizer.word_index) + 1
print(wordsize)

# 최대 문장 길이 계산
max = 0
for sentence in tokened_x:
    if max < len(sentence):
        max = len(sentence)
print(max)
with open('./data/tokenizer_max{}_{}.pkl'.format(max, datetime.datetime.now().strftime('%Y%m%d')), 'wb') as f:
    pickle.dump(tokenizer, f)

# Padding 적용
# 가장 긴 문장을 기준으로 모든 문장의 길이를 그에 맞춤(문장 앞에 0을 넣음으로써)
x_pad = pad_sequences(tokened_x, maxlen=max)
print(x_pad[:5])

x_train, x_test, y_train, y_test = train_test_split(
    x_pad, onehot_y, test_size=0.1)
print(x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)
np.save('./data/x_train_wordsize{}_{}.npy'.format(wordsize, datetime.datetime.now().strftime('%Y%m%d')), x_train)
np.save('./data/y_train_wordsize{}_{}.npy'.format(wordsize, datetime.datetime.now().strftime('%Y%m%d')), y_train)
np.save('./data/x_test_wordsize{}_{}.npy'.format(wordsize, datetime.datetime.now().strftime('%Y%m%d')), x_test)
np.save('./data/y_test_wordsize{}_{}.npy'.format(wordsize, datetime.datetime.now().strftime('%Y%m%d')), y_test)