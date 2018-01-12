from flask import request, jsonify
from helpers import mysql, user_exist

table = ["user_id", "bot", "requests", "privileges", "std_pp", "taiko_pp", "ctb_pp", "mania_pp", "format_score_osu",
         "format_score_twitch", "format_request_osu", "format_request_twitch"]


def api():
    user_id = request.args.get('user_id')
    update = request.args.get('update')

    if user_id and user_exist.user() and update in table:
        connection, cursor = mysql.connect()

        return jsonify({"code": "1", "message": "User settings updated!"})
    else:
        return jsonify({"code": "0", "message": "Bad POST request"})
