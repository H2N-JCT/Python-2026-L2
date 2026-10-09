import numpy as np
import pandas as pd

data = {
    "name" : ["alice","bob"],
    "GPA" : [3.4,3.7]
}

df=pd.read_csv("students.csv")

print(df.head(),'\n')

print(df.shape,'\n')

print(df[["name","GPA"]],'\n')

print(df.loc[df["GPA"]>3.5],'\n')

print(df.sort_values(by="GPA"))

print(df.groupby("major")["GPA"].mean(),'\n')

sc=pd.read_csv("scores.csv")

print(f"students.csv missing values:\n{df.isnull().sum()}\n")
print(f"scores.csv missing values:\n{sc.isnull().sum()}\n") 

print(df[df.isna().any(axis=1)],'\n')
for ac in [df,sc]:
    ac.fillna(ac.mean(numeric_only=True), inplace=True)
print(df[df.isna().any(axis=1)],'\n')

mg = pd.merge(df,sc,on="student_id")

print(df.groupby(["student_id","name"])["GPA"].mean(),'\n')

avg=df.groupby(["student_id","name"])["GPA"].mean().reset_index()
print(avg.sort_values(by="GPA",ascending=False).head(),'\n')

avg=df.groupby("major")["GPA"].mean().reset_index()
print(avg)