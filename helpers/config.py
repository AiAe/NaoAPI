import json


def flask():
    with open("./flask.json", "r") as f:
        flask = json.load(f)

    return flask
