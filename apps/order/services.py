from os import replace
import requests

def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

def get_casa(params={}):
    response = generate_request('https://www.dolarsi.com/api/api.php?type=valoresprincipales', params)
    if response:
        dolar_blue = 0.0
        for casa in response:
            if(casa['casa']['nombre']=="Dolar Blue"):
                dolar_blue=casa['casa']['compra']

        return float(dolar_blue.replace(',','.'))

    return ""