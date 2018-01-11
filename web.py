from flask import Flask, jsonify, request
from helpers import config, privileges, mysql
from functools import wraps

app = Flask(__name__)


def valid_token(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        connection, cursor = mysql.connect()

        token = request.args.get('token')

        get_tokens = mysql.execute(connection, cursor, "SELECT token FROM access_keys WHERE token = %s",
                                   [token]).fetchone()

        if get_tokens:
            return function(*args, **kwargs)

        return 'Invalid token!'

    return wrapper


def group(p):
    if privileges.hasuser(p):
        group = "User"

    elif privileges.hasuserdonator(p):
        group = "Donator"

    elif privileges.hasadmin(p):
        group = "Admin"

    elif privileges.hasuserrestricted(p):
        group = "Restricted"

    return {"group": group}


@app.route('/')
def index():
    return 'NaoAPI'


@app.errorhandler(404)
def not_found(error):
    return '404'


@app.route('/api/full', methods=['GET'])
@valid_token
def api_list():
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
        full.update(group(find_settings["privileges"]))

        return jsonify(full)
    else:
        return 'User not found!'


@app.route('/api/get_user', methods=['GET'])
@valid_token
def api_get_user():
    connection, cursor = mysql.connect()
    user_id = request.args.get('user_id')

    if user_id:

        find_user = mysql.execute(connection, cursor,
                                  "SELECT user_id, username, twitch_username FROM users WHERE user_id = %s",
                                  [user_id]).fetchone()

        return jsonify(find_user)
    else:
        return 'User not found!'


@app.route('/api/get_settings', methods=['GET'])
@valid_token
def api_get_settings():
    connection, cursor = mysql.connect()
    user_id = request.args.get('user_id')

    if user_id:

        find_user = mysql.execute(connection, cursor, "SELECT * FROM settings WHERE user_id = %s",
                                  [user_id]).fetchone()

        return jsonify(find_user)
    else:
        return 'User not found!'


@app.route('/api/get_tracking', methods=['GET'])
@valid_token
def api_get_tracking():
    connection, cursor = mysql.connect()
    user_id = request.args.get('user_id')

    if user_id:

        find_user = mysql.execute(connection, cursor, "SELECT * FROM tracking WHERE user_id = %s",
                                  [user_id]).fetchone()

        return jsonify(find_user)
    else:
        return 'User not found!'


@app.route('/api/update/user')
@valid_token
def api_update_user():
    connection, cursor = mysql.connect()
    user_id = request.args.get('user_id')

    if user_id:

        return ''
    else:
        return 'User not found!'


@app.route('/api/update/settings')
@valid_token
def api_update_settings():
    connection, cursor = mysql.connect()
    user_id = request.args.get('user_id')

    if user_id:

        return ''
    else:
        return 'User not found!'


@app.route('/api/update/tracking')
@valid_token
def api_update_tracking():
    connection, cursor = mysql.connect()
    user_id = request.args.get('user_id')

    if user_id:

        return ''
    else:
        return 'User not found!'


if __name__ == "__main__":
    app.run(**config.flask())
