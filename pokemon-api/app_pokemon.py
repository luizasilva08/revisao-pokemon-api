import requests          #back-end 

nome = input("Digite o nome do Pokémon: ")

url = f"https://pokeapi.co/api/v2/pokemon/{nome}"

resposta = requests.get(url)

if resposta.status_code == 200:

    dados = resposta.json()

    print(f"Pokémon: {dados['name']}")

else:

    print("Não foi possível consultar o Pokémon.")