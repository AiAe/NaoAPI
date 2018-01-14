import json
import pymysql
import os

try:
    with open(os.getcwd() + "/mysql.json", "r") as f:
        config = json.load(f)
except FileNotFoundError:
    with open("/home/ubuntu/NaoAPI/mysql.json", "r") as f:
        config = json.load(f)


def connect():
    connection = pymysql.connect(host=config['host'], user=config['username'], passwd=config['password'],
                                 db=config['db'],
                                 charset='utf8')
    connection.autocommit(True)
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    return connection, cursor


def execute(connection, cursor, sql, args=None):
    try:
        cursor.execute(sql, args) if args is not None else cursor.execute(sql)
        return cursor
    except pymysql.err.OperationalError:
        connection.connect()
        return execute(sql, args)
