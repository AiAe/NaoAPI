from flask import request, jsonify
from helpers import mysql, user_exist, ripple


def api():
    user_id = request.args.get('user_id')
    code = request.args.get('code')

    if user_id and code and not user_exist.user():
        connection, cursor = mysql.connect()

        user = ripple.get_user(user_id)

        format_score_osu = "{song}{mods}{mode}({accuracy:.2f}%, {rank}) | {pp:.2f}pp"
        format_score_twitch = "{song}{mods}{mode}({accuracy:.2f}%, {rank}) | {pp:.2f}pp"
        format_request_osu = '''{sender}: [osu://dl/{beatmapsetid} {artist} - {title} [{version}]] {all_mods} {bpm}BPM 
        {stars}'''
        format_request_twitch = "{artist} - {title} [{version}] {all_mods} {bpm}BPM {stars}"

        mysql.execute(connection, cursor, "INSERT INTO users (user_id, username, code) VALUES (%s, %s, %s)",
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

        mysql.execute(connection, cursor, '''
        INSERT INTO tracking (user_id, std_pp, std_rank, taiko_pp, taiko_rank, ctb_pp, ctb_rank, mania_pp, mania_rank) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', [user_id, user["std"]["pp"], std_rank, user["taiko"]["pp"], taiko_rank, user["ctb"]["pp"], ctb_rank,
              user["mania"]["pp"], mania_rank])
        mysql.execute(connection, cursor, '''
        INSERT INTO settings (user_id, format_score_osu, format_score_twitch, format_request_osu, format_request_twitch) 
        VALUES (%s, %s, %s, %s, %s)
        ''', [user_id, format_score_osu, format_score_twitch, format_request_osu, format_request_twitch])

        return jsonify({"code": "1", "message": "User added!"})

    return jsonify({"code": "0", "message": "Bad POST request!"})
