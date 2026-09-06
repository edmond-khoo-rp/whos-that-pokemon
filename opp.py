import os
import random
import requests
from flask import Flask, render_template

app = Flask(__name__)


def get_random_pokemon():
    # Fetch list
    res = requests.get("https://pokeapi.co/api/v2/pokemon/?limit=1025").json()
    pkmn_list = res["results"]

    # Reroll until a default form is found
    while True:
        choice = random.choice(pkmn_list)
        data = requests.get(choice["url"]).json()
        if data.get("is_default"):
            name = data["species"]["name"].title()
            img_url = data["sprites"]["other"]["official-artwork"][
                "front_default"
            ]
            return name, img_url


@app.route("/")
def index():
    name, img_url = get_random_pokemon()
    return render_template("index.html", name=name, img_url=img_url)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
