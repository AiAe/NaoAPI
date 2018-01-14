from flask import jsonify, request
from helpers import mysql


def api():
    connection, cursor = mysql.connect()
    twitch = request.args.get('twitch')

    if twitch:
        results = mysql.execute(connection, cursor,
                                "SELECT user_id, twitch_username FROM users WHERE twitch_username IS NOT NULL").fetchall()
    else:
        user_list = mysql.execute(connection, cursor, "SELECT user_id FROM users").fetchall()

        results = {
            "type": "subscribe_scores",
            "data": user_list
        }

    return jsonify(results)
