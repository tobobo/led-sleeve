import asyncio
import sqlite3
from aiohttp import web
from ..accounts.spotify_account import SpotifyAccount


async def index(_request):
    return web.Response(text='hello api')


def serialize_account(account):
    return {
        'id': account.id,
        'provider': account.provider,
        'now_playing_state': account.now_playing_state
    }


async def get_accounts(request):
    accounts = await request.app['now_playing'].get_accounts()
    return web.json_response(list(map(serialize_account, accounts)))


async def get_account(request):
    account = await request.app['now_playing'].get_account_and_wait_for_status(
        request.match_info['provider'],
        request.match_info['id']
    )
    return web.json_response(serialize_account(account))


async def get_account_data(creation_data):
    provider = creation_data['provider']
    if provider == 'spotify':
        return await SpotifyAccount.create(creation_data)

    raise ValueError(f'unknown provider "{provider}"')


async def add_account(request):
    creation_data = await request.json()
    account_data = await get_account_data(creation_data)
    try:
        request.app['database'].add_account(account_data)
    except sqlite3.IntegrityError:
        return web.json_response({'error': 'duplicate_account'}, status=400)
    await request.app['now_playing'].reload_accounts()
    asyncio.create_task(request.app['now_playing'].wait_for_updates())
    return web.json_response({}, status=201)


async def create_api_app(database, now_playing):
    api = web.Application()
    api['now_playing'] = now_playing
    api['database'] = database
    api.add_routes([
        web.get('/', index),
        web.get('/accounts', get_accounts),
        web.get('/accounts/{provider}/{id}', get_account),
        web.post('/accounts', add_account),
    ])
    return api
