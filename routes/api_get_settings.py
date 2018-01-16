from flask import request, jsonify
from helpers import mysql


def api():
    connection, cursor = mysql.connect()
    user_id = request.args.get('user_id')

    if user_id:
        find_user = mysql.execute(connection, cursor, "SELECT * FROM settings WHERE user_id = %s",
                                  [user_id]).fetchone()
        if find_user:
            return jsonify(find_user)

    return 'User not found!'
