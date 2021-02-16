import asyncio
import logging
from ..stream_command import stream_with_labeled_output_raw


class DisplayInterface():
    def __init__(self, display_command=None):
        if display_command is None:
            display_command = ["sudo", "python", "-u", "lib/display/album_display.py"]
        self._display_proc = None
        self._display_command = display_command
        self._now_displaying = None

    async def wait_for_display_proc(self, proc):
        await proc.wait()
        logging.debug("display proc exited")
        self._display_proc = None

    async def create_display_proc(self):
        proc, _, __ = await stream_with_labeled_output_raw("display", self._display_command)
        asyncio.create_task(self.wait_for_display_proc(proc))
        return proc

    async def ensure_display_proc(self):
        if not self._display_proc:
            self._display_proc = await self.create_display_proc()

    async def write_to_proc(self, msg):
        await self.ensure_display_proc()
        self._display_proc.stdin.write(f"{msg}\n".encode())
        await self._display_proc.stdin.drain()

    async def display_image_file(self, path, brightness):
        await self.write_to_proc(f"{path} {brightness}")

    async def display_nothing(self):
        await self.write_to_proc("")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    async def main():
        display = DisplayInterface(["python", "-u", "read_from_stdin.py"])

        while True:
            await display.display_image_file("foo")
            await asyncio.sleep(5)
            await display.display_nothing()
            await asyncio.sleep(5)

    asyncio.run(main())
