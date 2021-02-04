class DisplayMediator():
    def __init__(self, image_preparer, display):
        self._image_preparer = image_preparer
        self._display = display
        self._last_displayed = None

    async def handle_image_update(self, image_url):
        if image_url == self._last_displayed:
            return
        self._last_displayed = image_url
        if image_url:
            image_path = await self._image_preparer.prepare(image_url)
            await self._display.display_image_file(image_path)
        else:
            await self._display.display_nothing()
