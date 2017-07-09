# -*- coding: utf-8 -*-
from flask import Flask, render_template
import os, datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

POSTGRES = {
    'user': os.environ['DATABASE_USER'],
    'pw': os.environ['DATABASE_PASSWORD'],
    'db': os.environ['DATABASE_NAME'],
    'host': 'localhost',
    'port': '5432',
}

#app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db = SQLAlchemy(app)
db.init_app(app)

class Emoji(db.Model):
    """Model for the emojis table"""
    __tablename__ = 'emojis'

    id = db.Column(db.Integer, primary_key=True)
    emoji = db.Column(db.TEXT, nullable=False)
    text = db.Column(db.TEXT)
    author = db.Column(db.TEXT)
    datetime = db.Column(db.TIMESTAMP)

    def __init__(self, code, text, author):
        self.emoji = code
        self.text = text
        self.author = author
        self.datetime = str(datetime.datetime.now())   
     
@app.route("/")
def main():
    emojis = Emoji.query.order_by(Emoji.id.asc()).all()
    return render_template('home.html', emojis=emojis)

@app.route("/<code>")
def emoji(code):
    emoji = Emoji.query.filter_by(emoji=code).first() 
    return render_template('emoji.html', emoji=emoji)

"""
@app.route("/populate")
def populate():
    with open('emojis.txt', 'r') as f:
        for line in f:
            e = Emoji(
                line.rstrip(),
                None,
                None,
            )
            print e.emoji
            db.session.add(e)
            db.session.commit()
"""

if __name__ == '__main__':
    app.run()
