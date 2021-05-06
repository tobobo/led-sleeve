import asyncio
import logging
import signal
import os
import json
from ..stream_command import stream_with_labeled_output_raw


class DisplayInterface():
    def __init__(self, display_command=None):
        if display_command is None:
            display_command = ["sudo", "python",
                               "-u", "lib/display/album_display.py"]
        self._display_proc = None
        self._display_command = display_command
        self._now_displaying = None
        self._running = False

    async def wait_for_display_proc(self, proc):
        await proc.wait()
        logging.debug("display proc exited")
        self._display_proc = None

    async def stop(self):
        self._running = False
        logging.debug("stopping")
        if self._display_proc is not None:
            logging.debug("proc not none")
            os.killpg(os.getpgid(self._display_proc.pid), signal.SIGTERM)
            await self._display_proc.wait()
            self._display_proc = None

    async def create_display_proc(self):
        self._running = True
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
    
    async def send(self, msg):
        await self.write_to_proc(json.dumps(msg))

    async def display_image_file(self, path, brightness, position=None):
        if position is None:
            position = (0, 0)

        await self.send(
            [{
                'type': 'image',
                'path': path,
                'brightness': brightness,
                'position': position,
            }]
        )

    async def display_nothing(self):
        await self.send([{ 'type': 'clear' }])


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    async def main():
        display = DisplayInterface(["python", "-u", "read_from_stdin.py"])

        while True:
            await display.display_image_file("foo", 65536)
            await asyncio.sleep(5)
            await display.display_nothing()
            await asyncio.sleep(5)

    asyncio.run(main())
