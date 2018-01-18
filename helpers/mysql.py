import json
import os
import aiomysql

with open(os.getcwd() + "/mysql.json", "r") as f:
    config = json.load(f)


async def execute(sql, args=None, one=True):
    pool = await aiomysql.create_pool(host=config['host'], port=3306, user=config['user'], password=config['password'],
                                      db=config['db'], autocommit=True, charset="utf8", use_unicode=True)

    async with pool.acquire() as connection:
        async with connection.cursor(aiomysql.DictCursor) as cursor:

            await cursor.execute(sql, args)

            if one:
                r = await cursor.fetchone()
            else:
                r = await cursor.fetchall()

            await cursor.close()

            return r
