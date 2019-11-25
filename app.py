from flask import Flask, render_template, request
import json
from beer import closest_beer


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", results=None)


@app.route('/', methods=['POST'])
def beers_post():
    # Get text
    text = request.form['text']

    # Get abv and sanitize
    abv = request.form['abv']
    try:
        abv = min(max(int(abv), 0), 100)  # don't let users submit values below 0 or above 100
    except ValueError:
        abv = 5  # default

    # Get bitter
    bitter = request.form['bitter']

    # Get neighbors and sanitize
    neighbors = request.form['neighbors']
    try:
        neighbors = min(max(int(neighbors), 1), 10)  # max display of 10 beers min of 1
    except ValueError:
        neighbors = 1  # default

    # Search beers
    user_input = json.dumps({"abv": abv, "text": text, "bitter": bitter, "neighbors": neighbors})
    best_beers = closest_beer(user_input)

    beer_ids = json.loads(best_beers)['beer_id']


    return render_template('index.html', results=beer_ids)


if __name__ == "__main__":
    app.run(debug=False)
