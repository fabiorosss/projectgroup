import pandas as pd
from pandasgui import show


df = pd.read_csv('dataset/artworks.csv')
print(df.columns)

print(df.shape)
print(df.isnull().sum())
df.drop(columns=['Weight (kg)', 'Depth (cm)', 'Length (cm)'], axis=1, inplace=True)

#df.drop_duplicates(subset=['Title', 'Artist ID', 'Name', 'Date', 'Medium', 'Acquisition Date', 'Catalogue', 'Classification', 'Credit', 'Department'], inplace = True)
df.drop_duplicates(subset="Title", inplace=True)


#print(df['Classification'].unique())
#show(df)
print(df.shape)
#show(df)

df2 = pd.read_csv("dataset/artists.csv")

