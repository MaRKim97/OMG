import numpy as np
import pandas as pd
import glob
import datetime

# ↓ 제목, 줄거리, 카테고리를 포함한 모든 데이터 불러오기 ↓
data_path = glob.glob("./crawling_data/*.csv")

# ↓ 데이터를 합쳐주는 과정 ↓
df = pd.DataFrame()
for path in data_path:
    df_temp = pd.read_csv(path, index_col=0)
    df = pd.concat([df, df_temp], axis="rows", ignore_index=True)
df = df.replace('NULL', np.nan)
df = df.dropna()

print(df["category"].value_counts())
print(df.info())
df.to_csv("./movie_concat_data_{}.csv".format(datetime.datetime.now().strftime("%Y%m%d")), index=False)
