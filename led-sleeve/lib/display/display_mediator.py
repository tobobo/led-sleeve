class DisplayMediator():
    def __init__(self, now_playing, image_preparer, display):
        self._now_playing = now_playing
        self._image_preparer = image_preparer
        self._display = display
        self._last_displayed = None

        self._now_playing.on_update(self.handle_image_update)

    async def handle_image_update(self, image_url):
        if image_url == self._last_displayed:
            return
        self._last_displayed = image_url
        if image_url:
            image_path = await self._image_preparer.prepare(image_url)
            await self._display.display_image_file(image_path)
        else:
            await self._display.display_nothing()
