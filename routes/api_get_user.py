from flask import request, jsonify
from helpers import mysql


def api():
    connection, cursor = mysql.connect()
    user_id = request.args.get('user_id')

    if user_id:

        find_user = mysql.execute(connection, cursor,
                                  "SELECT user_id, username, twitch_username FROM users WHERE user_id = %s",
                                  [user_id]).fetchone()
        if find_user:
            find_user.update({"code": "1"})
            return jsonify(find_user)

    return jsonify({"code": "0", "message": "User not found!"})
