from sanic.response import json
from helpers import mysql, user_exist

table = ["bot", "requests", "privileges", "std_pp_limit", "taiko_pp_limit", "ctb_pp_limit", "mania_pp_limit",
         "format_score_osu", "format_score_twitch", "format_request_osu", "format_request_twitch"]


async def api(request):
    user_id = request.args['user_id'][0]
    update = request.args['update'][0]
    value = request.args['value'][0]

    if user_id and user_exist.user() and update in table and value:
        if update == "bot":
            if value != "0":
                value = "1"

            await mysql.execute("UPDATE settings SET bot = %s WHERE user_id = %s",
                          [value, user_id])
        elif update == "requests":
            if value != "0":
                value = "1"

            await mysql.execute("UPDATE settings SET requests = %s WHERE user_id = %s",
                          [value, user_id])
        elif update == "privileges":
            return json({"code": "0", "message": "Update privileges is disabled!"})
        elif update == "std_pp_limit":
            await mysql.execute("UPDATE settings SET std_pp_limit = %s WHERE user_id = %s",
                          [value, user_id])
        elif update == "taiko_pp_limit":
            await mysql.execute("UPDATE settings SET taiko_pp_limit = %s WHERE user_id = %s",
                          [value, user_id])
        elif update == "ctb_pp_limit":
            await mysql.execute("UPDATE settings SET ctb_pp_limit = %s WHERE user_id = %s",
                          [value, user_id])
        elif update == "mania_pp_limit":
            await mysql.execute("UPDATE settings SET mania_pp_limit = %s WHERE user_id = %s",
                          [value, user_id])
        elif update == "format_score_osu":
            await mysql.execute("UPDATE settings SET format_score_osu = %s WHERE user_id = %s",
                          [value, user_id])
        elif update == "format_score_twitch":
            await mysql.execute("UPDATE settings SET format_score_twitch = %s WHERE user_id = %s",
                          [value, user_id])
        elif update == "format_request_osu":
            await mysql.execute("UPDATE settings SET format_request_osu = %s WHERE user_id = %s",
                          [value, user_id])
        elif update == "format_request_twitch":
            await mysql.execute("UPDATE settings SET format_request_twitch = %s WHERE user_id = %s",
                          [value, user_id])
        return json({"code": "1", "message": "User settings updated!"})
    else:
        return json({"code": "0", "message": "Bad POST request"})
