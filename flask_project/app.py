from flask import Flask, render_template, redirect, Markup
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/marsAssignament")

@app.route("/")
def home():
    marsScrapeDocument = mongo.db.marsscrape.find_one()
    return render_template("index.html", marsScrapeDocument=marsScrapeDocument, htmlTable= Markup(marsScrapeDocument['marsFactsHtml']))


@app.route("/scrape")
def scrape():
    marsScrapeDocument = scrape_mars.main()
    mongo.db.marsscrape.update({}, marsScrapeDocument, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
