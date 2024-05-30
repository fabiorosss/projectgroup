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

def funzione_mese(dati_utente):

    if dati_utente['giorno_partenza'] == None and dati_utente['giorno_arrivo'] == None:
        mese_partenza = f'2024-{dati_utente["mese_partenza"]}-01_2024-{dati_utente["mese_arrivo"]}-31'  # nel caso si effettui la ricerca per mese
        mese_arrivo = f'2024-{dati_utente["mese_partenza"]}-01_2024-{dati_utente["mese_partenza"]}-31'
        if dati_utente['citta_partenza'] == None and dati_utente['citta_arrivo'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['paese_partenza']}/{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        elif dati_utente['citta_partenza'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['paese_partenza']}/{dati_utente['citta_arrivo']}-{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        elif dati_utente['citta_arrivo'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['citta_partenza']}-{dati_utente['paese_partenza']}/{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        else:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['citta_partenza']}-{dati_utente['paese_partenza']}/{dati_utente['citta_arrivo']}-{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"

    elif dati_utente['giorno_partenza'] == None:
        mese_partenza = f'2024-{dati_utente["mese_partenza"]}-01_2024-{dati_utente["mese_arrivo"]}-31'  # nel caso si effettui la ricerca per mese
        mese_arrivo = f'2024-{dati_utente["mese_arrivo"]}-{dati_utente['giorno_arrivo']}'
        if dati_utente['citta_partenza'] == None and dati_utente['citta_arrivo'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['paese_partenza']}/{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        elif dati_utente['citta_partenza'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['paese_partenza']}/{dati_utente['citta_arrivo']}-{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        elif dati_utente['citta_arrivo'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['citta_partenza']}-{dati_utente['paese_partenza']}/{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        else:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['citta_partenza']}-{dati_utente['paese_partenza']}/{dati_utente['citta_arrivo']}-{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"

    elif dati_utente['giorno_arrivo'] == None:
        mese_partenza = f'2024-{dati_utente["mese_partenza"]}-{dati_utente['giorno_partenza']}'
        mese_arrivo = f'2024-{dati_utente["mese_partenza"]}-01_2024-{dati_utente["mese_arrivo"]}-31'
        if dati_utente['citta_partenza'] == None and dati_utente['citta_arrivo'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['paese_partenza']}/{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        elif dati_utente['citta_partenza'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['paese_partenza']}/{dati_utente['citta_arrivo']}-{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        elif dati_utente['citta_arrivo'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['citta_partenza']}-{dati_utente['paese_partenza']}/{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        else:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['citta_partenza']}-{dati_utente['paese_partenza']}/{dati_utente['citta_arrivo']}-{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"

    else:
        mese_partenza = f'2024-{dati_utente["mese_partenza"]}-{dati_utente['giorno_partenza']}'
        mese_arrivo = f'2024-{dati_utente["mese_arrivo"]}-{dati_utente['giorno_arrivo']}'
        if dati_utente['citta_partenza'] == None and dati_utente['citta_arrivo'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['paese_partenza']}/{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        elif dati_utente['citta_partenza'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['paese_partenza']}/{dati_utente['citta_arrivo']}-{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        elif dati_utente['citta_arrivo'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['citta_partenza']}-{dati_utente['paese_partenza']}/{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        else:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['citta_partenza']}-{dati_utente['paese_partenza']}/{dati_utente['citta_arrivo']}-{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"

    print(url)

    # Ottieni il driver
    driver = get_driver()

    # Effettua la richiesta
    driver.get(url)
    driver.maximize_window()

    input("Vai avanti")

    html_content = driver.page_source

    try:
        accept_button = driver.find_element(By.ID, "cookies_accept")
        accept_button.click()
    except Exception as e:
        print("Non è stato possibile trovare il bottone di accettazione dei cookie:", e)

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
    partenza = country
    arrivo = country2
    url = f"https://www.kiwi.com/it/search/tiles/{partenza}/{arrivo}/{mese_partenza}/{mese_arrivo}"
else:
    city_country = input()
    city_country2 = input()
    partenza = city_country
    arrivo = city_country2
    url = f"https://www.kiwi.com/it/search/tiles/{partenza}/{arrivo}/{mese_partenza}/{mese_arrivo}"

print(url)

# Ottieni il driver
driver = get_driver()

# Effettua la richiesta
driver.get(url)
driver.maximize_window()

input("Vai avanti")

html_content = driver.page_source

try:
    accept_button = driver.find_element(By.ID, "cookies_accept")
    accept_button.click()
except Exception as e:
    print("Non è stato possibile trovare il bottone di accettazione dei cookie:", e)

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
    if arrivo.title() in lista_arrivi[0]:
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
input()
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

driver.quit()