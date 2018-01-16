from flask import request, jsonify
from helpers import mysql, user_exist

table = ["bot", "requests", "privileges", "std_pp", "taiko_pp", "ctb_pp", "mania_pp", "format_score_osu",
         "format_score_twitch", "format_request_osu", "format_request_twitch"]


def api():
    user_id = request.args.get('user_id')
    update = request.args.get('update')
    value = request.args.get('value')

    if user_id and user_exist.user() and update in table and value:
        connection, cursor = mysql.connect()

        if update == "bot":
            if value != 0:
                value = 1

            mysql.execute(connection, cursor, "UPDATE settings SET bot = %s WHERE user_id = %s",
                          [value, user_id])
        elif update == "requests":
            if value != 0:
                value = 1

            mysql.execute(connection, cursor, "UPDATE settings SET requests = %s WHERE user_id = %s",
                          [value, user_id])
        elif update == "privileges":
            return jsonify({"code": "0", "message": "Update privileges is disabled!"})
        elif update == "std_pp":
            mysql.execute(connection, cursor, "UPDATE settings SET std_pp = %s WHERE user_id = %s",
                          [value, user_id])
        elif update == "taiko_pp":
            mysql.execute(connection, cursor, "UPDATE settings SET taiko_pp = %s WHERE user_id = %s",
                          [value, user_id])
        elif update == "ctb_pp":
            mysql.execute(connection, cursor, "UPDATE settings SET ctb_pp = %s WHERE user_id = %s",
                          [value, user_id])
        elif update == "mania_pp":
            mysql.execute(connection, cursor, "UPDATE settings SET mania_pp = %s WHERE user_id = %s",
                          [value, user_id])
        elif update == "format_score_osu":
            mysql.execute(connection, cursor, "UPDATE settings SET format_score_osu = %s WHERE user_id = %s",
                          [value, user_id])
        elif update == "format_score_twitch":
            mysql.execute(connection, cursor, "UPDATE settings SET format_score_twitch = %s WHERE user_id = %s",
                          [value, user_id])
        elif update == "format_request_osu":
            mysql.execute(connection, cursor, "UPDATE settings SET format_request_osu = %s WHERE user_id = %s",
                          [value, user_id])
        elif update == "format_request_twitch":
            mysql.execute(connection, cursor, "UPDATE settings SET format_request_twitch = %s WHERE user_id = %s",
                          [value, user_id])
        return jsonify({"code": "1", "message": "User settings updated!"})
    else:
        return jsonify({"code": "0", "message": "Bad POST request"})
