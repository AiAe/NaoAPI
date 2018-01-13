import json
import os


def flask():
    with open(os.getcwd() + "/flask.json", "r") as f:
        config = json.load(f)

    return config
