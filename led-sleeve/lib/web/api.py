import asyncio
from ..accounts.spotify_account import SpotifyAccount
from aiohttp import web


async def index(_request):
    return web.Response(text='hello api')


def serialize_account(account):
    return {
        'provider': account.provider,
        'now_playing_state': account.now_playing_state
    }


async def get_account(request):
    accounts = await request.app['now_playing'].get_accounts()
    return web.json_response(list(map(serialize_account, accounts)))

async def get_account_data(creation_data):
    provider = creation_data['provider']
    if provider == 'spotify':
        return await SpotifyAccount.create(creation_data)
        
    raise ValueError(f'unknown provider "{provider}"')

async def add_account(request):
    creation_data = await request.json()
    account_data = await get_account_data(creation_data)
    request.app['database'].add_account(account_data)
    await request.app['now_playing'].reload_accounts()
    asyncio.create_task(request.app['now_playing'].wait_for_updates())
    return web.json_response({}, status=201)


async def create_api_app(database, now_playing):
    api = web.Application()
    api['now_playing'] = now_playing
    api['database'] = database
    api.add_routes([
        web.get('/', index),
        web.get('/accounts', get_account),
        web.post('/accounts', add_account)
    ])
    return api
