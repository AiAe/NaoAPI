from flask import request, jsonify
from helpers import mysql, user_exist

table = ["user_id", "username", "twitch_username", "code"]

def api():
    user_id = request.args.get('user_id')
    update = request.args.get('update')

    if user_id and user_exist.user() and update in table:
        connection, cursor = mysql.connect()

        return jsonify({"code": "1", "message": "User updated!"})
    else:
        return jsonify({"code": "0", "message": "Bad POST request"})
