from flask import request, jsonify
from helpers import mysql, config
import requests


def api():
    code = request.args.get('state')

    if code:
        connection, cursor = mysql.connect()

        find_user = mysql.execute(connection, cursor, "SELECT user_id, twitch_username FROM users WHERE token = %s", [code]).fetchone()

        if not find_user:
            return jsonify({"code": "0", "message": "User not found!"})

        twitch_data = {
            'client_id': config.twitch()["twitch_client"],
            'client_secret': config.twitch()["twitch_secret"],
            'grant_type': 'authorization_code',
            'redirect_uri': config.twitch()["twitch_redirect"],
            'code': request.args['code']
        }

        twitch_api = requests.post("https://api.twitch.tv/kraken/oauth2/token", data=twitch_data).json()

        if "status" in str(twitch_api):
            return jsonify({"code": "0", "message": "Something went wrong!"})

        headers = {
            'Authorization': 'OAuth ' + twitch_api['access_token']
        }

        user = requests.get('https://api.twitch.tv/kraken/', headers=headers).json()

        mysql.execute(connection, cursor,
                      "UPDATE users SET twitch_username = %s WHERE token = %s", [user["token"]["user_name"],
                                                                                 code])
        if find_user["twitch_username"]:
            return jsonify({"code": "1", "message": "Username is updated!"})
        return jsonify({"code": "1", "message": "User connected to Twitch."})

    return jsonify({"code": "0", "message": "Something went wrong!"})
