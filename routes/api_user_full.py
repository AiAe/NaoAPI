from flask import request, jsonify
from helpers import mysql, group


def api():
    connection, cursor = mysql.connect()
    user_id = request.args.get('user_id')

    if user_id:

        full = {}

        find_user = mysql.execute(connection, cursor,
                                  "SELECT user_id, username, twitch_username FROM users WHERE user_id = %s",
                                  [user_id]).fetchone()

        find_settings = mysql.execute(connection, cursor,
                                      "SELECT * FROM settings WHERE user_id = %s",
                                      [user_id]).fetchone()

        find_tracking = mysql.execute(connection, cursor,
                                      "SELECT * FROM tracking WHERE user_id = %s",
                                      [user_id]).fetchone()

        full.update(find_user)
        full.update(find_settings)
        full.update(find_tracking)
        full.update(group.get_group(find_settings["privileges"]))

        return jsonify(full)
    else:
        return 'User not found!'
