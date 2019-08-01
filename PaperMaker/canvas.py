from PIL import ImageFont, ImageDraw, Image
from .color import OColor

NONE_MARGIN = (0, 0, 0, 0)


class Canvas():
    NONE_MARGIN = (0, 0, 0, 0)
    ONE_MARGIN = (1, 1, 1, 1)
    TWO_MARGIN = (2, 2, 2, 2)
    THREE_MARGIN = (3, 3, 3, 3)

    def __init__(self):
        # self._margin = margin
        # self.bgcolor = color

        self._margin = self.setting.margin
        self.bgcolor = self.setting.color

    def setMargin(self, margin):
        self._margin = margin

    def setColor(self, color):
        self.bgcolor = color

    @property
    def top(self):
        return self._margin[0]

    @property
    def left(self):
        return self._margin[1]

    @property
    def down(self):
        return self._margin[2]

    @property
    def right(self):
        return self._margin[3]

    @property
    def origin(self):
        """
        返回左上角的原点 坐标
        :return: x, y
        """
        return (self.left, self.top)

    @property
    def size(self):
        return (0, 0)

    @property
    def image(self):
        return Image.new("RGB", self.size, self.bgcolor)
