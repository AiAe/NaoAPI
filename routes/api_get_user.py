from sanic.response import json
from helpers import mysql


async def api(request):
    user_id = request.args["user_id"][0]

    if user_id:
        find_user = await mysql.execute("SELECT * FROM users WHERE user_id = %s", [user_id])

        if find_user:
            find_user.update({"code": "1"})

            return json(find_user)

    return json({"code": "0", "message": "User not found!"})
