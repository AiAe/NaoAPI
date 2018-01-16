from flask import request, jsonify
from helpers import mysql, group


def api():
    connection, cursor = mysql.connect()
    user_id = request.args.get('user_id')

    if user_id:

        full = {}

        find = mysql.execute(connection, cursor,
                             '''
                             SELECT users.user_id, users.username, users.twitch_username, settings.bot, 
                             settings.requests, settings.privileges, settings.std_pp_limit, 
                             settings.taiko_pp_limit, settings.ctb_pp_limit, settings.mania_pp_limit, 
                             settings.format_score_osu, settings.format_score_twitch, 
                             settings.format_request_osu, settings.format_request_twitch, tracking.std_pp, 
                             tracking.std_rank, tracking.taiko_pp, tracking.taiko_rank, tracking.ctb_pp, 
                             tracking.ctb_rank, tracking.mania_pp, tracking.mania_rank, 
                             tracking.nowplaying FROM users , settings , tracking WHERE users.user_id = %s
                             ''',
                             [user_id]).fetchone()

        full.update(find)
        full.update(group.get_group(find["privileges"]))

        return jsonify(full)
    else:
        return 'User not found!'
