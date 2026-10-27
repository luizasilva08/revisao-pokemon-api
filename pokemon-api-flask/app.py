from flask import Flask    #api com flask

app = Flask(__name__)

@app.get("/pokemon")
def listar_pokemons():
    return {
        "pokemon": [
            "pikachu",
            "ditto",
            "charizard"
        ]
    }

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )