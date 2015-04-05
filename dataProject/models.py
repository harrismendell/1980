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

def insert_band(band, start_year, end_year, genre):
    # Connect to the database
    with g.db.cursor() as cursor:
        values = '\'' + band + '\' , \'' + start_year + '\' , \'' + end_year + '\' , \'' + genre + '\''
        sql = 'INSERT INTO bands (band_name, start_year, end_year, genre) VALUES (' + values + ')'
        import ipdb; ipdb.set_trace()
        cursor.execute(sql)
        g.db.commit()

