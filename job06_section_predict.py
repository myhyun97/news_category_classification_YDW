import pickle
import pandas as pd
import numpy as np
from keras.utils import to_categorical
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import re
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('./data/naver_headline_news_20260604.csv')
# 중복행 제거
df.drop_duplicates(inplace=True)
# 중복 제거 후 index를 다시 0부터 정리
df.reset_index(drop=True, inplace=True)
print(df.head())
df.info()
print(df.category.value_counts())

X = df.titles
Y = df.category

# 원래는 전에 저장했던 encoder를 가져와야하지만 저장을 잘못해서 밑에서 다시 생성
with open('./data/encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)
label = encoder.classes_
print(label)
labeled_y = encoder.transform(Y)
onehot_y = to_categorical(labeled_y)

# encoder = LabelEncoder()
# labeled_y = encoder.fit_transform(Y)
# print(labeled_y[:5])
# label = encoder.classes_
# print(label)
# onehot_y = to_categorical(labeled_y)
# print(onehot_y[:5])
X = list(X)

okt = Okt()
for i in range(len(X)):
    X[i] = re.sub('[^가-힣]', ' ', X[i])
    X[i] = okt.morphs(X[i], stem=True)
print(X)

for idx, sentence in enumerate(X):
    words = []
    for word in sentence:
        if len(word) > 1:
            words.append(word)
    X[idx] = ' '.join(words)
print(X[:10])

with open('./data/tokenizer_max26.pkl', 'rb') as f:
    tokenizer = pickle.load(f)
tokened_x = tokenizer.texts_to_sequences(X)
print(tokened_x[:5])

# test용 데이터인 X가 기존에 모델을 만들 때의 한문장의 최대 단어 개수인 26개를 넘을 경우
# 26번 뒤에 있는 데이터는 지우고 26보다 짧으면 앞의 자리에 0을 삽입
for i in range(len(tokened_x)):
    if len(tokened_x[i]) > 26:
        tokened_x[i] = tokened_x[i][:26]
x_pad = pad_sequences(tokened_x, maxlen=26)
print(x_pad[:5])

model = load_model('./models/news_section_classifier0.6883509755134583.h5')
score = model.evaluate(x=x_pad, y=onehot_y, verbose=0)
print('accuracy', score[1])

preds = model.predict(x_pad)
# print(preds)
predict_section = []
for pred in preds:
    most = label[np.argmax(pred)]
    pred[np.argmax(pred)] = 0
    second = label[np.argmax(pred)]
    predict_section.append([most, second])
df['predict'] = predict_section
print(df.head(5))

df['OX'] = 0
for i in range(len(df)):
    if df.loc[i, 'category'] in df.loc[i, 'predict']:
        df.loc[i, 'OX'] = 1
print(df.OX.mean())