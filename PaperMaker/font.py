from PIL import ImageFont
from .color import OColor


class OFont():

    def __init__(self, font_path, font_size, encoding="utf-8", color=OColor.BLACK):
        self._font_path = font_path
        self._font_size = font_size
        self._encoding = encoding
        self._font_color = color

    @property
    def font_path(self):
        return self._font_path

    @font_path.setter
    def font_path(self, font_path):
        self._font_path = font_path

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, font_size):
        self._font_size = font_size

    @property
    def encoding(self):
        return self._encoding

    @encoding.setter
    def encoding(self, encoding):
        self._encoding = encoding

    @property
    def font(self):
        return ImageFont.truetype(self._font_path, self._font_size, encoding=self._encoding)

    @property
    def font_color(self):
        return self._font_color
