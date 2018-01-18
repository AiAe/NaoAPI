from sanic.response import json
from helpers import mysql, user_exist, ripple

table = ["std_pp", "std_rank", "taiko_pp", "taiko_rank", "ctb_pp", "ctb_rank", "mania_pp", "mania_rank",
         "nowplaying"]


async def api(request):
    user_id = request.args['user_id'][0]
    update = request.args['update'][0]
    value = request.args['value'][0]

    if user_id and user_exist.user() and update in table or update == "stats":
        user = ripple.get_user(user_id)

        if not user["code"] == 0:

            if update == "nowplaying" and value:
                await mysql.execute("UPDATE tracking SET nowplaying = %s WHERE user_id = %s",
                              [value, user_id])
            elif update == "stats":

                current_stats = await mysql.execute("SELECT * FROM tracking WHERE user_id = %s",
                                              [user_id])

                await mysql.execute( '''
                UPDATE tracking SET std_pp = %s, std_rank = %s, taiko_pp = %s, taiko_rank = %s,
                 ctb_pp = %s, ctb_rank = %s, mania_pp = %s, mania_rank = %s WHERE user_id = %s
                ''',
                              [user["std"]["pp"], user["std"]["global_leaderboard_rank"], user["taiko"]["pp"],
                               user["taiko"]["global_leaderboard_rank"],
                               user["ctb"]["pp"], user["ctb"]["global_leaderboard_rank"], user["mania"]["pp"],
                               user["mania"]["global_leaderboard_rank"], user_id])

                stats = {
                    "update_std_pp": user["std"]["pp"] - current_stats["std_pp"],
                    "update_taiko_pp": user["taiko"]["pp"] - current_stats["taiko_pp"],
                    "update_ctb_pp": user["ctb"]["pp"] - current_stats["ctb_pp"],
                    "update_mania_pp": user["mania"]["pp"] - current_stats["mania_pp"],
                }

                if user["std"]["global_leaderboard_rank"]:
                    stats.update(
                        {"update_std_rank": current_stats["std_rank"] - user["std"]["global_leaderboard_rank"]})
                else:
                    stats.update({"update_std_rank": 0})
                if user["taiko"]["global_leaderboard_rank"]:
                    stats.update(
                        {"update_taiko_rank": current_stats["taiko_rank"] - user["taiko"]["global_leaderboard_rank"]})
                else:
                    stats.update({"update_taiko_rank": 0})
                if user["ctb"]["global_leaderboard_rank"]:
                    stats.update(
                        {"update_ctb_rank": current_stats["ctb_rank"] - user["ctb"]["global_leaderboard_rank"]})
                else:
                    stats.update({"update_ctb_rank": 0})
                if user["mania"]["global_leaderboard_rank"]:
                    stats.update(
                        {"update_mania_rank": current_stats["mania_rank"] - user["mania"]["global_leaderboard_rank"]})
                else:
                    stats.update({"update_mania_rank": 0})

                return json(stats)
            else:
                return json({"code": "0", "message": "Something went wrong!"})

            return json({"code": "1", "message": "Tracking updated!"})
    else:
        return json({"code": "0", "message": "Bad POST request!"})
