from flask import request
from functools import wraps
from helpers import mysql


def valid_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        connection, cursor = mysql.connect()

        token = request.args.get('token')

        get_tokens = mysql.execute(connection, cursor, "SELECT token FROM access_keys WHERE token = %s",
                                   [token]).fetchone()

        if get_tokens:
            return f(*args, **kwargs)

        return 'Invalid token!'

    return wrapper
