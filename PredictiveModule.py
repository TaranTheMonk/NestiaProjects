from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plot

df = pd.read_csv('./Data/MAU-Feb.csv')
df = df.set_index(df.columns[0])
df.index.name = 'Date'
pca = PCA()
pca.fit(df)

explainVariance = pca.explained_variance_ratio_
plot.hist(explainVariance, bins=20)