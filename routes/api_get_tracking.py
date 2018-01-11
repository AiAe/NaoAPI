from flask import request, jsonify
from helpers import mysql


def api():
    connection, cursor = mysql.connect()
    user_id = request.args.get('user_id')

    if user_id:

        find_user = mysql.execute(connection, cursor, "SELECT * FROM tracking WHERE user_id = %s",
                                  [user_id]).fetchone()

        return jsonify(find_user)
    else:
        return 'User not found!'
