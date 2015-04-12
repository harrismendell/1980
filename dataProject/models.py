__author__ = 'sunnyharris'
import pymysql
from flask import Flask, flash, redirect, url_for, request, get_flashed_messages, g
from flask.ext.login import LoginManager, UserMixin, current_user, login_user
from dataProject import login_manager


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
    with g.db.cursor() as cursor:
        cursor.execute("INSERT INTO user (username, password) VALUES (%s,%s)", (username, password))
        g.db.commit()
        user_id = cursor.execute('SELECT id FROM user WHERE username=%s', username)
    return User(user_id, username, password)


def insert_band(band, start_year, end_year, genre):
    # Connect to the database
    with g.db.cursor() as cursor:
        values = '\'' + band + '\' , \'' + start_year + '\' , \'' + end_year + '\' , \'' + genre + '\''
        sql = 'INSERT INTO bands (band_name, start_year, end_year, genre) VALUES (' + values + ')'
        cursor.execute(sql)
        g.db.commit()


# Explore functions

def get_bands(data):
    start_year = data['start'] or 2050
    end_year = data['end'] or 0 
    genre = data['genre']
    label = data['label']
    with g.db.cursor() as cursor:
        result = ''
        if label == "" and genre == "All":
            cursor.execute('SELECT * from bands WHERE start_year >= %s and end_year <= %s', (start_year, end_year))
            result = cursor.fetchall()

        elif label == "":
            cursor.execute('SELECT * from bands WHERE start_year >= %s and end_year <= %s and genre=%s', (start_year, end_year, genre))
            result = cursor.fetchall()

        elif genre == "All":
            import ipdb; ipdb.set_trace()
            cursor.execute('SELECT * from bands NATURAL JOIN label_released WHERE start_year >= %s and end_year <= %s and company_name LIKE %s', (start_year, end_year, label))
            result = cursor.fetchall()

            










