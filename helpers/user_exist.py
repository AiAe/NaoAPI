from flask import request
from helpers import mysql


def user():
    connection, cursor = mysql.connect()

    user_id = request.args.get('user_id')

    get_tokens = mysql.execute(connection, cursor, "SELECT user_id FROM users WHERE user_id = %s",
                               [user_id]).fetchone()

    if get_tokens:
        return True

    return False
