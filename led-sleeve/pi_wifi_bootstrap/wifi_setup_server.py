import asyncio
from aiohttp import web


async def index(request):
    return web.FileResponse(path='public/index.html')


async def set_credentials(request):
    data = await request.post()
    asyncio.create_task(request.app['credentials_callback'](
        data['ssid'], data['psk']))
    return web.Response(text="OK")


async def create_site(credentials_callback):
    app = web.Application()
    app['credentials_callback'] = credentials_callback
    app.add_routes(
        [web.get('/', index), web.post('/set_credentials', set_credentials), web.static('/', 'public')])
    runner = web.AppRunner(app)
    await runner.setup()
    return web.TCPSite(runner, '0.0.0.0', 8080)


async def get_credentials_from_server():
    future = asyncio.get_event_loop().create_future()

    async def credentials_callback(ssid, psk):
        future.set_result((ssid, psk))
        await site.stop()

    site = await create_site(credentials_callback)
    await site.start()
    return await future

if __name__ == "__main__":
    async def get_credentials_and_report():
        ssid, psk = await get_credentials_from_server()
        print(ssid)
        print(psk)

    while True:
        asyncio.run(get_credentials_and_report())
