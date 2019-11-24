from flask import Flask, render_template, request
import json
from beer import closest_beer


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", results=None)


@app.route('/', methods=['POST'])
def beers_post():
    text = request.form['text']
    abv = request.form['abv']
    bitter = request.form['bitter']
    neighbors = request.form['neighbors']
    user_input = json.dumps({"abv": abv, "text": text, "bitter": bitter, "neighbors": neighbors})
    best_beers = closest_beer(user_input)
    print(best_beers)
    return render_template('index.html', results=best_beers)


if __name__ == "__main__":
    app.run(debug=True)
