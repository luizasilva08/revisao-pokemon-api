import requests          #api sem flask

def consultar_pokemon():
    url = "https://pokeapi.co/api/v2/pokemon/pikachu"

    resposta = requests.get(url)

    if resposta.status_code == 200:
        return resposta.json()

    return None

dados = consultar_pokemon("pikachu")

if dados:
    print(dados["name"])

else:
    print("Pokemon não encontrado")