import os
import asyncio
from aiohttp import web
from .api import create_api_app

this_dir = os.path.dirname(os.path.realpath(__file__))
public_dir = os.path.join(this_dir, 'public')

async def index(_request):
    return web.FileResponse(path=os.path.join(public_dir, 'index.html'))


async def start_server(now_playing):
    app = web.Application(middlewares=[web.normalize_path_middleware()])
    api_app = await create_api_app(now_playing)
    app.add_subapp('/api', api_app)
    app.add_routes([web.get('/', index), web.static('/', public_dir)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 80)
    await site.start()

if __name__ == "__main__":
    async def run():
        await start_server(None)
        while True:
            await asyncio.sleep(1)

    asyncio.run(run())
