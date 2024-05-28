import pandas as pd

df = pd.read_csv('csv_puliti/flight_data_final.csv')
df.drop_duplicates()
lista = df['nome_compagnia'].to_list()

df_airline = pd.read_csv('csv_puliti/airlines_final.csv')
df_airline.drop_duplicates()
lista_compagnie = df_airline['Name'].to_list()
diz_compagnie = {elem[1]: elem[0] for elem in enumerate(lista_compagnie)}

lista2 = []
for elem in lista:
    lista2.append(elem.replace('[', '').replace(']', '').split('| '))

lista_id = []
for elem in enumerate(lista2, start=1):
    for i in range(len(elem[1])):
        lista_id.append([elem[0], elem[1][i]])

df_da_esportare = pd.DataFrame(lista_id)

df_da_esportare[1] = df_da_esportare[1].map(diz_compagnie)
print(df_da_esportare.isnull().sum())

df_da_esportare.to_csv('df_da_esportare333.csv')