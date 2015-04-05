from flask import render_template, g
from dataProject import app
import pymysql
from models import get_bands
import sqlite3 as sql

# routes
@app.route('/')
def title_screen():
    bands = get_bands()
    import pdb; pdb.set_trace()
    return render_template('main.html')

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