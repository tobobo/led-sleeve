from urllib.request import urlopen, urlretrieve
import mimetypes
import logging
import os
from ..stream_command import stream_with_labeled_output, get_stdout


class ImagePreparer():
    def __init__(self, image_dir_path='./data/display_image'):
        self._image_dir_path = image_dir_path
        if not os.path.exists(image_dir_path):
            os.makedirs(image_dir_path)

    async def prepare(self, image_url):
        with urlopen(image_url) as res:
            info = res.info()
            ext = mimetypes.guess_extension(info.get_content_type())
            if ext == ".jpe":
                ext = ".jpg"
            image_path = "{}/album{}".format(self._image_dir_path, ext)
            formatted_image_path = "{}/edited-album.png".format(self._image_dir_path)
            urlretrieve(image_url, image_path)
            await stream_with_labeled_output(
                "imagemagick",
                [
                    "/usr/bin/convert",
                    image_path,
                    "-resize", "64x64^",
                    "-gravity", "center",
                    "-extent", "64x64",
                    "+sigmoidal-contrast", "1,50%",
                    # "-brightness-contrast", "0x-10",
                    # "-modulate", "100,100,100",
                    "-gamma", "1.5",
                    # "-contrast", "1.1",
                    "-colorspace", "RGB",
                    formatted_image_path
                ]
            )
            image_path = formatted_image_path
            brightness_str = await get_stdout([
                "/usr/bin/convert",
                image_path,
                "-colorspace", "Gray",
                "-format", "%[fx:quantumrange*image.mean]",
                "info:"
            ])
            brightness = float(brightness_str)
            logging.debug("sending %s to display proc", image_path)
            return image_path, brightness
