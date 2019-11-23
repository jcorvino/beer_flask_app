from flask import Flask, render_template
import pandas as pd


app = Flask(__name__)

# Use pandas to load csv data
# read_cols = ['id', 'brewery_id', 'name', 'cat_id', 'style_id', 'abv', 'ibu', 'srm', 'upc', 'descript']
# df = pd.read_csv('beers-cleaned.csv', encoding='latin-1', usecols=read_cols)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/beers")
def beers():
    return "Finding beers!"


if __name__ == "__main__":
    app.run()
