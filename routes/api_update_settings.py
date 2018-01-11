from flask import request, jsonify
from helpers import mysql

def api():
    connection, cursor = mysql.connect()
    user_id = request.args.get('user_id')

    if user_id:

        return ''
    else:
        return 'User not found!'