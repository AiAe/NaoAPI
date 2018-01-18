import aiohttp


async def get_user(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.ripple.moe/api/v1/users/full', params={"id": user_id}) as resp:
            r = await resp.json()

            return r
