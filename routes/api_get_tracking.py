from flask import request, jsonify
from helpers import mysql


def api():
    connection, cursor = mysql.connect()
    user_id = request.args.get('user_id')
    twitch = request.args.get('twitch')

    if twitch:
        find_channel = mysql.execute(connection, cursor, "SELECT user_id FROM users WHERE twitch_username = %s",
                                     [twitch]).fetchone()

        user_id = find_channel["user_id"]

    if user_id:
        find_user = mysql.execute(connection, cursor, "SELECT * FROM tracking WHERE user_id = %s",
                                  [user_id]).fetchone()
        if find_user:
            return jsonify(find_user)

    return 'User not found!'
