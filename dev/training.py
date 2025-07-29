import numpy as np
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.preprocessing import LabelEncoder
import joblib



print(os.getcwd())


# 讀取資料
df = pd.read_csv('./data/personality_dataset.csv')

# 簡單填補缺失值
df.fillna(method='ffill', inplace=True)

# 將類別欄位轉為數值
label_cols = ['Stage_fear', 'Drained_after_socializing', 'Personality']
encoders = {}
for col in label_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le  # 如果你想要日後解碼用

# 拆成特徵與目標
X = df.drop("Personality", axis=1)
y = df["Personality"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 建立模型
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# 預測與評估
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]
accuracy = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_prob)

print("模型準確率：", accuracy)
print("AUC：", auc)

joblib.dump(model,'./dev/model.pkl')

# make test data
df_test1 = X_test.iloc[[0]]
model = joblib.load('./dev/model.pkl')
y = model.predict(df_test1)


df_test1.to_csv('./prod/test/input/input1.csv',index=False)
df_test1.to_json('./prod/test/input/input1.json',oriend='records')  


df_y = pd.DataFrame(y)
df_y.columns = ['IF_INTROVERTED']
df_y.to_csv('./prod/test/output/output1.csv',index=False)
df_y.to_json('./prod/test/output/output1.json',orient='records')