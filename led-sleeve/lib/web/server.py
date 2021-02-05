import os
from aiohttp import web

this_dir = os.path.dirname(os.path.realpath(__file__))
public_dir = os.path.join(this_dir, 'public')

async def index(_request):
    return web.FileResponse(path=os.path.join(public_dir, 'index.html'))


async def start_server():
    app = web.Application()
    app.add_routes([web.get('/', index), web.static('/', public_dir)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 80)
    await site.start()
