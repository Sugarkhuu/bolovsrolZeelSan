import pandas as pd 
# process data 
df = pd.read_csv("data/Боловсролын зээлийн сан түүх_1997_2023.csv")
df = df.iloc[:,3:] # remove index, page and full name columns

# rename and reorder columns, just for ease  of use
df.columns = ['country','school','field','duration','amount','Surname','First name']
df = df[['Surname','First name','country','school','field','duration','amount']]

df.to_csv('data/processed_data.csv',index=False, encoding='utf-8-sig')