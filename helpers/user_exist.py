from flask import request
from helpers import mysql


def user():
    connection, cursor = mysql.connect()

    user_id = request.args.get('user_id')

    u = mysql.execute(connection, cursor, "SELECT user_id FROM users WHERE user_id = %s",
                         [user_id]).fetchone()

    if u:
        return True

    return False
