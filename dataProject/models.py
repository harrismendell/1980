__author__ = 'sunnyharris'
import pymysql
from flask import Flask, flash, redirect, url_for, request, get_flashed_messages, g
from flask.ext.login import LoginManager, UserMixin, current_user, login_user
from dataProject import login_manager
from pymysql import InternalError, IntegrityError
import os
import webbrowser


class User(UserMixin):
    def __init__(self, id, name, password, is_admin=0, active=True):
        self.id = name
        self.name = name
        self.password = password
        self.active = active
        self.is_admin = is_admin

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    @classmethod
    def get(self_class, name):
        with g.db.cursor() as cursor:
            cursor.execute('SELECT * from user WHERE username = %s', name)
            result = cursor.fetchone()
            return User(result['id'], result['username'], result['password'], result['is_admin'])


@login_manager.user_loader
def load_user(username):
    with g.db.cursor() as cursor:
        cursor.execute('SELECT * from user WHERE username = %s', username)
        result = cursor.fetchone()
        return User(result['id'], result['username'], result['password'], result['is_admin'])


def insert_user(username, password):
    if check_for_sql_injection(username, password):
        return "si"

    with g.db.cursor() as cursor:
        cursor.execute("INSERT INTO user (username, password) VALUES (%s,%s)", (username, password))
        g.db.commit()
        user_id = cursor.execute('SELECT id FROM user WHERE username=%s', username)
    return User(user_id, username, password)


def insert_band(band, start_year, end_year, genre):
    if check_for_sql_injection(band, start_year, end_year, genre):
        return "si"

    # Connect to the database
    with g.db.cursor() as cursor:
        values = '\'' + band + '\' , \'' + start_year + '\' , \'' + end_year + '\' , \'' + genre + '\''
        sql = 'INSERT INTO bands (band_name, start_year, end_year, genre) VALUES (' + values + ')'
        cursor.execute(sql)
        g.db.commit()
    return "si"

def insert_record(band_name, record_title, release):
    if check_for_sql_injection(band_name, record_title, release):
        return "si"

    with g.db.cursor() as cursor:
        cursor.execute('INSERT INTO records (record_title, release_date, band_name) VALUES (%s, %s, %s)', (record_title, release, band_name))
        g.db.commit()
    return ''

def insert_song(data):
    if data['length'].count(':') == 1:
        length = '00:' + data['length']
    else:
        length = data['length']

    if check_for_sql_injection(data['song'], data['record_title'], length, data['release']):
        return "si"

    with g.db.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO songs (song_title, record_title, length, release_date) VALUES (%s,%s,%s,%s)', (data['song'], data['record_title'], length, data['release']))
        except InternalError:
            return "invalid date"

        g.db.commit()
        return "good"


# Explore functions

def get_bands(data):
    start_year = data['start'] or 0
    end_year = data['end'] or 2050
    genre = data['genre']

    if check_for_sql_injection(start_year, end_year, genre):
        return "si"

    with g.db.cursor() as cursor:
        result = ''
        if genre == "All":
            cursor.execute('SELECT * from bands WHERE start_year >= %s and end_year <= %s', (start_year, end_year))
            result = cursor.fetchall()

        else:
            cursor.execute('SELECT * from bands WHERE start_year >= %s and end_year <= %s and genre=%s', (start_year, end_year, genre))
            result = cursor.fetchall()
    return result

def find_specific_band(band_name):
    with g.db.cursor() as cursor:
        cursor.execute('SELECT * from bands WHERE band_name=%s', (band_name))
        return cursor.fetchone()

def get_records(band_name):
    with g.db.cursor() as cursor:
        cursor.execute('SELECT * from records WHERE band_name=%s', (band_name))
        return cursor.fetchall()

def get_songs(band_name):
    with g.db.cursor() as cursor:
        cursor.execute('SELECT * from bands NATURAL JOIN records NATURAL JOIN songs WHERE band_name=%s', (band_name))
        return cursor.fetchall()

def get_more_songs(data):
    band_name = data['band']
    start_year = data['start'] or 0
    end_year = data['end'] or 2050
    genre = data['genre']

    if check_for_sql_injection(band_name, start_year, end_year, genre):
        return "si"

    with g.db.cursor() as cursor:
        result = ''
        if band_name:
            cursor.execute('SELECT * from allsonginfo WHERE band_name = %s and (release_date >= %s and release_date <= %s)', ( band_name, start_year, end_year))
            result = cursor.fetchall()

        elif genre == "All":
            cursor.execute('SELECT * from allsonginfo WHERE release_date >= %s and release_date <= %s', (start_year, end_year))
            result = cursor.fetchall()

        else:
            cursor.execute('SELECT * from allsonginfo WHERE genre = %s AND (release_date >= %s and release_date <= %s)', (genre, start_year, end_year))
            result = cursor.fetchall()
    return result


def remove_song(song):
    with g.db.cursor() as cursor:
        cursor.execute('DELETE from songwriter WHERE song_title=%s', song)
        cursor.execute('DELETE from songs WHERE song_title=%s', song)
        g.db.commit()

def remove_band(band):
    with g.db.cursor() as cursor:
        cursor.execute('DELETE x from bands w NATURAL JOIN records e NATURAL JOIN songs s NATURAL JOIN songwriter x WHERE band_name=%s', band)

        cursor.execute('DELETE x from bands w NATURAL JOIN records e NATURAL JOIN label_released x WHERE band_name=%s', band)

        cursor.execute('DELETE w, e from songs w NATURAL JOIN records e WHERE band_name=%s', band)
        cursor.execute('DELETE from bands WHERE band_name=%s', band)
        g.db.commit()

def check_for_sql_injection(*args):
    for arg in args:
        if not isinstance(arg, int):
            if "\'" in arg:
                return True
    return False

def export_db():
    os.system("mysqldump --host=stardock.cs.virginia.edu --user=cs4750hbm2qc --password=cs47501980 cs4750hbm2qc > database.sql")
    webbrowser.open("file:///Users/sunnyharris/1980_new/1980/database.sql")
