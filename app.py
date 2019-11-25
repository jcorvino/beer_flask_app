from flask import Flask, render_template, request
from gevent.pywsgi import WSGIServer
import json
from beer import closest_beer, beer_details


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", results=None)


@app.route('/', methods=['POST'])
def beers_post():
    # Get text
    text = request.form['text'][0:255]  # max length of 255 chars

    # Get abv and sanitize
    abv = request.form['abv']
    try:
        abv = min(max(int(abv), 0), 100)  # don't let users submit values below 0 or above 100
    except ValueError:
        abv = 5  # default

    # Get bitter
    bitter = request.form['bitter']
    if bitter not in ('yes', 'no'):
        bitter = 'no'

    # Get neighbors and sanitize
    neighbors = request.form['neighbors']
    try:
        neighbors = min(max(int(neighbors), 1), 10)  # max display of 10 beers min of 1
    except ValueError:
        neighbors = 1  # default

    # Search beers
    user_input = json.dumps({"abv": abv, "text": text, "bitter": bitter, "neighbors": neighbors})
    best_beers = closest_beer(user_input)

    # compile results
    beer_ids = json.loads(best_beers)['beer_id']
    details = beer_details(beer_ids)
    return render_template('index.html', results=beer_ids, details=details)


if __name__ == '__main__':
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")
    # Production
    http_server = WSGIServer(('', 80), app)
    http_server.serve_forever()
