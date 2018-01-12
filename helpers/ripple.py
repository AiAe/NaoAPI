import requests


def get_user(user_id):
    try:
        user = requests.get('https://api.ripple.moe/api/v1/users', params={"id": user_id}).json()

        return user
    except:
        return {"code": "0", "message": "User not found!"}
