from sanic.response import json
from helpers import mysql, user_exist, ripple


async def api(request):
    user_id = request.args['user_id'][0]
    code = request.args['code'][0]

    is_user = await user_exist.user(request)

    if user_id and code and not is_user:

        user = await ripple.get_user(user_id)
        print(user)
        fso = "{song}{mods}{mode}({accuracy:.2f}%, {rank}) | {pp:.2f}pp"
        fst = "{song}{mods}{mode}({accuracy:.2f}%, {rank}) | {pp:.2f}pp"
        fro = "{sender}: [osu://dl/{beatmapsetid} {artist} - {title} [{version}]] {all_mods} {bpm}BPM {stars}"
        frt = "{artist} - {title} [{version}] {all_mods} {bpm}BPM {stars}"

        await mysql.execute("INSERT INTO users (user_id, username, token) VALUES (%s, %s, %s)",
                      [user_id, user["username"], code])

        if user["std"]["global_leaderboard_rank"]:
            std_rank = user["std"]["global_leaderboard_rank"]
        else:
            std_rank = 0
        if user["taiko"]["global_leaderboard_rank"]:
            taiko_rank = user["taiko"]["global_leaderboard_rank"]
        else:
            taiko_rank = 0
        if user["ctb"]["global_leaderboard_rank"]:
            ctb_rank = user["ctb"]["global_leaderboard_rank"]
        else:
            ctb_rank = 0
        if user["mania"]["global_leaderboard_rank"]:
            mania_rank = user["mania"]["global_leaderboard_rank"]
        else:
            mania_rank = 0

        await mysql.execute('''
        INSERT INTO tracking (user_id, std_pp, std_rank, taiko_pp, taiko_rank, ctb_pp, ctb_rank, mania_pp, mania_rank) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', [user_id, user["std"]["pp"], std_rank, user["taiko"]["pp"], taiko_rank, user["ctb"]["pp"], ctb_rank,
              user["mania"]["pp"], mania_rank])

        await mysql.execute('''
        INSERT INTO settings (user_id, format_score_osu, format_score_twitch, format_request_osu, format_request_twitch) 
        VALUES (%s, %s, %s, %s, %s)
        ''', [user_id, fso, fst, fro, frt])

        return json({"code": "1", "message": "User added!"})

    return json({"code": "0", "message": "Bad POST request!"})
