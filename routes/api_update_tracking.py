from flask import request, jsonify
from helpers import mysql, user_exist, ripple

table = ["std_pp", "std_rank", "taiko_pp", "taiko_rank", "ctb_pp", "ctb_rank", "mania_pp", "mania_rank",
         "nowplaying"]


def api():
    user_id = request.args.get('user_id')
    update = request.args.get('update')
    value = request.args.get('value')

    if user_id and user_exist.user() and update in table or update == "stats":
        connection, cursor = mysql.connect()

        user = ripple.get_user(user_id)

        if not user["code"] == 0:

            if update == "nowplaying" and value:
                mysql.execute(connection, cursor, "UPDATE tracking SET nowplaying = %s WHERE user_id = %s",
                              [value, user_id])
            elif update == "stats":

                current_stats = mysql.execute(connection, cursor, "SELECT * FROM tracking WHERE user_id = %s",
                                              [user_id]).fetchone()

                mysql.execute(connection, cursor, '''
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

                return jsonify(stats)
            else:
                return jsonify({"code": "0", "message": "Something went wrong!"})

            return jsonify({"code": "1", "message": "Tracking updated!"})
    else:
        return jsonify({"code": "0", "message": "Bad POST request!"})
