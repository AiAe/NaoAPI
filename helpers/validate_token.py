from helpers import mysql
from sanic.response import text


def valid_token(f):
    async def wrapper(request, *args, **kwargs):

        token = request.args["token"][0]

        find_token = await mysql.execute("SELECT token FROM access_keys WHERE token = %s", [token])

        if find_token:
            return await f(request, *args, **kwargs)
        else:
            return text('Not valid token')

    return wrapper