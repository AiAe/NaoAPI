from sanic.response import json
from helpers import mysql


async def api(request):
    user_id = request.args['user_id'][0]
    twitch = request.args['twitch'][0]

    if twitch:
        find_channel = await mysql.execute("SELECT user_id FROM users WHERE twitch_username = %s", [twitch])

        user_id = find_channel["user_id"]

    if user_id:
        find_user = await mysql.execute("SELECT * FROM tracking WHERE user_id = %s", [user_id])

        if find_user:
            return json(find_user)

    return json({"code": "0", "message": "User not found!"})
