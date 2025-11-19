import numpy as np
import pandas as pd
import csv

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

with open('NSMES1988 - NSMES1988.csv', 'r', newline='') as file:
    csv_reader = csv.reader(file)


df = pd.read_csv("NSMES1988 - NSMES1988.csv", index_col=0)
df.loc[df['age'] < 11, 'age'] = df['age'] * 10
df['income'] = (df['income']*1000).fillna(0)
print(df.head(50))
df.info()
df.describe()
print(df.columns)
#print(df.iloc[[287]])
print(df.isnull().sum())
