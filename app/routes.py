from app.static.student.Main import *
from app.static.student.utils import *
from app import app
from flask import render_template, url_for

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index():
    context = {
        'title': 'RickoIpsum'
    }
    return render_template('index.html', **context)

@app.route('/tree')
def tree():
    context = {
        'title': 'Tree'
    }
    return render_template('tree.html', **context)

@app.route('/reinforcement')
def reinforcement():
    context = {
        'title': 'Reinforcement Learning'
    }
    return render_template('reinforcement.html', **context)

@app.route('/search')
def search():
    context = {
        'title': 'Search',
    }
    return render_template('search.html', **context)

@app.route('/search/draw', methods=['POST'])
def drawAll():
    return drawBoard()

@app.route('/search/solvebfs', methods=['POST'])
def solution():
    return solveBFS()

@app.route('/search/clear', methods=['POST'])
def clearAll():
    return clear()

