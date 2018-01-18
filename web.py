#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.response import html
from helpers import validate_token
from routes import api_user_full, api_get_user, api_get_settings, \
    api_get_tracking, api_update_settings, api_update_tracking, \
    api_update_user, api_insert_user, api_twitch, api_list

app = Sanic()


@app.route('/')
async def index(request):
    return html("<div style='line-height: 1;'>"
                "╭━╮╱╭╮╱╱╱╱╱╭━━━┳━━━┳━━╮╱╱╱╭╮╱╭━━━╮<br>"
                "┃┃╰╮┃┃╱╱╱╱╱┃╭━╮┃╭━╮┣┫┣╯╱╱╭╯┃╱┃╭━╮┃<br>"
                "┃╭╮╰╯┣━━┳━━┫┃╱┃┃╰━╯┃┃┃╱╭╮┣╮┃╱┃┃┃┃┃<br>"
                "┃┃╰╮┃┃╭╮┃╭╮┃╰━╯┃╭━━╯┃┃╱┃╰╯┃┃╱┃┃┃┃┃<br>"
                "┃┃╱┃┃┃╭╮┃╰╯┃╭━╮┃┃╱╱╭┫┣╮╰╮╭╯╰┳┫╰━╯┃<br>"
                "╰╯╱╰━┻╯╰┻━━┻╯╱╰┻╯╱╱╰━━╯╱╰┻━━┻┻━━━╯<br>"
                "</div>")


@app.get('/api/full')
@validate_token.valid_token
async def route_api_list(request):
    return await api_user_full.api(request)


@app.get('/api/get_user')
@validate_token.valid_token
async def route_api_get_user(request):
    return await api_get_user.api(request)


@app.get('/api/get_settings')
@validate_token.valid_token
async def route_api_get_settings(request):
    return await api_get_settings.api(request)


@app.get('/api/get_tracking')
@validate_token.valid_token
async def route_api_get_tracking(request):
    return await api_get_tracking.api(request)


@app.get('/api/list')
@validate_token.valid_token
async def route_api_get_list(request):
    return await api_list.api(request)


@app.post('/api/update/user')
@validate_token.valid_token
async def route_api_update_user(request):
    return await api_update_user.api(request)


@app.post('/api/update/settings')
@validate_token.valid_token
async def route_api_update_settings(request):
    return await api_update_settings.api(request)


@app.post('/api/update/tracking')
@validate_token.valid_token
async def route_api_update_tracking(request):
    return await api_update_tracking.api(request)


@app.get('/api/insert/user')
@validate_token.valid_token
async def route_api_insert_user(request):
    return await api_insert_user.api(request)


@app.get('/api/twitch')
async def route_api_twitch(request):
    return await api_twitch.api(request)


@app.get('/favicon.ico')
async def route_api_twitch(request):
    return ''


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=6969, debug=True)
