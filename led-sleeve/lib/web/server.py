import os
import platform
from aiohttp import web
from .api import create_api_app

this_dir = os.path.dirname(os.path.realpath(__file__))
public_dir = os.path.join(this_dir, 'public')

async def config(_request):
    return web.json_response({
        'auth_site_base': os.getenv('AUTH_SITE_BASE'),
        'device_name': os.getenv('DEVICE_NAME')
    })

async def index(_request):
    return web.FileResponse(path=os.path.join(public_dir, 'index.html'))

async def disable_cache(_request, response):
    print('cache control')
    response.headers['Cache-Control'] = 'no-cache'

async def start_server(database, now_playing):
    app = web.Application(middlewares=[web.normalize_path_middleware()])
    app.on_response_prepare.append(disable_cache)
    api_app = await create_api_app(database, now_playing)
    app.add_subapp('/api', api_app)
    app.add_routes([web.get('/', index), web.get('/config.json', config), web.static('/', public_dir)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 80)
    await site.start()
