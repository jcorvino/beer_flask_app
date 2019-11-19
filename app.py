from flask import Flask, render_template
import pandas as pd


app = Flask(__name__)

# Use pandas to load csv data
df = pd.read_csv('beers-cleaned.csv')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/beers")
def beers():
    return "Finding beers!"


if __name__ == "__main__":
    app.run()
