#!/usr/bin/python
import sqlite3
import os.path

from flask import Flask, g, render_template, request, url_for
#from gevent.wsgi import WSGIServer
from pagination import Pagination

DATABASE = "quotes.sqlite3" #os.path.join(os.path.expanduser("~/.lala"), "quotes.sqlite3")
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config["DATABASE"])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

def get_quotes_for_page(page, PER_PAGE=25):
    return g.db.execute("select quote, rowid from quote limit (?) offset (?)",
            [PER_PAGE, (page - 1 ) * PER_PAGE])

@app.route("/quotes/", defaults = {"page": 1})
@app.route("/quotes/<int:page>")
def all(page):
    num_quotes = g.db.execute("select count(rowid) from quote;").fetchone()[0]
    p = Pagination(page, 25, num_quotes)
    quotes = [dict(quote=row[0], id=row[1]) for row in
            get_quotes_for_page(page, 25)]
    return render_template("allquotes.html", quotes=quotes, pagination=p)

@app.route("/random")
def random_quote():
    row = g.db.execute("SELECT rowid, quote FROM quote\
            ORDER BY random() LIMIT 1;").fetchall()[0]
    quote = dict(id=row[0], quote=row[1])
    return render_template("singlequote.html", quote=quote)

@app.route("/quote/<int:id>")
def single_quote(id):
    row = g.db.execute("SELECT rowid, quote FROM quote\
            WHERE rowid = (?)", [id]).fetchall()[0]
    quote = dict(id=row[0], quote=row[1])
    return render_template("singlequote.html", quote=quote)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/live")
def live():
    return render_template("live.html")

def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

app.jinja_env.globals['url_for_other_page'] = url_for_other_page

if __name__ == '__main__':
    # Use this to get the server to listen on a public interface:
    #http_server = WSGIServer(('10.8.0.10', 5000), app)
    #http_server.serve_forever()
    # Or this for localhost:
    app.run()
