import pandas as pd
wine = pd.read_csv("D:/BD/WINE/wine.csv", sep=',', header=0, engine='python')

wine.groupby('type')['quality'].describe()
wine.groupby('type')['quality'].mean()
wine.groupby('type')['quality'].std()
wine.groupby('type')['quality'].agg(['mean', 'std'])


from scipy import stats
red_wine_quality = wine.loc[wine['type'] == 'red', 'quality']
white_wine_quality = wine.loc[wine['type'] == 'white', 'quality']
stats.ttest_ind(red_wine_quality, white_wine_quality, equal_var = False)

8.1*0.0000000000000000000000001  #평균차이 있다 
