import requests            #funciona com o app.py da pasta pokemon-api-flask

url = "http://localhost:5000/pokemon"

resposta = requests.get(url)

dados = resposta.json()

print(dados)