import base64
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from q import *


def get_driver():
    options = Options()
    # options.add_argument('--headless')  # Esegui il browser in modalità headless
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


# URL da richiedere
data_partenza = '18 09 2024'
data_arrivo = '22 09 2024'
lista = data_partenza.split(' ')
lista2 = data_arrivo.split(' ')
mese_partenza = f'{lista[2]}-{lista[1]}-01_{lista[2]}-{lista[1]}-31'  # nel caso si effettui la ricerca per mese
mese_arrivo = f'{lista2[2]}-{lista2[1]}-01_{lista[2]}-{lista[1]}-31'
scelta = int(input())
if scelta == 0:
    country = input()
    country2 = input()
if scelta == 1:
    city_country = input()
    city_country2 = input()

url = f"https://www.kiwi.com/it/search/tiles/{city_country}/{city_country2}/{mese_partenza}/{mese_arrivo}"
print(url)

# Ottieni il driver
driver = get_driver()

# Effettua la richiesta
driver.get(url)
driver.maximize_window()

input("Vai avanti")

# Ottieni l'HTML della pagina
html_content = driver.page_source
# class_name = 'leading-normal'
# elements = driver.find_elements(By.CLASS_NAME, class_name)
# lista = []
# # Chiudi il driver
# if elements:
#     for index, element in enumerate(elements):
#         t_element = element.text
#         if '€' in t_element:
#             stringa = ''
#             print(f"Elemento {index + 1}:")
#             print(element.get_attribute('outerHTML'))
#             print("\n")
#             for i in range(1, len(t_element), 1):
#                 if t_element[i].isnumeric() and t_element[i+1].isnumeric():
#                     stringa += t_element[i]
#                 elif t_element[i].isnumeric() and t_element[i-1].isnumeric():
#                     stringa += t_element[i]
#             stringa += '€'
#             lista.append(stringa)
# else:
#     print(f"Nessun elemento trovato con la class {class_name}")

try:
    accept_button = driver.find_element(By.ID, "cookies_accept")
    accept_button.click()
except Exception as e:
    print("Non è stato possibile trovare il bottone di accettazione dei cookie:", e)

lista_citta_aeroporto = ['Roma', 'Milano', 'Bergamo', 'Venezia', 'Catania', 'Bologna', 'Napoli', 'Pisa', 'Palermo',
                         'Bari', 'Torino', 'Cagliari',
                         'Verona', 'Lamezia Terme', 'Firenze', 'Brindisi', 'Treviso', 'Olbia', 'Alghero', 'Trapani',
                         'Genova', 'Trieste',
                         'Reggio Calabria', 'Ancona', 'Rimini', 'Cuneo', 'Perugia', 'Parma', 'Bolzano', 'Brescia',
                         'Pescara', 'Pantelleria',
                         'Foggia', 'Grosseto', 'Comiso', 'Forli', 'Siena', 'Salerno', 'Crotone', 'Perugia', ]

tag_name = "span"
elements = driver.find_elements(By.TAG_NAME, tag_name)

lista_arrivi = []
if elements:
    for index, element in enumerate(elements):
        t_element = element.text
        print(t_element)
        if t_element.isalpha() and t_element != 'Feedback':
            lista_arrivi.append(t_element)
        elif '€' in t_element:
            lista_arrivi.append(t_element.replace(' ', ''))
else:
    print('nessun elemento trovato')

lista_finale = []
for i in range(1, len(lista_arrivi), 1):
    if lista_arrivi[0] in city_country2.title():
        lista_finale.append(lista_arrivi[0])
    if lista_arrivi[i].isalpha() and '€' in lista_arrivi[i - 1]:
        lista_finale.append(lista_arrivi[i])
    elif lista_arrivi[i].isalpha() and '€' in lista_arrivi[i - 1]:
        lista_finale.append(lista_arrivi[i])
    elif '€' in lista_arrivi[i] and lista_arrivi[i - 1].isalpha:
        lista_finale.append(lista_arrivi[i])
    else:
        continue

print(lista_finale)

image_elements = driver.find_elements(By.TAG_NAME, 'img')

for index, image_element in enumerate(image_elements):
    image_url = image_element.get_attribute('src')
    try:
        # Check if the URL is a base64 string
        if image_url.startswith('data:image'):
            header, encoded = image_url.split(',', 1)
            image_data = base64.b64decode(encoded)
        else:
            # Otherwise, it's a regular URL, so we fetch the content
            image_data = requests.get(image_url).content

        # Save the image data to a file
        with open(f'output_{index}.gif', 'wb') as handler:
            handler.write(image_data)
    except Exception as e:
        print(f"Error processing image {index}: {e}")

# Stampa l'HTML ottenuto
# print(html_content)
input()
driver.quit()
