import pandas as pd

df = pd.read_csv('../csv_puliti/airports-code2_final.csv')
df2 = pd.read_csv('../csv_puliti/airlines_final.csv')
lista_country = df['Country Name'].to_list()
lista_country2 = df2['Country'].to_list()
df3 = pd.read_csv('../csv_puliti/flight_data_database.csv')
lista_country3 = df3['paese_di_partenza'].to_list()
lista_country4 = df3['paese_di_arrivo'].to_list()

lista_country.extend(elem for elem in lista_country2 if type(elem) == str)
lista_country.extend(elem for elem in lista_country3 if type(elem) == str)
lista_country.extend(elem for elem in lista_country4 if type(elem) == str)
s = set()
for elem in lista_country:
    s.add(elem.title().strip())
l = list(s)
d = {l[i] :i+1 for i in range(len(l))}

print(len(s))
df_c = pd.DataFrame(s)
df_c[0].to_csv('country.csv')

