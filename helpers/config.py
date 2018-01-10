import json


def mysql():
    with open("./mysql.json", "r") as f:
        mysql = json.load(f)

    return mysql


def flask():
    with open("./flask.json", "r") as f:
        flask = json.load(f)

    return flask
