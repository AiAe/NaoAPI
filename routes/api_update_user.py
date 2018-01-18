from sanic.response import json
from helpers import mysql, user_exist, ripple

table = ["username", "twitch_username", "code"]


async def api(request):
    user_id = request.args['user_id'][0]
    update = request.args['update'][0]
    value = request.args['value'][0]

    if user_id and user_exist.user() and update in table:
        user = ripple.get_user(user_id)

        if not user["code"] == 0:

            if update == "username":
                await mysql.execute("UPDATE users SET username = %s WHERE user_id = %s",
                              [user["username"], user_id])
            elif update == "twitch_username" and value:
                await mysql.execute("UPDATE users SET twitch_username = %s WHERE user_id = %s",
                              [value, user_id])
            elif update == "code" and value:
                await mysql.execute("UPDATE users SET code = %s WHERE user_id = %s",
                              [value, user_id])
            else:
                return json({"code": "0", "message": "Something went wrong!"})

            return json({"code": "1", "message": "User updated!"})

    return json({"code": "0", "message": "Bad POST request!"})
