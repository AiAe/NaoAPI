from sanic.response import json
from helpers import mysql
import aiohttp
import os
import json as j


with open("/home/ubuntu/NaoAPI/twitch.json", "r") as f:
    config = j.load(f)


async def oauth(data):
    async with aiohttp.ClientSession() as session:
        async with session.post('https://api.twitch.tv/kraken/oauth2/token', data=data) as resp:
            r = await resp.json()

            return r


async def kraken_api(data):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.twitch.tv/kraken/', headers=data) as resp:
            r = await resp.json()

            return r


async def api(request):
    code = request.args['state'][0]

    if code:
        find_user = await mysql.execute("SELECT user_id, twitch_username FROM users WHERE token = %s", [code])

        if not find_user:
            return json({"code": "0", "message": "User not found!"})
        
        twitch_data = {
            'client_id': config["twitch_client"],
            'client_secret': config["twitch_secret"],
            'grant_type': 'authorization_code',
            'redirect_uri': config["twitch_redirect"],
            'code': request.args['code'][0]
        }

        twitch_api = await oauth(twitch_data)

        if "status" in str(twitch_api):
            return json({"code": "0", "message": "Something went wrong!"})

        headers = {
            'Authorization': 'OAuth ' + twitch_api['access_token']
        }

        user = await kraken_api(headers)

        await mysql.execute("UPDATE users SET twitch_username = %s WHERE token = %s", [user["token"]["user_name"],
                                                                                       code])

        if find_user["twitch_username"]:
            return json({"code": "1", "message": "Username is updated!"})
        return json({"code": "1", "message": "User connected to Twitch."})

    return json({"code": "0", "message": "Something went wrong!"})
