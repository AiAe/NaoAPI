from flask import request, jsonify
from helpers import mysql, user_exist, ripple

table = ["username", "twitch_username", "code"]


def api():
    user_id = request.args.get('user_id')
    update = request.args.get('update')
    value = request.args.get('value')

    if user_id and user_exist.user() and update in table:
        connection, cursor = mysql.connect()

        user = ripple.get_user(user_id)

        if not user["code"] == 0:

            if update == "username":
                mysql.execute(connection, cursor, "UPDATE users SET username = %s WHERE user_id = %s",
                              [user["username"], user_id])
            elif update == "twitch_username" and value:
                mysql.execute(connection, cursor, "UPDATE users SET twitch_username = %s WHERE user_id = %s",
                              [value, user_id])
            elif update == "code" and value:
                mysql.execute(connection, cursor, "UPDATE users SET code = %s WHERE user_id = %s",
                              [value, user_id])
            else:
                return jsonify({"code": "0", "message": "Something went wrong!"})

            return jsonify({"code": "1", "message": "User updated!"})

    return jsonify({"code": "0", "message": "Bad POST request!"})
