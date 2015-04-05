from flask import render_template, g, request
from dataProject import app
import pymysql
from models import get_bands, insert_band
import sqlite3 as sql

# routes
@app.route('/')
def title_screen():
    bands = get_bands()
    return render_template('layout.html')

@app.route('/contribute')
def contribute():
    bands = get_bands()
    return render_template('contribute.html')

@app.route('/contribute_band')
def contribute_band():
    return render_template('contribute_band.html')

@app.route('/contribute_record')
def contribute_record():
    return render_template('contribute_record.html')

@app.route('/contribute_song')
def contribute_song():
    return render_template('contribute_song.html')

@app.route('/submit', methods=['POST'])
def submit():
    insert_band(request.form['band'], request.form['start'], request.form['end'], request.form['genre'])
    return render_template('confirm.html')

@app.before_request
def db_connect():
    g.db = pymysql.connect(host='stardock.cs.virginia.edu',
                           user='cs4750hbm2qc',
                           passwd='cs47501980',
                           db='cs4750hbm2qc',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

@app.teardown_request
def db_disconnect(exception=None):
    g.db.close()