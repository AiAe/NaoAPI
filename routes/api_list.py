from sanic.response import json
from helpers import mysql


async def api(request):
    twitch = request.args['twitch'][0]

    if twitch:
        results = await mysql.execute("SELECT user_id, twitch_username FROM users WHERE twitch_username IS NOT NULL")
    else:
        user_list = await mysql.execute("SELECT user_id FROM users")

        results = {
            "type": "subscribe_scores",
            "data": user_list
        }

    return json(results)
