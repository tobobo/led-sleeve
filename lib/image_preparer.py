from urllib.request import urlopen, urlretrieve
import mimetypes
import logging
import os


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
            urlretrieve(image_url, image_path)
            logging.debug(f"sending {image_path} to display proc")
            return image_path
