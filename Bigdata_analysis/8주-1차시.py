import pandas as pd
red_df = pd.read_csv("D:/BD/WINE/winequality-red.csv", sep=';', header=0, engine='python')
white_df = pd.read_csv("D:/BD/WINE/winequality-white.csv", sep=';', header=0, engine='python')
red_df.to_csv("D:/BD/WINE/winequality-red2.csv", index=False)
white_df.to_csv("D:/BD/WINE/winequality-white2.csv", index=False)

red_df.head()
red_df.insert(0,column='type', value='red')
red_df.head()
red_df.shape
white_df.head()
white_df.insert(0,column='type', value='white')
white_df.head()
white_df.shape
wine = pd.concat([red_df, white_df])
wine.shape
wine.to_csv("D:/BD/WINE/wine.csv", index=False)

print(wine.info())
wine.columns = wine.columns.str.replace(' ','_')
wine.head()
wine.describe()
sorted(wine.quality.unique())
wine.quality.value_counts()
