from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, session
import dlrsstoemail.rssreader
import xml.etree.ElementTree as et
import re
import sqlite3

#RFC 5322 standard of email validation regular expression
REGEX_URL = "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"

app = Flask(__name__)
app.secret_key = "admin123" #session key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rss.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
db.app = app

class rss(db.Model):
    __tablename__ = "rss"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    rss_url = db.Column(db.Text)

    def __init__(self, rss_url):
        self.rss_url = rss_url

@app.route('/', methods=["POST", "GET"])
def home():
    records = ["empty"]
    if request.method == "POST":
        url = request.form["rss_url"]
        if (url != ''):
            entry = rss(url)
            db.session.add(entry)
            db.session.commit()
            flash("Dodano nowy URL")
            records = session.query(rss).all()
        else:
            flash("Niepoprawny URL")

    return render_template("index.html", rss_tab = records)

@app.route('/getPreview')
def get_preview(methods=["POST","GET"]):
    if request.method == "GET":
        rssreader.get_rss_content(session.query(rss).order_by(rss.id.desc()).first())
        preview = 'preview'
        print(preview)
    return render_template("index.html", preview = preview)

if __name__ == "__main__":
    db.create_all()
    app.run()
