from helpers import mysql


async def user(request):
    user_id = request.args['user_id']

    u = await mysql.execute("SELECT user_id FROM users WHERE user_id = %s", [user_id])

    if u:
        return True

    return False
