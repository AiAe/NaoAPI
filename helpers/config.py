import json
import os


def flask():
    try:
        with open(os.getcwd() + "/flask.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        with open("/home/ubuntu/NaoAPI/flask.json", "r") as f:
            config = json.load(f)

    return config
