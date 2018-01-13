from flask import Flask
from helpers import config, validate_token
from routes import api_list, api_get_user, api_get_settings, \
    api_get_tracking, api_update_settings, api_update_tracking, \
    api_update_user, api_insert_user

app = Flask(__name__)


@app.route('/')
def index():
    return ("<div style='line-height: 1;'>"
            "╭━╮╱╭╮╱╱╱╱╱╭━━━┳━━━┳━━╮╱╱╱╭╮╱╭━━━╮<br>"
            "┃┃╰╮┃┃╱╱╱╱╱┃╭━╮┃╭━╮┣┫┣╯╱╱╭╯┃╱┃╭━╮┃<br>"
            "┃╭╮╰╯┣━━┳━━┫┃╱┃┃╰━╯┃┃┃╱╭╮┣╮┃╱┃┃┃┃┃<br>"
            "┃┃╰╮┃┃╭╮┃╭╮┃╰━╯┃╭━━╯┃┃╱┃╰╯┃┃╱┃┃┃┃┃<br>"
            "┃┃╱┃┃┃╭╮┃╰╯┃╭━╮┃┃╱╱╭┫┣╮╰╮╭╯╰┳┫╰━╯┃<br>"
            "╰╯╱╰━┻╯╰┻━━┻╯╱╰┻╯╱╱╰━━╯╱╰┻━━┻┻━━━╯<br>"
            "</div>")


@app.errorhandler(404)
def not_found(error):
    return error


@app.route('/api/full', methods=['GET'])
@validate_token.valid_token
def route_api_list():
    return api_list.api()


@app.route('/api/get_user', methods=['GET'])
@validate_token.valid_token
def route_api_get_user():
    return api_get_user.api()


@app.route('/api/get_settings', methods=['GET'])
@validate_token.valid_token
def route_api_get_settings():
    return api_get_settings.api()


@app.route('/api/get_tracking', methods=['GET'])
@validate_token.valid_token
def route_api_get_tracking():
    return api_get_tracking.api()


@app.route('/api/update/user', methods=['POST'])
@validate_token.valid_token
def route_api_update_user():
    return api_update_user.api()


@app.route('/api/update/settings', methods=['POST'])
@validate_token.valid_token
def route_api_update_settings():
    return api_update_settings.api()


@app.route('/api/update/tracking', methods=['POST'])
@validate_token.valid_token
def route_api_update_tracking():
    return api_update_tracking.api()


@app.route('/api/insert/user', methods=['POST'])
@validate_token.valid_token
def route_api_insert_user():
    return api_insert_user.api()

if __name__ == "__main__":
    app.run(**config.flask())
