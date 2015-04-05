__author__ = 'sunnyharris'
import pymysql
from flask import g


def get_bands():
    # Connect to the database
    with g.db.cursor() as cursor:
        sql = 'SELECT * from bands'
        cursor.execute(sql)
        result = cursor.fetchall()

    return result

