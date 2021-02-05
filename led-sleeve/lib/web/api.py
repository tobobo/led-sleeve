from aiohttp import web


async def index(_request):
    return web.Response(text='hello api')


def serialize_account(account):
    return {
        'service_name': account.service_name,
        'now_playing_state': account.now_playing_state
    }


async def accounts_handler(request):
    accounts = await request.app['now_playing'].get_accounts()
    return web.json_response(list(map(serialize_account, accounts)))


async def create_api_app(now_playing):
    api = web.Application()
    api['now_playing'] = now_playing
    api.add_routes([web.get('/', index), web.get('/accounts', accounts_handler)])
    return api
