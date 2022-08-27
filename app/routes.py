from flask import render_template
from app import app

@app.route('/')

@app.route('/index')
def index():
    user = {"username": "Daisy"}
    return render_template('index.html', title="Home", user=user)

@app.route('/queries')
def queries():
    return render_template('queries.html', title="Queries")

@app.route('/downloads')
def downloads():
    return render_template('downloads.html', title="Downloads")