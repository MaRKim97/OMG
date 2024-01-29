import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle

# ↓ 제목, 줄거리, 카테고리를 포함한 데이터 불러오기 ↓
df = pd.read_csv('./movie_concat_data_20240129.csv')

# ↓ 줄거리를 통해 카테고리를 예측하기 위해 아래와 같이 설정 ↓
X = df['synopsis']
Y = df['category']

# ↓ 카테고리에 라벨 부여 ↓
label_encoder = LabelEncoder()
labeled_y = label_encoder.fit_transform(Y)
label = label_encoder.classes_
print(label) # 결과값: ['action' 'animation' 'melo']

# ↓ 예측하는 과정에서 사용하기위해 pickle확장자 파일로 저장 ↓
with open('./models/label_encoder.pickle', 'wb') as f:
    pickle.dump(label_encoder, f)

# ↓ 원-핫 인코딩된 벡터로 변환 ↓
onehot_y = to_categorical(labeled_y)

# ↓ 형태소 분리 ↓
okt = Okt()
for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)

# ↓ 불용어와 의미학습이 제대로 되지 않는 한글자 단어 제거 ↓
stopwords = pd.read_csv('./stopwords.csv', index_col=0)
for j in range(len(X)):
    words = []
    for i in range(len(X[j])):
        if len(X[j][i]) > 1:
            if X[j][i] not in list(stopwords['stopword']):
                words.append(X[j][i])
    X[j] = ' '.join(words) # 'a b c 와 같은 형태로 문자열을 만들어줌

# ↓ 토큰화와 및 정수인코딩 ↓
token = Tokenizer()
token.fit_on_texts(X) # 예시: {'오늘': 1, '있어': 2, '주식': 3} 이와 같이 맵핑이 된다
tokened_x = token.texts_to_sequences(X) # 정수인코딩 시켜준다 / 결과값: [1428, 1429, 818, 819, ...], [314, 30, 43, ...], ...
wordsize = len(token.word_index) + 1 # 단어의 길이 결과값: 3107

# ↓ 예측하는 과정에서 사용하기위해 pickle확장자 파일로 저장 ↓
with open('./models/movie_token.pickle', 'wb') as f:
    pickle.dump(token, f)

# ↓ 가장 긴 길이로 패딩해주는 과정 ↓
max = 0
for i in range(len(tokened_x)):
    if max < len(tokened_x[i]):
        max = len(tokened_x[i]) # 결과값: 214
x_pad = pad_sequences(tokened_x, max)

# ↓ 훈련데이터와 테스트데이터로 분리 ↓
X_train, X_test, Y_train, Y_test = train_test_split(x_pad, onehot_y, test_size=0.2)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

xy = X_train, X_test, Y_train, Y_test
xy = np.array(xy, dtype=object)
np.save('./movie_data_{}_wordsize_{}'.format(max, wordsize), xy)
